import pandas as pd
from src.setup import CHARACTERISTIC_CONFLICTS, CHARACTERISTIC, OUTPUT_DIR, IMAGES
from fuzzywuzzy import process
import seaborn as sns
import pylab as pl

YEAR = 2020.

cols_to_keep = [
    'VESSEL_ID',
    'DATA_FEED',
    'SOURCE_VALUE',
    'DB_VALUE',
    'RESOLVED_DATE',
    'CREATED_DATE',
    'UPDATED_DATE',
    'RESOLVED_BY',
    'CONFLICT_STATUS',
    'IGNORE_REASON',
]

ignore_reasons_where_correct = [
    'Likeness',
    'Manual Update',
]

sns.set_style('darkgrid')


def get_similar_source(row, sources, match_value=55.):
    ratios = process.extract(row.SOURCE_VALUE, sources)
    return str(sorted([source[0] for source in ratios if float(source[1]) >= match_value]))


def bar_feed_item(df, feed_type, order, feed_type_str):
    pl.close('all')
    df = df.loc[df['Data Feed'].isin(feed_type)]
    ax_bar = pl.axes()
    fig = sns.barplot(x='Data Feed', y='Count', data=df, palette='Blues')

    pl.xlabel("Data Feed", fontsize=11)
    pl.ylabel("Count", fontsize=11)
    title = ax_bar.set_title(f'Count Conflicts Created {order} by Data Feed for {feed_type_str}\n {int(YEAR)} onwards.',
                             fontsize=12)
    ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=90, fontsize=10)

    for p in fig.patches:
        fig.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                     textcoords='offset points')

    pl.savefig(IMAGES / f'{CHARACTERISTIC}' / f'count_{order}_data_feed_item_{feed_type_str}_{int(YEAR)}_onwards.png',
               dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    df.to_csv(OUTPUT_DIR / f'{CHARACTERISTIC}' /
              f'count_{order}_data_feed_item_{feed_type_str}_{int(YEAR)}_onwards.csv', index=False)


if __name__ == '__main__':
    print(f"Processing conflicts for {CHARACTERISTIC} for {int(YEAR)} onwards.")
    # Question: Which is the first feed to report correct value?

    df_conflicts_all = pd.read_csv(CHARACTERISTIC_CONFLICTS, encoding='cp1252')
    # Filter out pending conflicts, and only conflicts to the characteristic
    # of interest (extra check as should already be the case)
    df_conflicts_resolved = df_conflicts_all.loc[(df_conflicts_all.CONFLICT_STATUS != 'PENDING')
                                                 & (df_conflicts_all.DATA_ITEM_NAME == CHARACTERISTIC)][cols_to_keep]

    # Filter to conflicts raised that contained correct information
    df_correct_conflicts = df_conflicts_resolved.loc[
        (df_conflicts_resolved.IGNORE_REASON.isin(ignore_reasons_where_correct))
        | (df_conflicts_resolved.IGNORE_REASON.isnull())]

    # Formatting columns
    df_correct_conflicts['CREATED_DATE'] = pd.to_datetime(df_correct_conflicts['CREATED_DATE'])
    df_correct_conflicts['RESOLVED_DATE'] = pd.to_datetime(df_correct_conflicts['RESOLVED_DATE'])
    remove_words = ['LIMITED', 'LTD', 'SA']
    pat = r'\b(?:{})\b'.format('|'.join(remove_words))
    df_correct_conflicts['SOURCE_VALUE'] = df_correct_conflicts['SOURCE_VALUE'].str.upper().str.replace(pat, '') \
        .str.replace('.', '').str.replace(',', '').str.replace('/', '').str.replace('&AMP;', '&').str.replace('|', '') \
        .str.replace('  ', ' ') \
        .str.replace('SA', '').str.replace('SPF', '').str.replace('AS', '')

    # Dictionaries with values for each feed
    all_feeds = sorted(df_correct_conflicts.DATA_FEED.unique().tolist())
    dict_data_first_feeds = {el: 0 for el in all_feeds}
    dict_data_later_feeds = dict_data_first_feeds.copy()

    vessels = df_correct_conflicts.VESSEL_ID.unique().tolist()

    for vessel in vessels:
        df_original = df_correct_conflicts.loc[df_correct_conflicts.VESSEL_ID == vessel]

        df_vessel = df_original.sort_values(by='CREATED_DATE') \
            .drop_duplicates(subset=['DATA_FEED', 'DB_VALUE']) \
            .drop_duplicates(subset=['DATA_FEED', 'SOURCE_VALUE'])

        source_values = df_vessel.SOURCE_VALUE.unique().tolist()
        df_vessel['match_values'] = df_vessel.apply(lambda x: get_similar_source(x, source_values), axis=1)

        df_vessel_gr = df_vessel.groupby('match_values')
        match_values = df_vessel.match_values.unique().tolist()
        for sv in match_values:
            df_sv = df_vessel_gr.get_group(sv)
            feeds = df_sv.DATA_FEED.unique()

            dt_first_conflict = sorted(df_sv.CREATED_DATE.unique())[0]
            first_feeds = df_sv.loc[df_sv.CREATED_DATE == dt_first_conflict].DATA_FEED.unique().tolist()
            for f_feed in first_feeds:
                dict_data_first_feeds[f_feed] += 1

            later_feeds = [item for item in feeds if item not in first_feeds]
            for l_feed in later_feeds:
                dict_data_later_feeds[l_feed] += 1

            # if vessel in [12607306]:
            #     print(df_vessel[['VESSEL_ID', 'DATA_FEED', 'SOURCE_VALUE', 'DB_VALUE', 'CREATED_DATE',
            #     'CONFLICT_STATUS', 'IGNORE_REASON', 'match_values']])
            #     print(df_vessel.match_values.values)
            #     print('First feeds:', first_feeds)
            #     print('Later feeds:', later_feeds)
            #     print('\n')

    p_and_i = sorted([feed for feed in all_feeds if 'PI_' in feed])
    iacs = ['AB', 'BV', 'CS', 'HV', 'IR', 'KR', 'LR', 'NK', 'NG', 'PR', 'RINA', 'RS']
    other = [feed for feed in all_feeds if (feed not in iacs) & (feed not in p_and_i)]

    df_data_first_feeds = pd.DataFrame(dict_data_first_feeds.items(), columns=['Data Feed', 'Count'])
    df_data_later_feeds = pd.DataFrame(dict_data_later_feeds.items(), columns=['Data Feed', 'Count'])

    bar_feed_item(df_data_first_feeds, iacs, 'first', 'ICAS')
    bar_feed_item(df_data_later_feeds, iacs, 'later', 'ICAS')
    bar_feed_item(df_data_first_feeds, p_and_i, 'first', 'P&I')
    bar_feed_item(df_data_later_feeds, p_and_i, 'later', 'P&I')
    bar_feed_item(df_data_first_feeds, other, 'first', 'other')
    bar_feed_item(df_data_later_feeds, other, 'later', 'other')

