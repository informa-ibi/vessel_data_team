import pandas as pd
from fuzzywuzzy import fuzz
from src.setup import SID_PROCESSED, LR_PROCESSED, LR_NOT_FOR_UPLOAD, LR_FOR_UPLOAD_AND_APPLY, LR_CONFLICTS_TO_COMPARE, \
    LR_FOR_MANUAL_REVIEW
import time
start_time = time.time()


def get_sid_engine_designation(imo):
    engine_designation_list = sid_df.loc[sid_df.LREGNO == imo].ENGINE_DESIGNATION.unique().tolist()
    return engine_designation_list


def compare_sid_versus_lr_engine_designation(str1, str2):
    match = fuzz.token_set_ratio(str1, str2)
    return match


if __name__ == '__main__':
    sid_df = pd.read_csv(SID_PROCESSED)
    lr_df = pd.read_csv(LR_PROCESSED)

    list_lr_imos = lr_df.IMO.unique().tolist()  # get list of IMOs of interest
    imos_in_sid = sid_df.LREGNO.unique().tolist()

    # Dataframes relating to what we'll do with the data from LR
    not_for_upload_df = pd.DataFrame(columns=lr_df.columns)
    to_upload_and_apply_df = pd.DataFrame(columns=lr_df.columns)
    to_compare_df = pd.DataFrame(columns=lr_df.columns)
    manual_review_df = pd.DataFrame(columns=lr_df.columns)

    for i, row in lr_df.iterrows():
        imo_from_lr = row.IMO
        if imo_from_lr in imos_in_sid:  # if IMO exists in SID
            eng_designation_from_lr = row.ENGINE_DESIGNATION
            if (eng_designation_from_lr != 'N/K') & (pd.notnull(eng_designation_from_lr)):  # if LR data is informative
                vsl_eng_designations_from_sid = get_sid_engine_designation(imo_from_lr)  # eng desig from SID for IMO
                num_vsl_eng_sid = len(vsl_eng_designations_from_sid)
                if num_vsl_eng_sid <= 1:  # If one or less engines in SID
                    if eng_designation_from_lr not in vsl_eng_designations_from_sid:  # different data to SID
                        if ('UNKNOWN' in vsl_eng_designations_from_sid) | ('N/K' in vsl_eng_designations_from_sid) \
                                | (num_vsl_eng_sid == 0):  # Upload as gain - SID data is unknown and LR provides data
                            to_upload_and_apply_df = to_upload_and_apply_df.append(row)
                        else:  # Values that will need to be compared
                            match_val = compare_sid_versus_lr_engine_designation(eng_designation_from_lr,
                                                                                 vsl_eng_designations_from_sid[0])
                            row['engine_designation_from_sid'] = vsl_eng_designations_from_sid[0]
                            row['match_val'] = match_val
                            to_compare_df = to_compare_df.append(row, ignore_index=True)
                    else:  # Same data in SID and LR so dont need to upload
                        not_for_upload_df = not_for_upload_df.append(row, ignore_index=True)
                else:  # if more than one engine in SID - more complicated and needs manual review
                    manual_review_df = manual_review_df.append(row, ignore_index=True)
            else:  # Data from LR not informative so dont need to upload
                not_for_upload_df = not_for_upload_df.append(row, ignore_index=True)
        else:  # The IMO from LR is not in SID, not uploading for now
            not_for_upload_df = not_for_upload_df.append(row, ignore_index=True)

    not_for_upload_df.to_csv(LR_NOT_FOR_UPLOAD, index=False)
    to_upload_and_apply_df.to_csv(LR_FOR_UPLOAD_AND_APPLY, index=False)
    to_compare_df.to_csv(LR_CONFLICTS_TO_COMPARE, index=False)
    manual_review_df.to_csv(LR_FOR_MANUAL_REVIEW, index=False)

    print("--- %s seconds ---" % (time.time() - start_time))
    # checks: sid_vsl_all_features_df.loc[sid_vsl_all_features_df.LREGNO == 9503457.0]
    # where it wasn't in the apply df and is more complicated - probably needs manually reviewed
