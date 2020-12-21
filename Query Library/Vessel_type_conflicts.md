# Vessel type conflicts for database value null or 'ZZZ'

  select 
      t1.id
    , max(t3.file_data_line_id) as file_data_line_id
    , max(t3.vessel_conflict_id) as vessel_conflict_id
    , max(t1.source_value) assource_value
    , max(t1.db_value) as db_value
--    , t1.resolved_date
    , max(t1.created_date) as created_date
--    , max(t1.updated_date)
--    , t1.resolved_by
--    , t1.ignore_reason_id
--    , t1.source_value
    , max(t1.vessel_id) as vessel_id
--    , t1.data_feed_instance_file_id
--    , t3.file_data_line_id
    , max(t2.data_item_name) as data_item_name
--    , t2.ignore_timeout_days
    , max(t5.name) as Conflict_status
--    , t5.description 
    , max(t6.name) as data_feed
 --   , t7.display_value as ignore_reason
  
from vdp.vessel_conflicts t1
left join vdp.data_items t2
on t1.data_item_id = t2.id

left join VDP.data_line_conflicts t3
on t1.id = t3.vessel_conflict_id

left join vdp.data_feed t4
on t3.data_feed_id = t4.id    

left join  VDP.conflict_status t5
on t1.conflict_status_id = t5.id

left join vdp.data_feed t6
on t3.data_feed_id = t6.id

left join VDP.ignore_reasons t7
on t1.ignore_reason_id = t7.id

left join sid.vessels t8
on t1.vessel_id = t8.llpno



where t2.data_item_name like 'VSL_TYPE'
and t5.name = 'PENDING'
and t6.name <> 'GHOST_VESSEL'
and (t1.db_value is null or t1.db_value = 'ZZZ')



--ORDER BY t3.vessel_conflict_id

group by t1.id
