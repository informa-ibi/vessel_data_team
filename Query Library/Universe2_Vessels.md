# Universe 2 vessels

    SELECT  v.llpno, 

    v.lregno imo, 
    v.status, 
    COALESCE(v.gross,0) gross, 
    COALESCE(v.dwt,0) dwt, 
    v.gtype, 
    v.gtype||v.type vsltype, 
    v.classb_ind, 
    'UNI2' universe 

    FROM    sid.vessels v 
    WHERE   v.status = 'L'
    AND     (COALESCE(v.gtype,'Z') NOT IN ('B','C','G','L','M','P','T','U','N') 
    OR      COALESCE(v.gtype||v.type,'ZZZ') != 'OFY' )
    AND     COALESCE(v.classb_ind,'N') = 'N'
    AND     NOT EXISTS (SELECT 1 FROM TABLENAME x WHERE x.llpno = v.llpno);
