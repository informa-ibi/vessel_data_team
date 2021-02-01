import pandas as pd
import numpy as np
from src.setup import COMPANY, ENG_DESIGNATIONS, ENG_MODEL, LR, VSL_ID, VSL_ENGINES

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

if __name__ == '__main__':
    # SID Company table
    sid_company_df = pd.read_csv(COMPANY, encoding='cp1252', low_memory=False, usecols=company_cols_to_include)
    # SID Engines Designation tables
    sid_eng_desig_df = pd.read_csv(ENG_DESIGNATIONS, encoding='cp1252')
    # SID Vessel Engines Models tables
    sid_eng_model_df = pd.read_csv(ENG_MODEL, encoding='cp1252', usecols=eng_model_cols_to_include)
    # SID Vessel ID (with IMO and LLPNO)
    sid_vsl_ID_df = pd.read_csv(VSL_ID, encoding='cp1252')
    # SID Engines table
    sid_vsl_eng_df = pd.read_csv(VSL_ENGINES, encoding='cp1252', low_memory=False)
    # LR Engine Data
    lr_raw_df = pd.read_csv(LR, dtype={'IMO': float})

    # Process LR dataset
    lr_df = lr_raw_df.loc[lr_raw_df.MAIN_OR_AUX == 'MAIN']  # only using Main engine datasets
    list_lr_imos = lr_df.IMO.unique().tolist()  # get list of IMOs of interest
    count_nan_eng_desig_lr = lr_df.isna().sum().ENGINE_DESIGNATION
    count_unk_eng_desig_lr = len(lr_df.loc[lr_df.ENGINE_DESIGNATION == 'N/K'])
    print("The LR datasets for Main Engines has {} missing values for Engine Designation and {} values as 'N/K'"
          " out of {} total values."
          .format(count_nan_eng_desig_lr, count_unk_eng_desig_lr, len(lr_df)))
    print("No. unique vessels in the Main Engine data is {}".format(len(lr_df.IMO.unique())))
    lr_uplift_df = lr_df.loc[~((lr_df.ENGINE_DESIGNATION.isnull()) | (lr_df.ENGINE_DESIGNATION=='N/K'))]
    print("Total number observations in LR main engine data where the data is informative i.e. isn't missing or unknown"
          " is {}".format(len(lr_uplift_df)))
    print('Total unique IMOs in this is {}'.format(len(lr_uplift_df.IMO.unique())))

    # Process SID Engine datasets
    # Select relevant IMOs - help computational intensity
    sid_relevent_imo_df = sid_vsl_ID_df.loc[sid_vsl_ID_df.LREGNO.isin(list_lr_imos)]
    # List of IMOs from LR that we have in SID
    sid_imos_for_lr = sid_relevent_imo_df.LREGNO.unique().tolist()
    diff_list = np.setdiff1d(list_lr_imos, sid_imos_for_lr)  # yields the elements in first list that aren't in second
    print('There are {} IMOs from LR that need to be created in SID (or have IMO assigned).'.format(len(diff_list)))

    # Adding IMO to engine table
    sid_vsl_eng_with_id = sid_vsl_eng_df.merge(sid_relevent_imo_df, how='left', on='LLPNO')
    # Filtering to relevant IMOs and columns
    sid_vsl_eng = sid_vsl_eng_with_id.loc[(sid_vsl_eng_with_id.LREGNO.isin(list_lr_imos)) &
                                          (sid_vsl_eng_with_id.ENDDT.isnull())][sid_vsl_eng_cols_to_include]
    diff_list_sid_eng = np.setdiff1d(list_lr_imos, sid_vsl_eng.LREGNO.unique().tolist())
    # has multiple rows for one vessel & some vessels won't have engine values although in SID
    # no duplicated values in SID where the Engine Designation is UNKNOWN
    # len(sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'].drop_duplicates()) -
    # len(sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'])
    print("\nOut of the {} LR IMOs, {} are not contained in the SID vessel engine designation table, "
          "{} have null values in this table for Engine Designation and "
          "{} have the value 'UNKNOWN'".format(len(lr_df.IMO.unique()),
                                               len(diff_list_sid_eng),
                                               sid_vsl_eng.isna().sum().ENGINE_DESIGNATION,
                                               len(sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'].LREGNO.unique())))

    # Join SID Engine Designation, Model and Company onto the vessel table with engines, filter cols & remove duplicates
    sid_df = sid_eng_desig_df.merge(sid_eng_model_df, how='left', on='CODE') \
        .merge(sid_company_df, how='left', left_on='DESIGN_COMPID', right_on='ID') \
        .rename(columns={'ROOT_NAME': 'Designer'}) \
        .drop(columns='DESIGN_COMPID', axis=1)[sid_eng_desig_cols_to_compare_with_lr]
    sid_vsl_all_features_df = sid_vsl_eng.merge(sid_df, how='left', on='ENGINE_DESIGNATION') \
        .merge(sid_company_df, how='left', left_on='MANUF_COMPID', right_on='ID') \
        .drop(['MANUF_COMPID', 'ID'], axis=1) \
        .rename(columns={'ROOT_NAME': 'MANUFACTURER'}) \
        .drop_duplicates()

    # Part 1: Of the vessels that we have in common, check those that match (& add suffix to header to show source)
    lr_sid = sid_vsl_all_features_df.add_suffix('_sid').merge(lr_df.add_suffix('_lr'),
                                                              how='right', right_on='IMO_lr', left_on='LREGNO_sid')
    lr_sid_eq = lr_sid.loc[(lr_sid.ENGINE_DESIGNATION_sid == lr_sid.ENGINE_DESIGNATION_lr)]
    lr_sid_neq = lr_sid.loc[~(lr_sid.ENGINE_DESIGNATION_sid == lr_sid.ENGINE_DESIGNATION_lr)]
    print('\nNumber rows where LR and SID have the same datasets is {}.'.format(len(lr_sid_eq)))
    print('Number rows where LR reports datasets different to what is in SID is {}.'.format(len(lr_sid_neq))) # NaNs too

    # Part 2: Get gain i.e. number of non null entries from LR where the SID value is 'UNKNOWN' or null (i.e. new IMOs)
    gain = lr_sid_neq.loc[
        ((lr_sid_neq.ENGINE_DESIGNATION_sid == 'UNKNOWN') | (lr_sid_neq.ENGINE_DESIGNATION_sid.isnull()))
        & (lr_sid_neq.ENGINE_DESIGNATION_lr != 'N/K')
        & (lr_sid_neq.ENGINE_DESIGNATION_lr.notnull())]
    print("Number of non null entries from LR where the SID value is 'UNKNOWN' is {}. This is the gain from LR."
          .format(len(gain)))
    # More than the number of unknown values in sid since some will have multiple entries from LR
    # e.g. sid_vsl_sub.loc[sid_vsl_sub.LREGNO == 1012983.0]

    # IMO with UNKNOWN in SID and not in LR - still missing datasets
    sid_imo_unk_eng = sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'].LREGNO.unique()
    lr_gain_imo = gain.LREGNO_sid.unique()
    imo_unk_eng_not_lr = np.setdiff1d(sid_imo_unk_eng, lr_gain_imo)  # IMOs that have UNK value that aren't in LR
    print('There are {} out of {} IMOs in SID with an UNKNOWN Engine Designation that LR does not have '
          'data for.'.format(len(imo_unk_eng_not_lr), len(sid_imo_unk_eng)))

    # Part 3: Isolate the engine designations aren't in SID
    lr_eng_desig = lr_df.ENGINE_DESIGNATION.unique().tolist()
    existing_eng_desig = sid_eng_desig_df.ENGINE_DESIGNATION.tolist()
    new_eng_desig = np.setdiff1d(lr_eng_desig, existing_eng_desig)
    print("There are {} engine designations from LR that aren't in SID, which has {}.".format(len(new_eng_desig),
                                                                                              len(existing_eng_desig)))
    # Isolate the new values from LR that replace the UNKNOWN values that are new eng designations
    new_eng_des_replace_unk = np.setdiff1d(gain.ENGINE_DESIGNATION_lr.unique().tolist(), existing_eng_desig)
    print("Of the 'UNKNOWN' values in SID that LR has values for i.e. the gain from LR, there are {} engine "
          "designations not in SID out of the {} that engine designations in SID".format(len(new_eng_des_replace_unk),
                                                                                         len(existing_eng_desig)))

    # sid_vsl_eng.loc[sid_vsl_eng.LREGNO==9800180.0].iloc[1]   # duplicated values and does have no_engines
    # sid_vsl_eng.loc[sid_vsl_eng.LREGNO==8705383.0].iloc[1]   # doesn't have no_engines
    # lr_sid_neq.loc[(lr_sid_neq.ENGINE_DESIGNATION_x.isnull()) & (lr_sid_neq.ENGINE_DESIGNATION_y.isnull())]
    # lr_sub['a']  = lr_sub.groupby('IMO').transform('count') get no. unique times
