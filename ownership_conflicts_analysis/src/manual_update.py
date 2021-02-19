import pandas as pd
import numpy as np
import calendar
from datetime import datetime
import pylab as pl
import seaborn as sns
from src.setup import CHARACTERISTIC, CONFLICTS_MANUAL_UPDATE, IMAGES


YEAR = 2020.


def months_to_resolve(created_month, created_year, resolved_month, resolved_year):
    d1 = datetime(int(resolved_year), int(resolved_month), 1)
    d2 = datetime(int(created_year), int(created_month), 1)
    return (d1.year - d2.year) * 12 + d1.month - d2.month


if __name__ == '__main__':
    print(f"Analysing resolved conflict data for {int(YEAR)} where it was resolved under manual update"
          f", for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(CONFLICTS_MANUAL_UPDATE, encoding='cp1252')

    # Filter data to year of interest
    df = df_raw.loc[df_raw.RESOLVED_YEAR == YEAR]
    df['MONTHS_TO_RESOLVE'] = df.apply(lambda row: pd.Series(months_to_resolve(row['CREATED_MONTH'],
                                                                               row['CREATED_YEAR'],
                                                                               row['RESOLVED_MONTH'],
                                                                               row['RESOLVED_YEAR'])), axis=1)

    # Setting up params
    pl.close('all')
    sns.set_style("darkgrid")

    months = np.arange(1., 13.)

    # Figure 1
    for month in months:
        df_created_month = df.loc[(df.CREATED_MONTH == int(month)) &
                                  (df.CREATED_YEAR == YEAR)][['DATA_FEED', 'NUM_MANUAL_UPDATE', 'MONTHS_TO_RESOLVE']]

        df_created_month_pivot = df_created_month.pivot(columns='MONTHS_TO_RESOLVE', index='DATA_FEED').fillna(0)
        fig = df_created_month_pivot.plot(kind='bar', stacked=True, legend=False, width=0.85, linewidth=0.5)

        current_handles, current_labels = fig.get_legend_handles_labels()
        new_labels = [label.split(', ')[1].strip(')') for label in current_labels]
        legend = fig.legend(new_labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='x-small')
        legend.set_title('Months to Resolve')

        pl.xlabel("Data Feed", fontsize=12)
        pl.ylabel("Count", fontsize=12)
        pl.xticks(fontsize=4, rotation=90)

        pl.tight_layout(rect=[0, 0.03, 1, 0.95])
        title = fig.set_title(f'No. Conflicts Resolved under Manual Update per Data Feed, '
                              f'Grouped by Months Taken to Resolve'
                              f'\nfor Conflicts Created in {calendar.month_abbr[int(month)]} {int(YEAR)}', fontsize=16)
        pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'count_manual_update_by_feed_month_to_resolve_{int(month)}_{int(YEAR)}.png',
                   dpi=300, bbox_extra_artists=[title, legend], bbox_inches='tight')
