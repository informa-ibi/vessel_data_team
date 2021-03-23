import pandas as pd
import pylab as pl
import seaborn as sns
from src.setup import CHARACTERISTIC, CHARACTERISTIC_CONFLICTS, IMAGES, OUTPUT_DIR


YEAR = 2020.


if __name__ == '__main__':
    print(f"Analysing conflict status by data feed for conflicts created in {int(YEAR)}, for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(CHARACTERISTIC_CONFLICTS, encoding='cp1252')

    df = df_raw.loc[df_raw.CREATED_YEAR == YEAR].groupby(['CONFLICT_STATUS', 'DATA_FEED'])['ID'].count()\
        .reset_index().rename(columns={'ID': 'NO. CONFLICTS'})
    df_pivot = df.pivot(columns='CONFLICT_STATUS', index='DATA_FEED').fillna(0).sort_values(by='DATA_FEED', ascending=False)

    # Setting up params
    pl.close('all')
    sns.set_style("darkgrid")

    fig = df_pivot.plot(kind='barh', stacked=True, legend=False, width=0.85, linewidth=0.5)
    current_handles, current_labels = fig.get_legend_handles_labels()
    new_labels = [label.split(', ')[1].strip(')') for label in current_labels]
    legend = fig.legend(new_labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='x-small')
    legend.set_title('Conflict Status')

    pl.ylabel("Data Feed", fontsize=12)
    pl.xlabel("Count", fontsize=12)
    pl.yticks(fontsize=1)
    pl.yticks(fontsize=6)

    pl.tight_layout(rect=[0, 0.03, 1, 0.95])
    title = fig.set_title(f'Count conflicts by Data Feed and Conflict Status\n for {int(YEAR)}', fontsize=16)
    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'count_conflicts_by_feed_conflict_status_{int(YEAR)}.png',
               dpi=300, bbox_extra_artists=[title, legend], bbox_inches='tight')

    df.to_csv(OUTPUT_DIR / f'{CHARACTERISTIC}' / 'count_conflicts_by_feed_conflict_status.csv', index=False)
