import pandas as pd
import numpy as np
from fuzzywuzzy import process, fuzz
from src.setup import COMPANY, ENG_DESIGNATIONS, ENG_MODEL, LR, VSL_ID, VSL_ENGINES


def add_match(new_eng, existing_list):
    highest = process.extractOne(new_eng, existing_list)
    sid_closest_eng = highest[0]
    sid_closest_eng_val = highest[1]
    return sid_closest_eng_val, sid_closest_eng


def compare_company(str1, str2):
    match = fuzz.token_set_ratio(str1, str2)
    return match


company_cols_to_include = [
    'ID',
    'ROOT_NAME'
]

eng_model_cols_to_include = [
    'CODE',
    'DESIGN_COMPID'
]

sid_eng_desig_cols_to_compare_with_lr = [
    'ENGINE_DESIGNATION',
    'BORE',
    'CYLINDER_ARRANGEMENT',
    'NUMBER_OF_CYLINDERS',
    'FUEL_TYPE',
    'STROKE',
    'Designer'
]

sid_vsl_eng_cols_to_include = [
    'LREGNO',
    'NAME',
    'LLPNO',
    'ENGINE_DESIGNATION',
    'MANUF_COMPID',
    'BUILT_PLACEIDNO',
    'BUILT_TOWN_ID'
]

output_cols_to_include = [
    'ENGINE_DESIGNATION_lr', 'ENGINE_DESIGNATION_compare', 'eng_desig_match_val',
    'CYLINDERS_ARRANGEMENT_lr', 'CYLINDER_ARRANGEMENT_compare',
    'NO_OF_CYLINDERS_lr', 'NUMBER_OF_CYLINDERS_compare',
    'BORE_lr', 'BORE_compare',
    'STROKE_lr', 'STROKE_compare',
    'FUEL_TYPE_lr', 'FUEL_TYPE_compare',
    'DESIGNER_lr', 'Designer_compare'
]

