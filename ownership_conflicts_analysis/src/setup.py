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
