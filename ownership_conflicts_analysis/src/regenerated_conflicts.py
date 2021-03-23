import pandas as pd
import pylab as pl
import seaborn as sns
import calendar
from src.setup import CHARACTERISTIC, CHARACTERISTIC_CONFLICTS, IMAGES


YEAR = 2020.


if __name__ == '__main__':
    print(f"Analysing resolved conflict data for {int(YEAR)} where it was regenerated, for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(CHARACTERISTIC_CONFLICTS, encoding='cp1252')

    # Filter data to year of interest
    df = df_raw.loc[(df_raw.RESOLVED_YEAR == YEAR) & (df_raw.IGNORE_REASON == 'Regenerated Conflict')]

    df_gr = df.groupby('CREATED_MONTH')['ID'].count().reset_index()

    print(f'Number of conflicts for {CHARACTERISTIC} in total for {int(YEAR)} IS {len(df_raw)}.')
    print(f'Number of conflicts for {CHARACTERISTIC} for regenerated conflicts only for {int(YEAR)} IS {len(df)}, '
          f'{round(len(df)/len(df_raw) * 100, 2)}% of the total.')
    analysts_resolving_regen = df.RESOLVED_BY.unique()

    sns.set_style('darkgrid')
    pl.close('all')

    ax_bar = pl.axes()
    fig = sns.barplot(x='CREATED_MONTH', y='ID', data=df_gr, palette='Blues')
    pl.xlabel("Month", fontsize=11)
    pl.ylabel("Count", fontsize=11)
    xlabels = [f'{calendar.month_abbr[int(x.get_text())]}' for x in ax_bar.get_xticklabels()]
    ax_bar.set_xticklabels(xlabels)
    title = ax_bar.set_title(f'No. Regenerated Conflicts per Month in {int(YEAR)}.', fontsize=12)

    for p in fig.patches:
        fig.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                       textcoords='offset points')

    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'count_regenerated_conflicts_per_month_{int(YEAR)}.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')
