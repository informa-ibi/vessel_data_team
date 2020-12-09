# Ownership Team Conflicts Analysis
The following queries are used in regards to analysis completed for the Ownership team, looking at the timeliness and accuracy of resolving conflicts from feeds regarding ownership changes.


## Reg Owner Conflicts:
      select
      t1.id
      , t3.file_data_line_id
      , t3.vessel_conflict_id
      , t1.source_value
      , t1.db_value
      , t1.resolved_date
      , t1.created_date
      , t1.updated_date
      , t1.resolved_by
      -- , t1.ignore_reason_id
      -- , t1.source_value
      , t1.vessel_id
      -- , t1.data_feed_instance_file_id
      -- , t3.file_data_line_id
      , t2.data_item_name
      , t2.ignore_timeout_days
      , t5.name as Conflict_status
      -- , t5.description
      , t6.name as data_feed
      , t7.display_value as ignore_reason
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
      and t8.lregno = 9884617
      ORDER BY t3.vessel_conflict_id;
      
      
      
      
      
# Work In Progress
      
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
        -- , t1.ignore_reason_id
        -- , t1.source_value
        , t1.vessel_id
        -- , t1.data_feed_instance_file_id
        -- , t3.file_data_line_id
        , t2.data_item_name
        , t2.ignore_timeout_days
        , t5.name as Conflict_status
        -- , t5.description
        , t6.name as data_feed
        , t7.display_value as ignore_reason
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
        SELECT *
        FROM ownership_t;


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
        -- , t1.ignore_reason_id
        -- , t1.source_value
        , t1.vessel_id
        -- , t1.data_feed_instance_file_id
        -- , t3.file_data_line_id
        , t2.data_item_name
        , t2.ignore_timeout_days
        , t5.name as Conflict_status
        -- , t5.description
        , t6.name as data_feed
        , t7.display_value as ignore_reason
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
        SELECT CONFLICT_STATUS, DATA_FEED, COUNT(CONFLICT_STATUS) AS COUNT_STATUS_PER_FEED
        FROM ownership_t
        GROUP BY CONFLICT_STATUS, DATA_FEED
        ORDER BY COUNT_STATUS_PER_FEED DESC;


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
        -- , t1.ignore_reason_id
        -- , t1.source_value
        , t1.vessel_id
        -- , t1.data_feed_instance_file_id
        -- , t3.file_data_line_id
        , t2.data_item_name
        , t2.ignore_timeout_days
        , t5.name as Conflict_status
        -- , t5.description
        , t6.name as data_feed
        , t7.display_value as ignore_reason
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
        SELECT DATA_FEED, COUNT(DATA_FEED) AS NUM_IGNORED
        FROM ownership_t
        WHERE CONFLICT_STATUS = 'IGNORED'
        GROUP BY DATA_FEED
        ORDER BY NUM_IGNORED DESC;

