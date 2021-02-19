import pandas as pd
from src.setup import LR_FOR_UPLOAD_AND_APPLY, ENG_DESIGNATIONS, LR_APPLY_CHECK_ENG_DESIG_REVIEWED
import time
start_time = time.time()


company_cols_to_include = [
    'ID',
    'ROOT_NAME'
]

engine_designations_to_create_columns = [
    'ENGINE_DESIGNATION_lr',
    'CYLINDERS_ARRANGEMENT_lr',
    'NO_OF_CYLINDERS_lr',
    'BORE_lr',
    'STROKE_lr',
    'FUEL_TYPE_lr',
    'DESIGNER_lr',
    'Company ID'
]

engine_designations_to_map_columns = [
    'ENGINE_DESIGNATION_lr',
    'ENGINE_DESIGNATION_compare',
    'CYLINDERS_ARRANGEMENT_lr',
    'CYLINDER_ARRANGEMENT_compare',
    'NO_OF_CYLINDERS_lr',
    'NUMBER_OF_CYLINDERS_compare',
    'BORE_lr',
    'BORE_compare',
    'STROKE_lr',
    'STROKE_compare',
    'FUEL_TYPE_lr',
    'FUEL_TYPE_compare',
    'DESIGNER_lr',
    'Designer_compare',
]

map_columns_to_output = [
    'IMO',
    'NO_OF_ENGINE',
    'ENGINE_TYPE',
    'ENGINE_DESIGNATION',
    'POWER_KW',
    'CYLINDERS_ARRANGEMENT',
    'NO_OF_CYLINDERS',
    'BORE',
    'STROKE',
    'ENGINE_BUILDER',
    'DESIGNER',
    'PLACE_OF_BUILD',
    'FUEL_TYPE',
    'MAIN_OR_AUX'
]

map_columns_to_output = [s + 'output' for s in map_columns_to_output]

if __name__ == '__main__':
    # Of the data to upload and apply, check the engine designations if they need to be created or mapped
    lr_to_apply_df = pd.read_csv(LR_FOR_UPLOAD_AND_APPLY)
    sid_eng_desig_df = pd.read_csv(ENG_DESIGNATIONS, encoding='cp1252', low_memory=False)
    manually_reviewed_df = pd.read_excel(LR_APPLY_CHECK_ENG_DESIG_REVIEWED)

    # Formatting columns
    manually_reviewed_df['BORE_lr'] = manually_reviewed_df['BORE_lr'].astype(str)
    manually_reviewed_df['STROKE_lr'] = manually_reviewed_df['STROKE_lr'].astype(str)

    # Check all the unique values of the reviewed output column to ensure 'Yes' or 'No' answers
    print('The unique values for the match review are:\n{}'.format(manually_reviewed_df['Match (Yes/No)'].unique()))

    # Engine designations to create in SID - include the company ID of the designer
    to_create_df = manually_reviewed_df.loc[manually_reviewed_df['Match (Yes/No)'] !=
                                            'Yes'][engine_designations_to_create_columns]

    # Engine designations to map
    to_map_df = manually_reviewed_df.loc[manually_reviewed_df['Match (Yes/No)'] ==
                                         'Yes'][engine_designations_to_map_columns]
    to_map_df['is_mapped'] = 'mapped'
    to_map_df.columns = [col.replace('_lr', '') for col in to_map_df.columns]
    output_lr_apply_df = lr_to_apply_df.merge(to_map_df, how='left',
                                              left_on=['ENGINE_DESIGNATION',
                                                       'CYLINDERS_ARRANGEMENT',
                                                       'NO_OF_CYLINDERS', 'BORE', 'STROKE', 'FUEL_TYPE', 'DESIGNER'],
                                              right_on=['ENGINE_DESIGNATION',
                                                        'CYLINDERS_ARRANGEMENT',
                                                        'NO_OF_CYLINDERS', 'BORE', 'STROKE',
                                                        'FUEL_TYPE', 'DESIGNER'])

    lr_columns = lr_to_apply_df.columns
    df1_cols = ['IMO', 'NO_OF_ENGINE', 'ENGINE_TYPE', 'ENGINE_DESIGNATION_compare', 'POWER_KW',
                'CYLINDER_ARRANGEMENT_compare', 'NUMBER_OF_CYLINDERS_compare', 'BORE_compare',
                'STROKE_compare', 'ENGINE_BUILDER', 'Designer_compare', 'PLACE_OF_BUILD',
                'FUEL_TYPE_compare', 'MAIN_OR_AUX']

    df1 = output_lr_apply_df.loc[output_lr_apply_df.is_mapped == 'mapped'][df1_cols]
    df1.columns = [col.replace('_compare', '').upper() for col in df1.columns]
    df2 = output_lr_apply_df.loc[output_lr_apply_df.is_mapped != 'mapped'][lr_columns]\
        .rename(columns={'NO_OF_CYLINDERS': 'NUMBER_OF_CYLINDERS',
                         'CYLINDERS_ARRANGEMENT': 'CYLINDER_ARRANGEMENT'})

    df_output = pd.concat([df1, df2])
    # TODO Figure out the columns to output and replace the other values that have been mapped
    # TODO add Company IDs
    print("--- %s seconds ---" % (time.time() - start_time))
