import pandas as pd
from src.setup import CHARACTERISTIC, CHARACTERISTIC_CONFLICTS, \
    CONFLICTS_ALL, RESOLVED_ANALYST, CONFLICTS_IGNORED, CONFLICTS_LIKENESS, CONFLICTS_MANUAL_UPDATE

YEAR = 2020.


def f_group_for_analysis(df):
    # Count resolved conflicts by analyst, grouping by month, year, analyst
    df_analyst = df_raw.drop_duplicates(subset='VESSEL_CONFLICT_ID')\
        .groupby(['RESOLVED_MONTH', 'RESOLVED_YEAR', 'RESOLVED_BY'])['ID']\
        .count().reset_index().rename(columns={'ID': 'NUM_PER_ANALYST'})

    # Count all conflicts grouping by created/resolved month/year, conflict status and data feed
    df_all = df_raw.groupby(
        ['CREATED_MONTH', 'CREATED_YEAR', 'RESOLVED_MONTH', 'RESOLVED_YEAR', 'CONFLICT_STATUS', 'DATA_FEED'])[
        'ID'].count().reset_index().rename(columns={'ID': 'COUNT_STATUS_PER_FEED'})

    # Count ignored conflicts grouping by created/resolved month/year, conflict status and data feed
    df_ignored = df_raw.loc[df_raw.CONFLICT_STATUS.isin(['IGNORED', 'IGNORED VALUE'])].groupby(
        ['CREATED_MONTH', 'CREATED_YEAR', 'RESOLVED_MONTH', 'RESOLVED_YEAR', 'DATA_FEED'])[
        'ID'].count().reset_index().rename(columns={'ID': 'NUM_IGNORED'})

    # Count manually updated conflicts grouping by created/resolved month/year, conflict status and data feed
    df_updated = df_raw.loc[df_raw.CONFLICT_STATUS == 'MANUAL UPDATE'].groupby(
        ['CREATED_MONTH', 'CREATED_YEAR', 'RESOLVED_MONTH', 'RESOLVED_YEAR', 'DATA_FEED'])[
        'ID'].count().reset_index().rename(columns={'ID': 'NUM_MANUAL_UPDATE'})

    # Count conflicts resolved under likeness grouping by created/resolved month/year, conflict status and data feed
    df_likeness = df_raw.loc[df_raw.IGNORE_REASON == 'Likeness'].groupby(
        ['CREATED_MONTH', 'CREATED_YEAR', 'RESOLVED_MONTH', 'RESOLVED_YEAR', 'DATA_FEED'])[
        'ID'].count().reset_index().rename(columns={'ID': 'NUM_LIKENESS'})

    return df_analyst, df_all, df_ignored, df_updated, df_likeness


if __name__ == '__main__':
    print(f"Processing {CHARACTERISTIC} data for {int(YEAR)} onwards.")

    df_raw = pd.read_csv(CHARACTERISTIC_CONFLICTS, encoding='cp1252')
    df_analyst_conlicts, df_all_conflicts, df_ignored_conflicts, df_updated_conflicts, df_likeness_conflicts = \
        f_group_for_analysis(df_raw)

    df_analyst_conlicts.to_csv(RESOLVED_ANALYST, index=False)
    df_all_conflicts.to_csv(CONFLICTS_ALL, index=False)
    df_ignored_conflicts.to_csv(CONFLICTS_IGNORED, index=False)
    df_updated_conflicts.to_csv(CONFLICTS_MANUAL_UPDATE, index=False)
    df_likeness_conflicts.to_csv(CONFLICTS_LIKENESS, index=False)
