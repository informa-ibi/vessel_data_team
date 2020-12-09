# Universe 1 Vessels

Use the following query:

    SELECT  v.llpno
	, v.lregno imo
	, v.status
	, COALESCE(v.gross,0) gross
	, COALESCE(v.dwt,0) dwt
	, v.gtype
	, v.gtype||v.type vsltype
	, v.classb_ind
	, 'UNI1' universe 
    FROM    sid.vessels v 
        WHERE   v.status = 'L'
        AND     ( COALESCE(v.gtype,'Z') IN ('B','C','G','L','M','P','T','U') 
        OR      COALESCE(v.gtype||v.type,'ZZZ') = 'OFY' )
        AND     COALESCE(v.gross,0) > 100 
        AND     COALESCE(v.classb_ind,'N') = 'N' 
