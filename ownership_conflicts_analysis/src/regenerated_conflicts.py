import pandas as pd
from src.setup import CHARACTERISTIC, REG_OWNER_CONFLICTS


YEAR = 2020.


if __name__ == '__main__':
    print(f"Analysing resolved conflict data for {int(YEAR)} where it was regenerated, for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(REG_OWNER_CONFLICTS, encoding='cp1252')

    # Filter data to year of interest
    df = df_raw.loc[(df_raw.RESOLVED_YEAR == YEAR) & (df_raw.IGNORE_REASON == 'Regenerated Conflict')]
    print(f'Number of conflicts for {CHARACTERISTIC} in total for {int(YEAR)} IS {len(df_raw)}.')
    print(f'Number of conflicts for {CHARACTERISTIC} for regenerated conflicts only for {int(YEAR)} IS {len(df)}, '
          f'{round(len(df)/len(df_raw) * 100, 2)}% of the total.')
    analysts_resolving_regen = df.RESOLVED_BY.unique()

