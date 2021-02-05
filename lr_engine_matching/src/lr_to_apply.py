import pandas as pd
import numpy as np
from fuzzywuzzy import process, fuzz
from src.setup import SID_PROCESSED, LR_FOR_UPLOAD_AND_APPLY, ENG_DESIGNATIONS, LR_APPLY_CHECK_ENG_DESIG
import time
start_time = time.time()


def add_match(new_eng, existing_list):
    highest = process.extractOne(new_eng, existing_list)
    sid_closest_eng = highest[0]
    sid_closest_eng_val = highest[1]
    return sid_closest_eng_val, sid_closest_eng


def compare_company(str1, str2):
    match = fuzz.token_set_ratio(str1, str2)
    return match


output_cols_to_include = [
    'ENGINE_DESIGNATION', 'ENGINE_DESIGNATION_compare', 'eng_desig_match_val',
    'CYLINDERS_ARRANGEMENT', 'CYLINDER_ARRANGEMENT_compare',
    'NO_OF_CYLINDERS', 'NUMBER_OF_CYLINDERS_compare',
    'BORE', 'BORE_compare',
    'STROKE', 'STROKE_compare',
    'FUEL_TYPE', 'FUEL_TYPE_compare',
    'DESIGNER', 'Designer_compare'
]


if __name__ == '__main__':
    # Of the data to upload and apply, check the engine designations if they need to be created or mapped
    sid_df = pd.read_csv(SID_PROCESSED)
    lr_to_apply_df = pd.read_csv(LR_FOR_UPLOAD_AND_APPLY)
    sid_eng_desig_df = pd.read_csv(ENG_DESIGNATIONS, encoding='cp1252', low_memory=False)

    # Isolate the new values from LR that replace the UNKNOWN values that are new eng designations
    existing_eng_desig = sid_eng_desig_df.ENGINE_DESIGNATION.tolist()
    new_eng_des_replace_unk = np.setdiff1d(lr_to_apply_df.ENGINE_DESIGNATION.unique().tolist(), existing_eng_desig)

    # Identify engine designation and Manufacturer values that are very different - this part is TIMELY!
    vsl_eng_with_new_eng_desig_df = lr_to_apply_df.loc[lr_to_apply_df.ENGINE_DESIGNATION.isin(new_eng_des_replace_unk)]
    vsl_eng_with_new_eng_desig_df[['eng_desig_match_val', 'eng_desig_match_in_sid']] = vsl_eng_with_new_eng_desig_df \
        .apply(lambda row: pd.Series(add_match(row['ENGINE_DESIGNATION'], existing_eng_desig)), axis=1)

    # Get the Designer etc of the existing Engine Desigination value from SID that is closest to the LR value
    vsl_eng_with_new_eng_desig_company_df = vsl_eng_with_new_eng_desig_df.merge(sid_df.add_suffix('_compare'),
                                                                                how='left',
                                                                                left_on='eng_desig_match_in_sid',
                                                                                right_on='ENGINE_DESIGNATION_compare')

    # Part 6: Drop irrelevant columns and duplicates - doesn't need to be on ship by ship level
    # Need: Model, Description, Designer, Designation, Bore, Arrangement, No. Cyl, Type, Cycle, Action, Fuel, Stroke
    # Don't have: Model, Description, Action, Cycle
    # Less Priority: Engine_Type, FUEL_TYPE
    # Don't include: IMO, No Engine, Place of Build, POWER_KW MAIN_OR_AUX
    eng_desigs_to_manually_review = vsl_eng_with_new_eng_desig_company_df[output_cols_to_include].drop_duplicates()

    # Part 7: Add value for matching the designer
    eng_desigs_to_manually_review['designer_match_val'] = eng_desigs_to_manually_review.apply(lambda row: pd.Series(
        compare_company(row['Designer_compare'], row['DESIGNER'])), axis=1)

    eng_desigs_to_manually_review.to_csv(LR_APPLY_CHECK_ENG_DESIG, index=False)

    # TODO Create a map dictionary and create table of new data

    print("--- %s seconds ---" % (time.time() - start_time))
