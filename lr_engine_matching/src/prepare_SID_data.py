import pandas as pd
from src.setup import COMPANY, ENG_DESIGNATIONS, ENG_MODEL, LR, VSL_ID, VSL_ENGINES, SID_PROCESSED, LR_PROCESSED


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
    'NUMBER_OF_ENGINES',
    'ENGINE_DESIGNATION',
    'MANUF_COMPID',
    'BUILT_PLACEIDNO',
    'BUILT_TOWN_ID'
]

if __name__ == '__main__':
    # SID Company table
    sid_company_df = pd.read_csv(COMPANY, encoding='cp1252', low_memory=False, usecols=company_cols_to_include)
    # SID Engines Designation tables
    sid_eng_desig_df = pd.read_csv(ENG_DESIGNATIONS, encoding='cp1252', low_memory=False)
    # SID Engines Models tables
    sid_eng_model_df = pd.read_csv(ENG_MODEL, encoding='cp1252', low_memory=False, usecols=eng_model_cols_to_include)
    # SID Vessel ID (with IMO and LLPNO)
    sid_vsl_ID_df = pd.read_csv(VSL_ID, encoding='cp1252', low_memory=False)
    # SID Vessel Engines table
    sid_vsl_eng_df = pd.read_csv(VSL_ENGINES, encoding='cp1252', low_memory=False)
    # LR Vessel Engine Data
    lr_raw_df = pd.read_csv(LR, dtype={'IMO': float})

    # Process LR data - remove auxiliary engines
    lr_df = lr_raw_df.loc[lr_raw_df.MAIN_OR_AUX == 'MAIN'].reset_index().drop(columns='index', axis=1)  # Main eng only
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
    sid_df = sid_eng_desig_df.merge(sid_eng_model_df, how='left', on='CODE') \
        .merge(sid_company_df, how='left', left_on='DESIGN_COMPID', right_on='ID') \
        .rename(columns={'ROOT_NAME': 'Designer'}) \
        .drop(columns='DESIGN_COMPID', axis=1)[sid_eng_desig_cols_to_compare_with_lr]
    sid_vsl_all_features_df = sid_vsl_eng.merge(sid_df, how='left', on='ENGINE_DESIGNATION') \
        .merge(sid_company_df, how='left', left_on='MANUF_COMPID', right_on='ID') \
        .drop(['MANUF_COMPID', 'ID'], axis=1) \
        .rename(columns={'ROOT_NAME': 'MANUFACTURER'}) \
        .drop_duplicates()

    sid_vsl_all_features_df.to_csv(SID_PROCESSED, index=False)
    lr_df.to_csv(LR_PROCESSED, index=False)
