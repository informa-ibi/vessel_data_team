# VDP Conflicts

Use the following:

        SELECT 
         t3.name as Vname
        ,t3.lregno
        ,concat(t3.type,t3.gtype) Vtype
        ,t3.flag
        ,t3.gross
        ,t3.sigs as CallSign
        ,t3.status
        ,t2.data_item_name
        ,t1.source_value
        ,t1.db_value
        ,t3.class1
        ,t1.created_date
        ,t1.built
        ,CASE WHEN t1.conflicts_status_id = 1 THEN 'Pending' END as Conflict_Status
     from vdp.vessel_conflicts t1
    left join vdp.data_items t2
    on t1.data_item_id = t2.id
    left join sid.vessels t3
    on t1.vessel_id = t3.llpno
    where t1.conflict_status_id = 1
    and status not in ('D', 'A', 'R', 'E')
    and t2.data_item_name in ('GROSS', 'DWT', 'LOA');
