import pandas as pd
import numpy as np
import pylab as pl
import seaborn as sns
from src.setup import LINKED_CONFLICTS, NOT_LINKED_CONFLICTS, IMAGES


YEAR = 2020.


def stack_bar_feed_item(df, feed_type):
    fig = df.plot(kind='bar', stacked=True, legend=False, width=0.85, linewidth=0.5)

    current_handles, current_labels = fig.get_legend_handles_labels()
    new_labels = [label.split(', ')[1].strip(')') for label in current_labels]
    legend = fig.legend(new_labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='x-small')
    legend.set_title('Data Item')
    pl.xlabel("Data Feed", fontsize=12)
    pl.ylabel("Count", fontsize=12)
    pl.xticks(fontsize=6, rotation=90)
    pl.tight_layout(rect=[0, 0.03, 1, 0.95])
    title = fig.set_title(f'Count conflicts grouped by data item for {feed_type} feeds', fontsize=16)
    pl.savefig(IMAGES / f'stacked_data_feed_data_items_{feed_type}.png',
               dpi=300, bbox_extra_artists=[title, legend], bbox_inches='tight')


if __name__ == '__main__':
    print(f"Analysing lag between Name and Flag changes on Registered Owner for {int(YEAR)} onwards.")

    df_conflicts_all = pd.read_csv(NOT_LINKED_CONFLICTS)
    df_conflicts_proc = pd.read_csv(LINKED_CONFLICTS)

    # Setting up params for viz
    pl.close('all')
    sns.set_style("darkgrid")

    # 1/ Grouping the data into bins for lag and plotting
    step = 7  # i.e. how many weeks
    max_group_limit = step * 15
    upper_bound_for_cut = max_group_limit + step
    upper_bound_plus_cat_val = max_group_limit + 1
    df_conflicts_proc['lag_gr'] = pd.cut(df_conflicts_proc.lag, np.arange(0, upper_bound_for_cut, step))
    df_conflicts_proc['lag_gr'] = df_conflicts_proc['lag_gr'].cat.add_categories(['0', f'{upper_bound_plus_cat_val}+'])
    df_conflicts_proc.loc[df_conflicts_proc.lag == 0, 'lag_gr'] = '0'
    df_conflicts_proc.loc[df_conflicts_proc.lag > max_group_limit-step, 'lag_gr'] = f'{upper_bound_plus_cat_val}+'

    df_conflicts_proc_gr = df_conflicts_proc.groupby('lag_gr').count().reset_index()[['lag_gr', 'vsl_id']]\
        .rename(columns={'vsl_id': 'No. Ownership Changes'})
    orig_lag_gr_categories = df_conflicts_proc['lag_gr'].cat.categories.tolist()
    orig_lag_gr_categories.insert(0, orig_lag_gr_categories.pop(orig_lag_gr_categories.index('0')))
    df_conflicts_proc_gr = df_conflicts_proc_gr.set_index('lag_gr').loc[orig_lag_gr_categories].reset_index()

    ax_bar = pl.figure()
    sns.barplot(data=df_conflicts_proc_gr, x="lag_gr", y='No. Ownership Changes', palette='Spectral_r', order=orig_lag_gr_categories)
    pl.xlabel("Lag (days)", fontsize=11)
    pl.xticks(rotation=90)
    title = ax_bar.suptitle(f'No. of vessels grouped by lag (days)\n from initial data item conflict to final data '
                             f'item conflict',  fontsize=12)
    pl.savefig(IMAGES / f'bar_conflicts_lag{int(YEAR)}.png', dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    # 2/ Understand order of data item changes e.g. how many are flag before reg owner, name before reg owner
    df_conflicts_proc.loc[df_conflicts_proc.flag_date <= df_conflicts_proc.reg_owner_date, 'flag_after_reg_owner'] = 0
    df_conflicts_proc.loc[df_conflicts_proc.flag_date > df_conflicts_proc.reg_owner_date, 'flag_after_reg_owner'] = 1
    df_conflicts_proc.loc[df_conflicts_proc.vsl_name_date <= df_conflicts_proc.reg_owner_date, 'name_after_reg_owner'] = 0
    df_conflicts_proc.loc[df_conflicts_proc.vsl_name_date > df_conflicts_proc.reg_owner_date, 'name_after_reg_owner'] = 1

    dict_order_conflicts_raised = {
        'flag and name \nafter reg owner': len(df_conflicts_proc.loc[(df_conflicts_proc.flag_after_reg_owner == 1) &
                                                                     (df_conflicts_proc.name_after_reg_owner == 1)]),
        'flag and name\nnot after reg owner': len(df_conflicts_proc.loc[(df_conflicts_proc.flag_after_reg_owner == 0) &
                                                                        (df_conflicts_proc.name_after_reg_owner == 0)]),
        'flag only \nafter reg owner': len(df_conflicts_proc.loc[(df_conflicts_proc.flag_after_reg_owner == 1) &
                                                                 (df_conflicts_proc.name_after_reg_owner == 0)]),
        'name only \nafter reg owner': len(df_conflicts_proc.loc[(df_conflicts_proc.flag_after_reg_owner == 0) &
                                                                 (df_conflicts_proc.name_after_reg_owner == 1)])
                 }

    df_order_conflicts_raised = pd.DataFrame([dict_order_conflicts_raised]).stack().reset_index()\
        .rename(columns={'level_1': 'Order Data Item Conflicts Created', 0: 'No. Ownership Changes'})

    ax_bar_order = pl.figure()
    sns.barplot(data=df_order_conflicts_raised, x="Order Data Item Conflicts Created", y='No. Ownership Changes',
                palette='Spectral_r')
    title = ax_bar_order.suptitle(f'No. ownership changes grouped by order of change',  fontsize=12)
    pl.savefig(IMAGES / f'bar_conflicts_order{int(YEAR)}.png', dpi=300, bbox_extra_artists=[title], bbox_inches='tight')

    # 3/ Data items by data feeds - grouped by IACS, P and I, AIS, and other
    all_feeds = sorted(df_conflicts_all.DATA_FEED.unique().tolist())

    iacs = ['AB', 'BV', 'CS', 'HV', 'IR', 'KR', 'LR', 'NK', 'NG', 'PR', 'RINA', 'RS']
    df_iacs = df_conflicts_all.loc[df_conflicts_all.DATA_FEED.isin(iacs)]
    df_iacs_gr_pivot = df_iacs.groupby(['DATA_ITEM_NAME', 'DATA_FEED'])['VESSEL_ID'].count().reset_index()\
        .rename(columns={'VESSEL_ID': 'No. Conflicts'}).pivot(columns='DATA_ITEM_NAME', index='DATA_FEED').fillna(0)
    stack_bar_feed_item(df_iacs_gr_pivot, 'IACS')  # IACS plot

    p_and_i = sorted([feed for feed in all_feeds if 'PI_' in feed])
    df_pandi = df_conflicts_all.loc[df_conflicts_all.DATA_FEED.isin(p_and_i)]
    df_pandi_gr_pivot = df_pandi.groupby(['DATA_ITEM_NAME', 'DATA_FEED'])['VESSEL_ID'].count().reset_index()\
        .rename(columns={'VESSEL_ID': 'No. Conflicts'}).pivot(columns='DATA_ITEM_NAME', index='DATA_FEED').fillna(0)
    stack_bar_feed_item(df_pandi_gr_pivot, 'PandI')  # AIS plot

    ais = sorted([feed for feed in all_feeds if 'AIS_' in feed])
    df_ais = df_conflicts_all.loc[df_conflicts_all.DATA_FEED.isin(ais)]
    df_ais_gr_pivot = df_ais.groupby(['DATA_ITEM_NAME', 'DATA_FEED'])['VESSEL_ID'].count().reset_index()\
        .rename(columns={'VESSEL_ID': 'No. Conflicts'}).pivot(columns='DATA_ITEM_NAME', index='DATA_FEED').fillna(0)
    stack_bar_feed_item(df_ais_gr_pivot, 'AIS')  # AIS plot

    other = [feed for feed in all_feeds if (feed not in iacs) & (feed not in p_and_i) & (feed not in ais)]
    df_other = df_conflicts_all.loc[df_conflicts_all.DATA_FEED.isin(other)]
    df_other_gr_pivot = df_other.groupby(['DATA_ITEM_NAME', 'DATA_FEED'])['VESSEL_ID'].count().reset_index()\
        .rename(columns={'VESSEL_ID': 'No. Conflicts'}).pivot(columns='DATA_ITEM_NAME', index='DATA_FEED').fillna(0)
    stack_bar_feed_item(df_other_gr_pivot, 'other')  # AIS plot

    # 4/ Number vessel with ownership changed and only with flag and name change
    new_df = df_conflicts_all.copy()[['VESSEL_ID', 'DATA_ITEM_NAME']]
    test = new_df.groupby('VESSEL_ID')['DATA_ITEM_NAME'].nunique().reset_index()
    d = {'One Data Item Only': 0,
         'Flag and Reg Owner': 0,
         'Flag and Vessel Name': 0,
         'Vessel Name and Reg Owner': 0,
         'Flag, Vessel Name and Reg Owner': 0}
    ships = new_df.VESSEL_ID.unique().tolist()
    for ship in ships:
        vsl_data_items = new_df.loc[new_df.VESSEL_ID == ship].DATA_ITEM_NAME.unique().tolist()
        if len(vsl_data_items) == 1:
            d['One Data Item Only'] += 1
        elif len(vsl_data_items) == 3:
            d['Flag, Vessel Name and Reg Owner'] += 1
        else:
            if sorted(vsl_data_items) == ['FLAG', 'VSL NAME']:
                d['Flag and Vessel Name'] += 1
            elif sorted(vsl_data_items) == ['FLAG', 'REG_OWNER']:
                d['Flag and Reg Owner'] += 1
            elif sorted(vsl_data_items) == ['REG_OWNER', 'VSL NAME']:
                d['Vessel Name and Reg Owner'] += 1


