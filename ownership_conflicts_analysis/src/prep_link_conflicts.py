import pandas as pd
from src.setup import REG_OWNER_CONFLICTS, FLAG_CONFLICTS, VSL_NAME_CONFLICTS, LINKED_CONFLICTS, NOT_LINKED_CONFLICTS


YEAR = 2020.


def prep_data(df):
    df_prep = df.loc[df.CONFLICT_STATUS.isin(['AUTOMATED UPDATE', 'MANUAL UPDATE'])][cols_to_keep]
    df_prep['CREATED_DATE'] = pd.to_datetime(df_prep.CREATED_DATE)
    return df_prep


def deduplicate_vessel_conflicts(df):
    # Drop duplicates based on the DB value for each data item, then concat
    name_changes_for_vsl = df.loc[df.DATA_ITEM_NAME == 'VSL NAME'].drop_duplicates(['DB_VALUE'])
    flag_changes_for_vsl = df.loc[df.DATA_ITEM_NAME == 'FLAG'].drop_duplicates(['DB_VALUE'])
    owner_changes_for_vsl = df.loc[df.DATA_ITEM_NAME == 'REG_OWNER'].drop_duplicates(['DB_VALUE'])
    deduplicated_df = pd.concat([name_changes_for_vsl, flag_changes_for_vsl, owner_changes_for_vsl])\
        .sort_values(by='CREATED_DATE').reset_index()
    return deduplicated_df


def append_linked_conflicts(vessel_of_interest, df_vessel, df_to_append_to):
    def get_conflict_date_feed(df, date_item):
        date = df.loc[df.DATA_ITEM_NAME == date_item].CREATED_DATE.values[0]
        feed = df.loc[df.DATA_ITEM_NAME == date_item].DATA_FEED.values[0]
        return date, feed

    dict_for_df['vsl_id'] = vessel_of_interest
    dict_for_df['reg_owner_date'] = get_conflict_date_feed(df_vessel, 'REG_OWNER')[0]
    dict_for_df['reg_owner_feed'] = get_conflict_date_feed(df_vessel, 'REG_OWNER')[1]
    dict_for_df['flag_date'] = get_conflict_date_feed(df_vessel, 'FLAG')[0]
    dict_for_df['flag_feed'] = get_conflict_date_feed(df_vessel, 'FLAG')[1]
    dict_for_df['vsl_name_date'] = get_conflict_date_feed(df_vessel, 'VSL NAME')[0]
    dict_for_df['vsl_name_feed'] = get_conflict_date_feed(df_vessel, 'VSL NAME')[1]

    df_to_append_to = df_to_append_to.append(dict_for_df, ignore_index=True)
    return df_to_append_to


def get_conflict_lag(row):
    max_date = max([row.reg_owner_date, row.flag_date, row.vsl_name_date])
    min_date = min([row.reg_owner_date, row.flag_date, row.vsl_name_date])
    return float((max_date - min_date).days)


cols_to_keep = [
    'SOURCE_VALUE',
    'DB_VALUE',
    'CREATED_DATE',
    # 'RESOLVED_DATE',
    # 'UPDATED_DATE',
    'VESSEL_ID',
    'DATA_ITEM_NAME',
    # 'CONFLICT_STATUS',
    'DATA_FEED',
    # 'IGNORE_REASON',
]


headers = [
    'vsl_id',
    'reg_owner_date',
    'reg_owner_feed',
    'flag_date',
    'flag_feed',
    'vsl_name_date',
    'vsl_name_feed',
]


dict_for_df = {header: None for header in headers}

data_items = ['REG_OWNER', 'FLAG', 'VSL NAME']

if __name__ == '__main__':
    print(f"Processing lag between Name and Flag changes on Registered Owner for {int(YEAR)} onwards.")

    df_reg_owner = prep_data(pd.read_csv(REG_OWNER_CONFLICTS, encoding='cp1252'))
    df_flag = prep_data(pd.read_csv(FLAG_CONFLICTS, encoding='cp1252'))
    df_vsl_name = prep_data(pd.read_csv(VSL_NAME_CONFLICTS, encoding='cp1252'))
    df_conflicts_all = pd.concat([df_reg_owner, df_flag, df_vsl_name]).sort_values(by='CREATED_DATE')

    list_vessels = df_conflicts_all.VESSEL_ID.unique().tolist()
    list_vessels_without_all_changes = []
    list_vessel_multple_changes = []

    df_conflicts_proc = pd.DataFrame(columns=headers)
    for i, vessel in enumerate(list_vessels):
        df_for_vessel = deduplicate_vessel_conflicts(df_conflicts_all.loc[df_conflicts_all.VESSEL_ID == vessel])
        conflicting_data_items = df_for_vessel.DATA_ITEM_NAME.unique()
        if len(conflicting_data_items) == 3:
            if len(df_for_vessel) == 3:
                df_conflicts_proc = append_linked_conflicts(vessel, df_for_vessel, df_conflicts_proc)
            else:
                df_for_vessel['delta'] = abs(
                    (df_for_vessel['CREATED_DATE'] - df_for_vessel['CREATED_DATE'].shift(-1)).dt.days.fillna(0.))
                list_df_indexes = df_for_vessel.index.values
                starting_date = df_for_vessel.CREATED_DATE.values[0]
                list_data_items_changed = []
                index_to_start_append_from = 0
                for i in list_df_indexes:
                    df_sub = df_for_vessel.iloc[index_to_start_append_from::]
                    row = df_for_vessel.iloc[i]
                    list_data_items_changed.append(row.DATA_ITEM_NAME)
                    if row.delta <= 31.:
                        if sorted(set(data_items)) == sorted(set(list_data_items_changed)):
                            df_conflicts_proc = append_linked_conflicts(vessel, df_sub, df_conflicts_proc)
                            index_to_start_append_from = i + 1
                            list_data_items_changed = []
                    else:
                        if sorted(set(data_items)) == sorted(set(list_data_items_changed)):
                            df_conflicts_proc = append_linked_conflicts(vessel, df_sub, df_conflicts_proc)
                            list_data_items_changed = []
                        else:
                            index_to_start_append_from = i + 1
                            list_data_items_changed = []
                            continue
                list_vessel_multple_changes.append(vessel)
        else:
            list_vessels_without_all_changes.append(vessel)

    df_conflicts_proc['lag'] = df_conflicts_proc.apply(get_conflict_lag, axis=1)
    # 226116 ownership changed to unknown # 367590  # 12930131 # 11040453 # 367590 dup row # 11102495 # 12881568 # 11151624  # 278601  # 307979
    df_conflicts_proc.to_csv(LINKED_CONFLICTS, index=False)
    df_conflicts_all.to_csv(NOT_LINKED_CONFLICTS, index=False)
