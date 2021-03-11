import pandas as pd
import numpy as np
from math import ceil
from datetime import datetime
import pylab as pl
import seaborn as sns
from src.setup import CHARACTERISTIC, CONFLICTS_ALL, IMAGES


YEAR = 2020.


def months_to_resolve(created_month, created_year, resolved_month, resolved_year):
    d1 = datetime(int(resolved_year), int(resolved_month), 1)
    d2 = datetime(int(created_year), int(created_month), 1)
    return (d1.year - d2.year) * 12 + d1.month - d2.month


if __name__ == '__main__':
    print(f"Analysing all conflict data for {int(YEAR)}, "
          f"grouped by month for {CHARACTERISTIC}.")

    df_raw = pd.read_csv(CONFLICTS_ALL, encoding='cp1252', dtype={'CREATED_MONTH': float,
                                                                  'CREATED_YEAR': float})

    # Filter data to year of interest
    df = df_raw.loc[(df_raw.RESOLVED_YEAR == YEAR) & (df_raw.DATA_FEED.notnull())]
    df['MONTHS_TO_RESOLVE'] = df.apply(lambda row: pd.Series(months_to_resolve(row['CREATED_MONTH'],
                                                                               row['CREATED_YEAR'],
                                                                               row['RESOLVED_MONTH'],
                                                                               row['RESOLVED_YEAR'])), axis=1)

    all_feeds = sorted(df.DATA_FEED.unique().tolist())
    p_and_i = sorted([feed for feed in all_feeds if 'PI_' in feed])
    iacs = ['AB', 'BV', 'CS', 'HV', 'IR', 'KR', 'LR', 'NK', 'NG', 'PR', 'RINA', 'RS']
    other = [feed for feed in all_feeds if (feed not in iacs) & (feed not in p_and_i)]

    # Setting up params
    pl.close('all')
    sns.set_style("darkgrid")

    months = np.arange(1., 13.)
    months_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    created_resolved = ['Number Conflicts Created', 'Number Conflicts Resolved']

    # Figure 1 - IACS Class Society
    df_iacs = df.loc[df.DATA_FEED.isin(iacs)]
    df_iacs_created = df_iacs.groupby(['CREATED_MONTH', 'CREATED_YEAR', 'DATA_FEED'])\
        .sum().COUNT_STATUS_PER_FEED.reset_index().sort_values(by='DATA_FEED')
    df_iacs_resolved = df_iacs.groupby(['RESOLVED_MONTH', 'RESOLVED_YEAR', 'DATA_FEED'])\
        .sum().COUNT_STATUS_PER_FEED.reset_index().sort_values(by='DATA_FEED')

    fig_line_iacs, ax_line_iacs = pl.subplots(nrows=1, ncols=2, figsize=(30, 15))
    sns.lineplot(x='CREATED_MONTH', y='COUNT_STATUS_PER_FEED', hue='DATA_FEED', data=df_iacs_created,
                 palette='Spectral', ci=None, linewidth=1.5, ax=ax_line_iacs[0])\
        .set(xticks=months, xticklabels=months_abbr)
    sns.lineplot(x='RESOLVED_MONTH', y='COUNT_STATUS_PER_FEED', hue='DATA_FEED', data=df_iacs_resolved,
                 palette='Spectral', ci=None, linewidth=1.5, ax=ax_line_iacs[1])\
        .set(xticks=months, xticklabels=months_abbr)

    for i, ax_line_iacs in enumerate(fig_line_iacs.axes):
        ax_line_iacs.set_xlabel('Month', fontsize=15)
        ax_line_iacs.set_ylabel('Count', fontsize=15)
        ax_line_iacs.set_ylim(0, ceil(max(df_iacs_created.COUNT_STATUS_PER_FEED)))
        ax_line_iacs.set_xlim(1, 12)
        ax_line_iacs.set_title(f'{created_resolved[i]}', fontsize=18)
        ax_line_iacs.legend().texts[0].set_text("Data Feed")

    title = fig_line_iacs.suptitle(f'No. Conflicts Created and Resolved each Month in {int(YEAR)} '
                                   f'\nfor IACS Class Societies.', fontsize=20)
    fig_line_iacs.tight_layout(rect=[0, 0.03, 1, 0.95])
    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'line_conflicts_created_resolved_per_month_{int(YEAR)}_IACS.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    # Figure 2 - P&I Clubs
    df_p_and_i = df.loc[df.DATA_FEED.isin(p_and_i)]
    df_p_and_i_created = df_p_and_i.groupby(['CREATED_MONTH', 'CREATED_YEAR', 'DATA_FEED'])\
        .sum().COUNT_STATUS_PER_FEED.reset_index().sort_values(by='DATA_FEED')
    df_p_and_i_resolved = df_p_and_i.groupby(['RESOLVED_MONTH', 'RESOLVED_YEAR', 'DATA_FEED'])\
        .sum().COUNT_STATUS_PER_FEED.reset_index().sort_values(by='DATA_FEED')

    fig_line_p_and_i, ax_line_p_and_i = pl.subplots(nrows=1, ncols=2, figsize=(30, 15))
    sns.lineplot(x='CREATED_MONTH', y='COUNT_STATUS_PER_FEED', hue='DATA_FEED', data=df_p_and_i_created,
                 palette='Spectral', ci=None, linewidth=1.5, ax=ax_line_p_and_i[0])\
        .set(xticks=months, xticklabels=months_abbr)
    sns.lineplot(x='RESOLVED_MONTH', y='COUNT_STATUS_PER_FEED', hue='DATA_FEED', data=df_p_and_i_resolved,
                 palette='Spectral', ci=None, linewidth=1.5, ax=ax_line_p_and_i[1])\
        .set(xticks=months, xticklabels=months_abbr)

    for i, ax_line_p_and_i in enumerate(fig_line_p_and_i.axes):
        ax_line_p_and_i.set_xlabel('Month', fontsize=15)
        ax_line_p_and_i.set_ylabel('Count', fontsize=15)
        ax_line_p_and_i.set_ylim(0, ceil(max(df_p_and_i_created.COUNT_STATUS_PER_FEED)))
        ax_line_p_and_i.set_xlim(1, 12)
        ax_line_p_and_i.set_title(f'{created_resolved[i]}', fontsize=18)
        ax_line_p_and_i.legend().texts[0].set_text("Data Feed")

    title = fig_line_p_and_i.suptitle(f'No. Conflicts Created and Resolved each Month in {int(YEAR)} '
                                      f'\nfor P&I Clubs.', fontsize=20)
    fig_line_p_and_i.tight_layout(rect=[0, 0.03, 1, 0.95])
    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'line_conflicts_created_resolved_per_month_{int(YEAR)}_PandI.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    # Figure  - Non IACS or P&I
    df_other = df.loc[df.DATA_FEED.isin(other)]
    df_other_created = df_other.groupby(['CREATED_MONTH', 'CREATED_YEAR', 'DATA_FEED'])\
        .sum().COUNT_STATUS_PER_FEED.reset_index().sort_values(by='DATA_FEED')
    df_other_resolved = df_other.groupby(['RESOLVED_MONTH', 'RESOLVED_YEAR', 'DATA_FEED'])\
        .sum().COUNT_STATUS_PER_FEED.reset_index().sort_values(by='DATA_FEED')

    fig_line_other, ax_line_other = pl.subplots(nrows=1, ncols=2, figsize=(30, 15))
    sns.lineplot(x='CREATED_MONTH', y='COUNT_STATUS_PER_FEED', hue='DATA_FEED', data=df_other_created,
                 palette='Spectral', ci=None, linewidth=1.5, ax=ax_line_other[0])\
        .set(xticks=months, xticklabels=months_abbr)
    sns.lineplot(x='RESOLVED_MONTH', y='COUNT_STATUS_PER_FEED', hue='DATA_FEED', data=df_other_resolved,
                 palette='Spectral', ci=None, linewidth=1.5, ax=ax_line_other[1])\
        .set(xticks=months, xticklabels=months_abbr)

    for i, ax_line_other in enumerate(fig_line_other.axes):
        ax_line_other.set_xlabel('Month', fontsize=15)
        ax_line_other.set_ylabel('Count', fontsize=15)
        ax_line_other.set_ylim(0, ceil(max(df_other_created.COUNT_STATUS_PER_FEED)))
        ax_line_other.set_xlim(1, 12)
        ax_line_other.set_title(f'{created_resolved[i]}', fontsize=18)
        ax_line_other.legend().texts[0].set_text("Data Feed")

    title = fig_line_other.suptitle(f'No. Conflicts Created and Resolved each Month in {int(YEAR)} '
                                    f'\nfor non-IACS and non-P&I Clubs.', fontsize=20)
    fig_line_other.tight_layout(rect=[0, 0.03, 1, 0.95])
    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'line_conflicts_created_resolved_per_month_{int(YEAR)}_other.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')
