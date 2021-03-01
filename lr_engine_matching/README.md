## Lloyd's Register Engine Designation Matching
### Overview
Analysis of the Lloyds Register engine data feed versus the engine
 data in SID, namely comparing the engine designation.
 
It is assumed that the input data files reside in 
`/lr_engine_matching/datasets/input` folder.

##### Code structure
Should any files need updated their path can be changed in the 
`/lr_engine_matching/src/setup.py` file.

Run the scripts in this order:
- `prepare_data.py`
- `check_data_to_be_uploaded.py`
- `lr_to_apply.py`
- `compare_LR_and_SID.py`

From the `check_data_to_be_uploaded.py` script there will be 4 outputfiles:
- `lr_conflicts_to_compare.csv`: Informative data from LR that does not equal
the existing SID data that may need to be uploaded. Fuzzy matching has been done but may
need a manual review.
- `lr_for_manual_review.csv`: This data cannot be reviewed programmatically as it does
not follow a set pattern. It contains data from LR when the vessel in SID has 1 or fewer engines entries.
- `lr_for_upload_and_apply.csv`: Informative data from LR where the SID data is missing
or unknown and the LR data should be apply and overwritten. Further steps are taken to 
check the engine designations of these entries if they exist in SID.
- `lr_not_for_upload.csv`: This may be uninformative LR data (i.e. missing or unknown),
IMO's we don't yet have in SID, or the same data exists in SID already.

##### Downloading data from SID 
In order to compare the LR feed with the existing data in SID, we download
a static file. Use the following queries to get the tables and then export 
them to csv and rename accordingly i.e. `COMPANY.COMPANY` becomes 
`COMPANY_COMPANY.csv`:


    SELECT * FROM COMPANY.COMPANY;
    
    SELECT * FROM SID.vessels;
    
    SELECT * FROM SID.vslengine_designations;
    
    SELECT * FROM SID.vslengine_models;
    
    SELECT * FROM SID.vslengines;
