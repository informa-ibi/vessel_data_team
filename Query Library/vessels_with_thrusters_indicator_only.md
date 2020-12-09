# Vessels with Thrusters (Indicator Only)

Use the following query:

    select llpno, count(*)
    from(
    select 
          t1.llpno
        , t1.lregno
        , t2.thruster_ind

    from sid.vessels t1

    left join SID.vslhull_designs t2

    on t1.llpno = t2.llpno

    where t1.status not in ('D', 'E', 'Q', 'X')

    and t2.thruster_ind is not null

    order by t1.lregno
    )

    group by llpno
    having count(*) >1
    ;

    --X both
    --Y Yes unspecified
    --B Bow
    --S Stern

    select distinct thruster_ind from SID.vslhull_designs;
