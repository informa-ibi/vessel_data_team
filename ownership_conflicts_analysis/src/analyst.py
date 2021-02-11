import pandas as pd
import numpy as np
import calendar
import pylab as pl
import seaborn as sns
from src.setup import CHARACTERISTIC, RESOLVED_ANALYST, IMAGES


YEAR = 2020.

if __name__ == '__main__':
    print(f"Analysing resolved conflict data for {int(YEAR)} with respect to the analyst who resolved the conflict, "
          f"grouped by month for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(RESOLVED_ANALYST, encoding='cp1252')

    # Filter data to year of interest
    df = df_raw.loc[df_raw.RESOLVED_YEAR == YEAR]

    # Setting up params
    pl.close('all')
    sns.set_style("darkgrid")

    months = np.arange(1., 13.)
    max_conflicts_resolved = max(df.NUM_PER_ANALYST)

    # Figure 1
    df_pivot = df.pivot('RESOLVED_BY', 'RESOLVED_MONTH', 'NUM_PER_ANALYST')
    df_pivot.sort_index(level=0, ascending=True, inplace=True)

    sns.set(font_scale=0.5)
    cmap = pl.get_cmap('Spectral_r', 25)

    ax_heatmap = pl.axes()
    sns.heatmap(df_pivot, annot=True, linewidths=0.4, cmap=cmap, ax=ax_heatmap,
                cbar_kws={'label': 'Count', "shrink": 0.8})
    pl.xlabel("Month", fontsize=11)
    pl.ylabel("Analyst", fontsize=11)
    xlabels = [f'{calendar.month_abbr[int(x + 0.5)]}' for x in ax_heatmap.get_xticks()]
    ax_heatmap.set_xticklabels(xlabels)
    title = ax_heatmap.set_title(f'No. Conflicts Resolved per Month in {int(YEAR)} Grouped by Analyst.', fontsize=12)

    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'heatmap_resolved_by_analyst_per_month_{int(YEAR)}.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    # Figure 2
    sns.set(font_scale=1.5)
    fig_bar, ax_bar = pl.subplots(nrows=4, ncols=3, figsize=(40, 30))

    for ax_bar, month in zip(fig_bar.axes, months):
        df_month = df.loc[df['RESOLVED_MONTH'] == month].sort_values(by='NUM_PER_ANALYST', ascending=False)
        sns.barplot(x='RESOLVED_BY', y='NUM_PER_ANALYST', data=df_month, palette='viridis', ax=ax_bar)

    for i, ax_bar in enumerate(fig_bar.axes):
        month_num = months[i]
        month_abbr = calendar.month_abbr[int(month_num)]
        total_resolved_per_month = df.loc[df.RESOLVED_MONTH == month_num].sum().NUM_PER_ANALYST
        ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=90, fontsize=13)
        ax_bar.set_xlabel('Analyst', fontsize=25)
        ax_bar.set_ylabel('Count', fontsize=25)
        # ax.set_ylim(None, max_conflicts_resolved)  # uncomment this for setting a max limit to compare months
        ax_bar.set_title(f'{month_abbr} (Total: {total_resolved_per_month})', fontsize=30)

    title = fig_bar.suptitle(f'No. Conflicts Resolved per Month in {int(YEAR)} Grouped by Analyst.', fontsize=40)
    fig_bar.tight_layout(rect=[0, 0.03, 1, 0.95])
    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'count_resolved_by_analyst_per_month_{int(YEAR)}.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')
