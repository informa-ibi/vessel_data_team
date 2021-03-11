from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'datasets'
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'output'

IMAGES = Path(__file__).parent.parent / 'images'

CHARACTERISTIC = 'REG_OWNER'

CONFLICTS_ALL = INPUT_DIR / f'{CHARACTERISTIC}' / 'count_conflicts_grouped_by_month_year_feed_status.csv'
RESOLVED_ANALYST = INPUT_DIR / f'{CHARACTERISTIC}' / 'count_resolved_conflicts_grouped_by_month_year_analyst.csv'
CONFLICTS_IGNORED = INPUT_DIR / f'{CHARACTERISTIC}' / 'count_ignored_grouped_by_month_year_feed.csv'
CONFLICTS_LIKENESS = INPUT_DIR / f'{CHARACTERISTIC}' / 'count_likeness_grouped_by_month_year_feed.csv'
CONFLICTS_MANUAL_UPDATE = INPUT_DIR / f'{CHARACTERISTIC}' / 'count_manual_update_grouped_by_month_year_feed.csv'


REG_OWNER_CONFLICTS = INPUT_DIR / 'REG_OWNER_conflicts_2020.csv'
FLAG_CONFLICTS = INPUT_DIR / 'FLAG_conflicts_2020.csv'
VSL_NAME_CONFLICTS = INPUT_DIR / 'VSL_NAME_conflicts_2020.csv'
LINKED_CONFLICTS = OUTPUT_DIR / 'conflicts_linked_2020.csv'
NOT_LINKED_CONFLICTS = OUTPUT_DIR / 'conflicts_not_linked_2020.csv'
