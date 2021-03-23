from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'datasets'
INPUT_DIR = DATA_DIR / 'input'
PREPROCESSED_DIR = DATA_DIR / 'preprocessed'
OUTPUT_DIR = DATA_DIR / 'output'
IMAGES = Path(__file__).parent.parent / 'images'

REG_OWNER_CONFLICTS = INPUT_DIR / 'REG_OWNER_conflicts_2020.csv'
FLAG_CONFLICTS = INPUT_DIR / 'FLAG_conflicts_2020.csv'
VSL_NAME_CONFLICTS = INPUT_DIR / 'VSL_NAME_conflicts_2020.csv'

CHARACTERISTIC = 'REG_OWNER'
PROC_CHAR_DIR = PREPROCESSED_DIR / f'{CHARACTERISTIC}'

if CHARACTERISTIC == 'REG_OWNER':
    CHARACTERISTIC_CONFLICTS = REG_OWNER_CONFLICTS
    CONFLICTS_ALL = PROC_CHAR_DIR / 'count_conflicts_grouped_by_month_year_feed_status.csv'
    RESOLVED_ANALYST = PROC_CHAR_DIR / 'count_resolved_conflicts_grouped_by_month_year_analyst.csv'
    CONFLICTS_IGNORED = PROC_CHAR_DIR / 'count_ignored_grouped_by_month_year_feed.csv'
    CONFLICTS_LIKENESS = PROC_CHAR_DIR / 'count_likeness_grouped_by_month_year_feed.csv'
    CONFLICTS_MANUAL_UPDATE = PROC_CHAR_DIR / 'count_manual_update_grouped_by_month_year_feed.csv'
elif CHARACTERISTIC == 'FLAG':
    CHARACTERISTIC_CONFLICTS = FLAG_CONFLICTS
    CONFLICTS_ALL = PROC_CHAR_DIR / 'count_conflicts_grouped_by_month_year_feed_status.csv'
    RESOLVED_ANALYST = PROC_CHAR_DIR / 'count_resolved_conflicts_grouped_by_month_year_analyst.csv'
    CONFLICTS_IGNORED = PROC_CHAR_DIR / 'count_ignored_grouped_by_month_year_feed.csv'
    CONFLICTS_LIKENESS = PROC_CHAR_DIR / 'count_likeness_grouped_by_month_year_feed.csv'
    CONFLICTS_MANUAL_UPDATE = PROC_CHAR_DIR / 'count_manual_update_grouped_by_month_year_feed.csv'
elif CHARACTERISTIC == 'VSL NAME':
    CHARACTERISTIC_CONFLICTS = VSL_NAME_CONFLICTS
    CONFLICTS_ALL = PROC_CHAR_DIR / 'count_conflicts_grouped_by_month_year_feed_status.csv'
    RESOLVED_ANALYST = PROC_CHAR_DIR / 'count_resolved_conflicts_grouped_by_month_year_analyst.csv'
    CONFLICTS_IGNORED = PROC_CHAR_DIR / 'count_ignored_grouped_by_month_year_feed.csv'
    CONFLICTS_LIKENESS = PROC_CHAR_DIR / 'count_likeness_grouped_by_month_year_feed.csv'
    CONFLICTS_MANUAL_UPDATE = PROC_CHAR_DIR / 'count_manual_update_grouped_by_month_year_feed.csv'
else:
    raise ValueError('There is no data for this characteristic. Check directory.')


LINKED_CONFLICTS = PREPROCESSED_DIR / 'conflicts_linked_2020.csv'
NOT_LINKED_CONFLICTS = PREPROCESSED_DIR / 'conflicts_not_linked_2020.csv'
