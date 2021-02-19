# Ownership Team Conflicts Analysis
The following queries are used in regards to analysis completed for the Ownership team, looking at the timeliness and accuracy of resolving conflicts from feeds regarding ownership changes.


## Reg Owner Conflicts:
The following query contains the main table that is created, with 4 subsequent queries that can be uncommented for those pieces of analysis from the main table `ownership_t`:
            
      -- Inital table with all the relevant features
      WITH ownership_t AS (select
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
        
        , ROW_NUMBER() OVER (PARTITION BY vessel_conflict_id ORDER BY vessel_conflict_id) AS RN

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
        where t2.data_item_name like 'REG_OWNER'
        and t1.created_date >= '01-JAN-2020 00:00:00'

        ORDER BY t3.vessel_conflict_id)

      -- Count conflicts by analyst, grouping by month, year, analyst
        SELECT RESOLVED_MONTH, RESOLVED_YEAR, resolved_by, COUNT(resolved_by) AS NUM_PER_ANALYST
        FROM ownership_t
        WHERE RN = 1
        GROUP BY RESOLVED_MONTH, RESOLVED_YEAR, resolved_by;

      ---- Count conflicts grouped by month, year, feed and conflict status
      --  SELECT CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, CONFLICT_STATUS, DATA_FEED, COUNT(CONFLICT_STATUS) AS COUNT_STATUS_PER_FEED
      --  FROM ownership_t
      --  WHERE RN = 1
      --  GROUP BY CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, CONFLICT_STATUS, DATA_FEED;
      --
      ---- Count conflicts where conflict status is ignore, grouping by month, year, feed
      --  SELECT CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, DATA_FEED, COUNT(DATA_FEED) AS NUM_IGNORED
      --  FROM ownership_t
      --  WHERE CONFLICT_STATUS = 'IGNORED' AND RN = 1
      --  GROUP BY CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, DATA_FEED;
      --  
      ---- Count conflicts where reason - likeness - how often does this happen and
      ---- from which feeds
      --  SELECT CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, DATA_FEED, COUNT(DATA_FEED) AS NUM_LIKENESS
      --  FROM ownership_t
      --  WHERE IGNORE_REASON = 'Likeness' AND RN = 1
      --  GROUP BY CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, DATA_FEED;
      
      ---- Count conflicts where conflict status is manual update, grouping by month, year, feed
      --    SELECT CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, DATA_FEED, COUNT(DATA_FEED) AS NUM_MANUAL_UPDATE
      --    FROM ownership_t
      --    WHERE CONFLICT_STATUS = 'MANUAL UPDATE' AND RN = 1
      --    GROUP BY CREATED_MONTH, CREATED_YEAR, RESOLVED_MONTH, RESOLVED_YEAR, DATA_FEED;