if __name__ == '__main__':
    # SID Company table
    sid_company_df = pd.read_csv(COMPANY, encoding='cp1252', low_memory=False, usecols=company_cols_to_include)
    # SID Engines Designation tables
    sid_eng_desig_df = pd.read_csv(ENG_DESIGNATIONS, encoding='cp1252')
    # SID Engines Models tables
    sid_eng_model_df = pd.read_csv(ENG_MODEL, encoding='cp1252', usecols=eng_model_cols_to_include)
    # SID Vessel ID (with IMO and LLPNO)
    sid_vsl_ID_df = pd.read_csv(VSL_ID, encoding='cp1252')
    # SID Vessel Engines table
    sid_vsl_eng_df = pd.read_csv(VSL_ENGINES, encoding='cp1252', low_memory=False)
    # LR Vessel Engine Data
    lr_raw_df = pd.read_csv(LR, dtype={'IMO': float})

    # Process LR data - remove auxiliary engines
    lr_df = lr_raw_df.loc[lr_raw_df.MAIN_OR_AUX == 'MAIN']  # only using Main engine datasets
    list_lr_imos = lr_df.IMO.unique().tolist()  # get list of IMOs of interest

    # Process SID Engine datasets
    # Select relevant IMOs - help computational intensity
    sid_relevent_imo_df = sid_vsl_ID_df.loc[sid_vsl_ID_df.LREGNO.isin(list_lr_imos)]
    # Adding IMO to engine table
    sid_vsl_eng_with_id = sid_vsl_eng_df.merge(sid_relevent_imo_df, how='left', on='LLPNO')
    # Filtering to relevant IMOs and columns
    sid_vsl_eng = sid_vsl_eng_with_id.loc[(sid_vsl_eng_with_id.LREGNO.isin(list_lr_imos)) &
                                          (sid_vsl_eng_with_id.ENDDT.isnull())][sid_vsl_eng_cols_to_include]

    # Join SID Engine Designation, Model and Company onto the vessel table with engines, filter cols & remove duplicates
    sid_df = sid_eng_desig_df.merge(sid_eng_model_df, how='left', on='CODE')\
        .merge(sid_company_df, how='left', left_on='DESIGN_COMPID', right_on='ID')\
        .rename(columns={'ROOT_NAME': 'Designer'})\
        .drop(columns='DESIGN_COMPID', axis=1)[sid_eng_desig_cols_to_compare_with_lr]
    sid_vsl_all_features_df = sid_vsl_eng.merge(sid_df, how='left', on='ENGINE_DESIGNATION') \
        .merge(sid_company_df, how='left', left_on='MANUF_COMPID', right_on='ID') \
        .drop(['MANUF_COMPID', 'ID'], axis=1) \
        .rename(columns={'ROOT_NAME': 'MANUFACTURER'})\
        .drop_duplicates()

    # Part 1: Of the vessels that we have in common, check those that match (& add suffix to header to show source)
    lr_sid = sid_vsl_all_features_df.add_suffix('_sid').merge(lr_df.add_suffix('_lr'),
                                                              how='right', right_on='IMO_lr', left_on='LREGNO_sid')
    lr_sid_eq = lr_sid.loc[(lr_sid.ENGINE_DESIGNATION_sid == lr_sid.ENGINE_DESIGNATION_lr)]
    lr_sid_neq = lr_sid.loc[~(lr_sid.ENGINE_DESIGNATION_sid == lr_sid.ENGINE_DESIGNATION_lr)]

    # Part 2: Get gain i.e. number of non null entries from LR where the SID value is 'UNKNOWN' or null (i.e. new IMOs)
    gain = lr_sid_neq.loc[((lr_sid_neq.ENGINE_DESIGNATION_sid == 'UNKNOWN') | (lr_sid_neq.ENGINE_DESIGNATION_sid.isnull()))
                          & (lr_sid_neq.ENGINE_DESIGNATION_lr != 'N/K')
                          & (lr_sid_neq.ENGINE_DESIGNATION_lr.notnull())]

    # Part 3: Isolate the new values from LR that replace the UNKNOWN values that are new eng designations
    existing_eng_desig = sid_eng_desig_df.ENGINE_DESIGNATION.tolist()
    new_eng_des_replace_unk = np.setdiff1d(gain.ENGINE_DESIGNATION_lr.unique().tolist(), existing_eng_desig)

    # Part 4: Identify engine designation and Manufacturer values that are very different - this part is TIMELY!
    new_eng_desig_with_eng_matches_df = gain.loc[gain.ENGINE_DESIGNATION_lr.isin(new_eng_des_replace_unk)]
    new_eng_desig_with_eng_matches_df[['eng_desig_match_val',
                      'eng_desig_match_in_sid']] = new_eng_desig_with_eng_matches_df\
        .apply(lambda row: pd.Series(add_match(row['ENGINE_DESIGNATION_lr'], existing_eng_desig)), axis=1)
    # new_eng_desig_with_eng_matches_df.to_csv('datasets/output/temporary_fuzzy_results.csv', index=False)

    # Part 5: Get the Designer etc of the existing Engine Desigination value from SID that is closest to the LR value
    new_eng_desig_with_eng_manu_matches_df = new_eng_desig_with_eng_matches_df.merge(sid_df.add_suffix('_compare'),
                                                                                     how='left',
                                                                                     left_on='eng_desig_match_in_sid',
                                                                                     right_on='ENGINE_DESIGNATION_'
                                                                                              'compare')

    # Part 6: Drop irrelevant columns and duplicates - doesn't need to be on ship by ship level
    # Need: Model, Description, Designer, Designation, Bore, Arrangement, No. Cyl, Type, Cycle, Action, Fuel, Stroke
    # Don't have: Model, Description, Action, Cycle
    # Less Priority: Engine_Type, FUEL_TYPE
    # Don't include: IMO, No Engine, Place of Build, POWER_KW MAIN_OR_AUX
    output_df = new_eng_desig_with_eng_manu_matches_df[output_cols_to_include].drop_duplicates()

    # Part 7: Add value for matching the designer
    output_df['designer_match_val'] = output_df.apply(lambda row: pd.Series(compare_company(row['Designer_compare'],
                                                                                            row['DESIGNER_lr'])),
                                                      axis=1)
    output_df.to_csv('lr_engine_designation_comparison.csv', index=False)

    # Part 8: File manually reviewed for engine designations that do and don't match and based on outputs:
    # 8a/ Create df for MAPPING new engine designations that have a similar existing in SID

    # 8b/ Creating df of NEW engine designations that will need to be created, along with other features
    # TODO include relevant columns that match the engine models page

