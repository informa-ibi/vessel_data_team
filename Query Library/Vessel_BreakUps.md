select t1.llpno
    , t5.lregno         as IMO_Number
    , t5.name           as Vessel_Name
    , t2.description    as How_Dead
    , t1.deaddt         as Dead_Date
    , t1.brokendt       as Broken_Date
    , t3.root_name      as Breaker
    , t4.name           as Broken_At
    , t1.lt_tonnes
    , t1.lt_tonnes_price
    , t1.dead_authority
    , t6.description    as Ownership_Type
    , t6.root_name      as Company_Name
    , t6.startdt        as Start_Date
    , t6.descr          as Ownership_Authority
    , t7.name           as Place_ID
    , t7.ardt           as Arrived_Date
    , t7.movetype       as Move_Type
    , t7.movetypeq      as Move_Type_Q
    , t8.name           as Origin
    , t9.name           as Destination 
    
from sid.vslhistories t1
LEFT JOIN sid.how_dead t2
ON t1.how_dead = t2.id

LEFT JOIN company.company t3
ON t1.breaker_compid = t3.id

LEFT JOIN sid.places t4
ON t1.broken_place = t4.idno

LEFT JOIN sid.vessels t5
ON t1.llpno = t5.llpno

LEFT JOIN (select t1.llpno, t2.description, t3.root_name, t1.startdt, t1.descr
FROM sid.vsl_co_rels t1
LEFT JOIN sid.vslco_rel_type t2
ON t1.rel_type = t2.id
LEFT JOIN company.company t3
ON t1.compid = t3.id
WHERE curr_ind = 'Y') t6
ON t1.llpno = t6.llpno

LEFT JOIN 
(select * from ( 
select t1.llpno, t1.placeidno, t1.ardt, t1.movetype, t1.movetypeq, t2.name, row_number() over (partition by t1.llpno order by t1.llpno, t1.ardt desc) as rn from sid.moves t1
LEFT JOIN sid.places t2
ON t1.placeidno = t2.idno
where llpno in (
select t1.llpno
from sid.vslhistories t1
LEFT JOIN sid.how_dead t2
ON t1.how_dead = t2.id
LEFT JOIN company.company t3
ON t1.breaker_compid = t3.id
LEFT JOIN sid.places t4
ON t1.broken_place = t4.idno
LEFT JOIN sid.vessels t5
ON t1.llpno = t5.llpno
LEFT JOIN (select t1.llpno, t2.description, t3.root_name, t1.startdt, t1.descr
FROM sid.vsl_co_rels t1
LEFT JOIN sid.vslco_rel_type t2
ON t1.rel_type = t2.id
LEFT JOIN company.company t3
ON t1.compid = t3.id
WHERE curr_ind = 'Y') t6
ON t1.llpno = t6.llpno
where deaddt >= '11-AUG-2020 00:00:00'))
where rn = 1) t7
on t1.llpno = t7.llpno

left join sid.places t8
on t5.origin = t8.idno

left join sid.places t9
on t5.destination = t9.idno

where deaddt >= '11-AUG-2020 00:00:00';

