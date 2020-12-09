# Scrubber Tables

Use the following in Oracle:

    select 
        t1.vessel_id
        , t2.description as installation_type
        , t3.description as operating_arrangement
        , t4.description as treatment_type 
        , t5.root_name as manufacturer
        , t5.id

    from sid.vslscrubbers t1

    left join SID.scrubber_inst_types t2
    on t1.installation_type_id = t2.id
    left join SID.scrubber_op_arrangements t3
    on t1.operating_arrangement_id = t3.id
    left join SID.scrubber_treatment_types t4
    on t1.treatment_type_id = t4.id
    left join company.company t5
    on t1.system_manufacturer_id = t5.id
    ;


    select distinct manufacturer, id

    from
    (
    select 
        t1.vessel_id
        , t2.description as installation_type
        , t3.description as operating_arrangement
        , t4.description as treatment_type 
        , t5.root_name as manufacturer
        , t5.id

    from sid.vslscrubbers t1

    left join SID.scrubber_inst_types t2
    on t1.installation_type_id = t2.id
    left join SID.scrubber_op_arrangements t3
    on t1.operating_arrangement_id = t3.id
    left join SID.scrubber_treatment_types t4
    on t1.treatment_type_id = t4.id
    left join company.company t5
    on t1.system_manufacturer_id = t5.id
    )
    ;
