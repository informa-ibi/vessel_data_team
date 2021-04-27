import pandas as pd
import pylab as pl
import seaborn as sns
import numpy as np
from src.setup import CHARACTERISTIC, CHARACTERISTIC_CONFLICTS, IMAGES, OUTPUT_DIR


YEAR = 2020.


if __name__ == '__main__':
    print(f"Analysing resolved conflict data for {int(YEAR)} where it was ignored, for {CHARACTERISTIC} "
          f"and what was their reasoning.")

    df_raw = pd.read_csv(CHARACTERISTIC_CONFLICTS, encoding='cp1252')

    # Filter data to year of interest
    df = df_raw.loc[df_raw.RESOLVED_YEAR == YEAR]

    df = df.loc[df.CONFLICT_STATUS.isin(['IGNORED', 'IGNORED VALUE'])].replace(np.nan, 'None')

    df_gr = df.reset_index().groupby('IGNORE_REASON')['index'].count().reset_index().sort_values(by='index')

    pl.close('all')
    sns.set_style('darkgrid')

    ax_bar = pl.figure()
    fig = sns.barplot(data=df_gr, x="IGNORE_REASON", y='index', palette='Spectral_r')
    pl.ylabel("No. conflicts", fontsize=11)
    pl.xticks(rotation=90)
    for p in fig.patches:
        fig.annotate(int(p.get_height()),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center',
                     xytext=(0, 5),
                     textcoords='offset points')
    title = ax_bar.suptitle(f'No. of ignored conflicts grouped by ignore reason'
                            f'\n for {CHARACTERISTIC} in {int(YEAR)}', fontsize=12)
    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'count_ignore_reason_{int(YEAR)}.png', dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    df_gr.to_csv(OUTPUT_DIR / f'{CHARACTERISTIC}' / f'count_ignore_reason_{int(YEAR)}.csv', index=False)
