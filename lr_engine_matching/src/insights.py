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


if __name__ == '__main__':
    # SID Company table
    sid_company_df = pd.read_csv(COMPANY, encoding='cp1252', low_memory=False, usecols=company_cols_to_include)
    # SID Vessel Engines Designation tables
    sid_vsl_eng_desig_raw_df = pd.read_csv(ENG_DESIGNATIONS, encoding='cp1252')
    # SID Vessel Engines Models tables
    sid_vsl_eng_model_df = pd.read_csv(ENG_MODEL, encoding='cp1252', usecols=eng_model_cols_to_include)
    # SID Vessel ID (with IMO and LLPNO)
    sid_vsl_ID_raw_df = pd.read_csv(VSL_ID, encoding='cp1252')
    # SID Engines table
    sid_vsl_eng_raw_df = pd.read_csv(VSL_ENGINES, encoding='cp1252', low_memory=False)
    # LR Engine Data
    lr_raw_df = pd.read_csv(LR, dtype={'IMO': float})

    # Process LR dataset
    lr_df = lr_raw_df.loc[lr_raw_df.MAIN_OR_AUX == 'MAIN']  # only using Main engine datasets
    list_lr_imos = lr_df.IMO.unique().tolist()  # get list of IMOs of interest
    count_nan_eng_desig_lr = lr_df.isna().sum().ENGINE_DESIGNATION
    count_unk_eng_desig_lr = len(lr_df.loc[lr_df.ENGINE_DESIGNATION == 'N/K'])
    print("The LR datasets for Main Engines has {} missing values for Engine Designation and {} values as 'N/K'."
          .format(count_nan_eng_desig_lr, count_unk_eng_desig_lr))

    # Process SID Engine Designation, Model and Company
    sid_df = sid_vsl_eng_desig_raw_df.merge(sid_vsl_eng_model_df, how='left', on='CODE')\
                                     .merge(sid_company_df, how='left', left_on='DESIGN_COMPID', right_on='ID')

    # Process SID Engine datasets
    sid_relevent_imo_df = sid_vsl_ID_raw_df.loc[sid_vsl_ID_raw_df.LREGNO.isin(list_lr_imos)]   # select relevant IMOs
    sid_imos_for_lr = sid_relevent_imo_df.LREGNO.unique().tolist()
    diff_list = np.setdiff1d(list_lr_imos, sid_imos_for_lr)  # yields the elements in first list that aren't in second
    print('There are {} IMOs from LR that need to be created in SID (or have IMO assigned).'.format(len(diff_list)))

    sid_vsl_eng_with_id = sid_vsl_eng_raw_df.merge(sid_relevent_imo_df, how='left', on='LLPNO')  # adding imo to engine table
    sid_vsl_eng = sid_vsl_eng_with_id.loc[(sid_vsl_eng_with_id.LREGNO.isin(list_lr_imos)) &
                                          (sid_vsl_eng_with_id.ENDDT.isnull())]  # filtering to relevant imos
    diff_list_sid_eng = np.setdiff1d(list_lr_imos, sid_vsl_eng.LREGNO.unique().tolist())
    # has multiple rows for one vessel & some vessels won't have engine values although in SID
    # no duplicated values in SID where the Engine Designation is UNKNOWN
    # len(sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'].drop_duplicates()) -
    # len(sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'])
    print("\nOut of the LR IMOs, {} are not contained in the SID vessel engine designation table, "
          "{} have null values in this table for Engine Designation and "
          "{} have the value 'UNKNOWN'".format(len(diff_list_sid_eng),
                                               sid_vsl_eng.isna().sum().ENGINE_DESIGNATION,
                                               len(sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'])))

    # Part 1: Of the vessels that we have in common, check matches - take subset of datasets columns for ease
    sid_vsl_sub = sid_vsl_eng[['LREGNO', 'LLPNO', 'ENGINE_DESIGNATION', 'MANUF_COMPID']].drop_duplicates()  # remove drop dup after
    lr_sub = lr_df[['IMO', 'ENGINE_DESIGNATION', 'ENGINE_BUILDER']]

    # merge the two to compare where equal, unequal and both NaN
    lr_sid = sid_vsl_sub.merge(lr_sub, how='right', right_on='IMO', left_on='LREGNO', suffixes=('_sid', '_lr'))
    lr_sid_eq = lr_sid.loc[(lr_sid.LREGNO == lr_sid.IMO) & (lr_sid.ENGINE_DESIGNATION_sid == lr_sid.ENGINE_DESIGNATION_lr)]
    lr_sid_neq = pd.concat([lr_sid, lr_sid_eq]).drop_duplicates(keep=False)
    print('\nNumber rows where LR and SID have the same datasets is {}.'.format(len(lr_sid_eq)))
    print('Number rows where LR reports datasets different to what is in SID is {}.'.format(len(lr_sid_neq)))  # includes NaNs

    # Number of non null entries from LR where the SID value is 'UNKNOWN' or null (i.e. new IMOs)
    gain = lr_sid_neq.loc[((lr_sid_neq.ENGINE_DESIGNATION_sid == 'UNKNOWN') | (lr_sid_neq.ENGINE_DESIGNATION_sid.isnull()))
                                   & (lr_sid_neq.ENGINE_DESIGNATION_lr != 'N/K')
                                   & (lr_sid_neq.ENGINE_DESIGNATION_lr.notnull())]\
        .merge(sid_company_df, how='left', left_on='MANUF_COMPID', right_on='ID')\
        .drop(['IMO', 'MANUF_COMPID', 'ID'], axis=1)\
        .rename(columns={'ENGINE_BUILDER': 'ENGINE_BUILDER_lr',
                         'ROOT_NAME': 'MANUFACTURER_sid'})
    # Removing extra columns that don't add much and renaming to identify source
    # Adding Manufacturer Name from SID based on existing MANUF_COMPID

    print("Number of non null entries from LR where the SID value is 'UNKNOWN' is {}. This is the gain from LR."
          .format(len(gain)))
    # More than the number of unknown values in sid since some will have multiple entries from LR
    # e.g. sid_vsl_sub.loc[sid_vsl_sub.LREGNO == 1012983.0]

    # IMO with UNKNOWN in SID and not in LR - still missing datasets
    sid_imo_unk_eng = sid_vsl_eng.loc[sid_vsl_eng.ENGINE_DESIGNATION == 'UNKNOWN'].LREGNO.unique()
    lr_gain_imo = gain.LREGNO.unique()
    imo_unk_eng_not_lr = np.setdiff1d(sid_imo_unk_eng, lr_gain_imo)  # IMOs that have UNK value that aren't in LR
    print('There are {} IMOs in SID with an UNKNOWN Engine Designation that LR does not have '
          'datasets for.'.format(len(imo_unk_eng_not_lr)))

    # 2/ Isolate the engine designations aren't in SID
    no_match_eng_desig = lr_sid_neq.ENGINE_DESIGNATION_lr.unique().tolist()
    existing_eng_desig = sid_df.ENGINE_DESIGNATION.tolist()
    new_eng_desig = np.setdiff1d(no_match_eng_desig, existing_eng_desig)
    print("There are {} engine designations from LR that aren't in SID.".format(len(new_eng_desig)))
    # of the new values from LR that replace the UNKNOWN values - which are new eng designations
    new_eng_des_replace_unk = np.setdiff1d(gain.ENGINE_DESIGNATION_y.unique().tolist(), existing_eng_desig)
    print("Of the 'UNKNOWN' values in SID that LR has values for, there are {} engine "
          "designations not in SID".format(len(new_eng_des_replace_unk)))

    # Other checks:
    # lr_sid_neq['fuzzy_PR'] = lr_sid_neq.apply(lambda x: float(fuzz.partial_ratio(x['sid_eng_des'], x['lr_eng_des']))
    #                                           , axis=1)
    # a = lr_sid_neq.loc[(lr_sid_neq.lr_eng_des != 'N/K')
    #                    & (lr_sid_neq.lr_eng_des != 'None')
    #                    & (lr_sid_neq.sid_eng_des != 'None')
    #                    & (lr_sid_neq.sid_eng_des != 'UNKNOWN')]
    # a.loc[(a.fuzzy_PR <80.)&(a.fuzzy_PR >70.)]

    # sid_vsl_eng.loc[sid_vsl_eng.LREGNO==9800180.0].iloc[1]   # duplicated values and does have no_engines
    # sid_vsl_eng.loc[sid_vsl_eng.LREGNO==8705383.0].iloc[1]   # doesn't have no_engines
    # lr_sid_neq.loc[(lr_sid_neq.ENGINE_DESIGNATION_x.isnull()) & (lr_sid_neq.ENGINE_DESIGNATION_y.isnull())]
    # lr_sub['a']  = lr_sub.groupby('IMO').transform('count') get no. unique times
