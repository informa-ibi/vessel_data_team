# SQL Query for Data Extraction

Dataset with all the relevant features for analysis:
  

    WITH ownership_t as (select
        t1.id
        , t3.file_data_line_id
        , t3.vessel_conflict_id
        , t1.source_value
        , t1.db_value
        , t1.resolved_date
        , t1.created_date
        , t1.updated_date
        , t1.resolved_by
        , t1.vessel_id
        , t2.data_item_name
        , t2.ignore_timeout_days
        , t5.name as Conflict_status
        , t6.name as data_feed
        , t7.display_value as ignore_reason
    
        , extract(month from t1.created_date) AS CREATED_MONTH
        , extract(year from t1.created_date) AS CREATED_YEAR
        , extract(month from t1.resolved_date) AS RESOLVED_MONTH
        , extract(year from t1.resolved_date) AS RESOLVED_YEAR
        
        , ROW_NUMBER() OVER (PARTITION BY vessel_conflict_id, t6.name ORDER BY vessel_conflict_id, t6.name) AS RN
    
        from vdp.vessel_conflicts t1
        left join vdp.data_items t2
        on t1.data_item_id = t2.id
    
        left join VDP.data_line_conflicts t3
        on t1.id = t3.vessel_conflict_id
        left join vdp.data_feed t4
        on t3.data_feed_id = t4.id
        left join VDP.conflict_status t5
        on t1.conflict_status_id = t5.id
        left join vdp.data_feed t6
        on t3.data_feed_id = t6.id
        left join VDP.ignore_reasons t7
        on t1.ignore_reason_id = t7.id
        left join sid.vessels t8
        on t1.vessel_id = t8.llpno
        where t2.data_item_name like 'REG_OWNER'  -- FLAG, VSL NAME
        and t1.created_date >= '01-JAN-2020 00:00:00')
        SELECT * FROM OWNERSHIP_T
        WHERE RN = 1
        ORDER BY VESSEL_ID;
