# Universe 1 Vessel with YOB Groups

Use the following query:

    SELECT  v.llpno, v.lregno imo, v.status, COALESCE(v.gross,0) gross, COALESCE(v.dwt,0) dwt, v.gtype, v.gtype||v.type vsltype, v.flag, v.built, v.classb_ind, 'UNI1' universe,
    COALESCE(
    CASE WHEN v.built < 1960 then '< 1960' else null end,
    CASE WHEN v.built between 1960 and 1969 then '1960-1969' else null end,
    CASE WHEN v.built between 1970 and 1979 then '1970-1979' else null end,
    CASE WHEN v.built between 1980 and 1989 then '1980-1989' else null end,
    CASE WHEN v.built between 1990 and 1999 then '1990-1999' else null end,
    CASE WHEN v.built between 2000 and 2009 then '2000-2009' else null end,
    CASE WHEN v.built between 2010 and 2020 then '2000-2020' else 'NA' end
    ) as YOB_groups
        FROM    sid.vessels v
            WHERE   v.status = 'L'
            AND v.class1 is NULL
            AND v.class2 is NULL
            AND v.class3 is NULL
            AND     ( COALESCE(v.gtype,'Z') IN ('B','C','G','L','M','P','T','U')
            OR      COALESCE(v.gtype||v.type,'ZZZ') = 'OFY' )
            AND     COALESCE(v.gross,0) > 100
            AND     COALESCE(v.classb_ind,'N') = 'N'
