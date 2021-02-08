import pandas as pd
from src.setup import LR_CONFLICTS_TO_COMPARE
import time
start_time = time.time()

MATCH_THRESHOLD = 70.

if __name__ == '__main__':
    lr_sid_to_compare_df = pd.read_csv(LR_CONFLICTS_TO_COMPARE)

    print("If uploading the entire dataset without checking similaritites, there would be {} conflicts raised for "
          "{} vessels."
          .format(len(lr_sid_to_compare_df), len(lr_sid_to_compare_df.IMO.unique())))

    # Will either be deemed as the same or different. If the same, can ignore them - if different will raise a conflict
    ignore_df = lr_sid_to_compare_df.loc[lr_sid_to_compare_df.match_val >= MATCH_THRESHOLD][['IMO',
                                                                                             'ENGINE_DESIGNATION',
                                                                                             'engine_designation_from_sid']]

    conflicts_df = lr_sid_to_compare_df.loc[lr_sid_to_compare_df.match_val < MATCH_THRESHOLD][['IMO',
                                                                                               'ENGINE_DESIGNATION',
                                                                                               'engine_designation_from_sid']]

    print("--- %s seconds ---" % (time.time() - start_time))

    print('Number unique vessels that conflicts would be raised for before any matching checking is '
          '{}'.format(len(lr_sid_to_compare_df.IMO.unique())))
    print('Number unique vessels that conflicts would be raised for after matching checking at threshold {} is '
          '{}'.format(MATCH_THRESHOLD, len(conflicts_df.IMO.unique())))
