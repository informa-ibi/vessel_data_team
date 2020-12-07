# SQL Queries
The following contains the SQL queries used to extract boilers data from Oracle.


    select t4.descr, count(*) from sid.vslboilers t1
    left join SID.vslhull_designs t2
    on t1.hull_id = t2.idno
    left join sid.vessels t3
    on t2.llpno = t3.llpno
    left join sid.vslgtypes t4
    on t3.gtype = t4.code
    group by t4.descr;
    --t3.gtype;



    select t3.dwtton from sid.vslboilers t1
    left join SID.vslhull_designs t2
    on t1.hull_id = t2.idno
    left join SID.vsltonnages t3
    on t2.llpno = t3.llpno
    where t3.dwtton is not null
    order by t3.dwtton;
