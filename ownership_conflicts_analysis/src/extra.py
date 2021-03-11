import pandas as pd
import calendar
import pylab as pl
import seaborn as sns
from src.setup import CHARACTERISTIC, REG_OWNER_CONFLICTS


YEAR = 2020.


if __name__ == '__main__':
    print(f"Analysing resolved conflict data for {int(YEAR)} where it was ignored, for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(REG_OWNER_CONFLICTS, encoding='cp1252')

    df = df_raw.groupby(['CONFLICT_STATUS', 'DATA_FEED'])['ID'].count().reset_index().rename(columns={'ID': 'NO. CONFLICTS'})
    df_pivot = df.pivot(columns='CONFLICT_STATUS', index='DATA_FEED').fillna(0)

    # Setting up params
    pl.close('all')
    sns.set_style("darkgrid")

    fig = df_pivot.plot(kind='bar', stacked=True, legend=False, width=0.85, linewidth=0.5)

    current_handles, current_labels = fig.get_legend_handles_labels()
    new_labels = [label.split(', ')[1].strip(')') for label in current_labels]
    legend = fig.legend(new_labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='x-small')
    legend.set_title('Months to Resolve')

    # pl.xlabel("Data Feed", fontsize=12)
    # pl.ylabel("Count", fontsize=12)
    # pl.xticks(fontsize=4, rotation=90)

    pl.tight_layout(rect=[0, 0.03, 1, 0.95])
    title = fig.set_title(f'', fontsize=16)

