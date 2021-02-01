# Lloyd's Register Engine Designation Matching
##Overview
Analysis of the Lloyds Register engine data feed versus the engine
 data in SID, namely comparing the engine designation.
 
It is assumed that the input data files reside in 
`/lr_engine_matching/datasets/input` folder.

Code structure
Insights from comparing the LR Main Engine data and the SID 
Engine Data can be found by running `/lr_engine_matching/src/insights.py`

While the output data for comparision can be found by running
 `/lr_engine_matching/src/match_LR_engines.py`
 
 
 Should any files need updated their path can be changed in
 the `/lr_engine_matching/src/setup.py` file


## Downloading data from SID 
In order to compare the LR feed with the existing data in SID, we download
a static file. Use the following queries to get the tables and then export 
them to csv and rename accordingly i.e. `COMPANY.COMPANY` becomes 
`COMPANY_COMPANY.csv`:


    SELECT * FROM COMPANY.COMPANY;
    
    SELECT * FROM SID.vessels;
    
    SELECT * FROM SID.vslengine_designations;
    
    SELECT * FROM SID.vslengine_models;
    
    SELECT * FROM SID.vslengines;
