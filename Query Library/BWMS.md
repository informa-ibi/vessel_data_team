# Ballast Water Management System Tables

The following contains queries relating to BWMS:

      select 
          t1.vessel_id
          , t2.description as model 
          , t3.description as technology
          , t4.root_name as manufacturer
          from sid.vslbwms t1
      left join SID.vslbwms_models t2
      on t1.bwms_model_id = t2.id
      left join SID.vslbwms_technologies t3
      on t2.technology_id = t3.id
      left join company.company t4
      on t2.manufacturer_id = t4.id
      ;

      select distinct manufacturer, id

      from

      (
      select 
          t1.vessel_id
          , t2.description as model 
          , t3.description as technology
          , t4.root_name as manufacturer
          , t4.id
          from sid.vslbwms t1
      left join SID.vslbwms_models t2
      on t1.bwms_model_id = t2.id
      left join SID.vslbwms_technologies t3
      on t2.technology_id = t3.id
      left join company.company t4
      on t2.manufacturer_id = t4.id)
      ;
