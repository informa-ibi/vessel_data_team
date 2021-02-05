from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'datasets'
INPUT_DIR = DATA_DIR / 'input'
OUTPUT_DIR = DATA_DIR / 'output'
PREPROCESSED_DIR = DATA_DIR / 'pre-processed'

# Input files
COMPANY = INPUT_DIR / 'COMPANY_COMPANY.csv'
ENG_DESIGNATIONS = INPUT_DIR / 'SID_VSLENGINE_DESIGNATIONS.csv'
ENG_MODEL = INPUT_DIR / 'SID_VSLENGINE_MODELS.csv'
LR = INPUT_DIR / 'LR_ENGINE 20201016.csv'
VSL_ID = INPUT_DIR / 'SID_VESSELS.csv'
VSL_ENGINES = INPUT_DIR / 'SID_VSLENGINES.csv'

# Preprocessed files
SID_PROCESSED = PREPROCESSED_DIR / 'sid_vsl_engines_processed.csv'
LR_PROCESSED = PREPROCESSED_DIR / 'lr_main_engines.csv'

# Output files for analysis
LR_NOT_FOR_UPLOAD = OUTPUT_DIR / 'lr_not_for_upload.csv'
LR_FOR_UPLOAD_AND_APPLY = OUTPUT_DIR / 'lr_for_upload_and_apply.csv'
LR_CONFLICTS_TO_COMPARE = OUTPUT_DIR / 'lr_conflicts_to_compare.csv'
LR_FOR_MANUAL_REVIEW = OUTPUT_DIR / 'lr_for_manual_review.csv'

# Data to apply - manual review to check engine designations
LR_APPLY_CHECK_ENG_DESIG = OUTPUT_DIR / 'lr_engine_designation_comparison.csv'
