# New AIS Latest

The following query can be used:

    SET PAGES 0
    SET LINESIZE 1000
    SET TERMOUT OFF
    SET FEEDBACK OFF
    SET TRIMSPOOL ON
    spool &5.NEW_AIS_Latest.csv
    SELECT '"'||'Vessel ID'||'","'||'IMO'||'","'||'VESSEL NAME'||'","'||'MMSI'||'","'||'START_AIS_POSITIONS_MMSI'||'","'||'END_AIS_POSITIONS_MMSI'||'","'||
    'START_LATITUDE'||'","'||'START_LONGITUDE'||'","'||'END_LATITUDE'||'","'||'END_LONGITUDE'||'","'||
    'MILES_DIFFERENCE'||'","'||'START_AIS_TIMESTAMP'||'","'||'END_AIS_TIMESTAMP'||'","'||'START_COG'||'","'||'START_SOG'||'","'||'END_COG'||'","'||'END_SOG'||'","'||
    'DESTINATION'||'","'||'ETA'||'","'||'DRAUGHT'||'","'||'DISTANCE'||'"'
    from dual;
    WITH vessel as (
        SELECT llpno, v.name, v.lregno, v.gross, v.status,v.class1,v.class2,v.class3,v.mmsi_country_code||LPAD(v.mmsi_vessel_code,6,0) mmsi
        FROM sid.vessels v
        WHERE v.status IN ('O', 'U', 'I')),
      LATEST AS (
                SELECT DISTINCT a.llpno, First_Value(a.rowid) over(PARTITION BY a.llpno ORDER BY a.AIS_positions.message_ts DESC) Row_ID
                    FROM    AIS.AIS_latest a, AIS.AIS_stations s2, ssgis.stationgroupings g
                        WHERE   a.llpno IN (SELECT llpno 
                                                FROM    VESSEL)
                        AND     a.ais_positions.asn_idno = s2.idno
                        AND     s2.idno = g.asn_idno
              ) ,
      EARLIEST AS  (
                SELECT DISTINCT a.llpno, First_Value(a.rowid) over(PARTITION BY a.llpno ORDER BY a.AIS_positions.message_ts ASC) Row_ID
                    FROM    AIS.AIS_latest a, AIS.AIS_stations s2, ssgis.stationgroupings g
                        WHERE   a.llpno IN (SELECT llpno 
                                                FROM    VESSEL)
                        AND     a.ais_positions.asn_idno = s2.idno
                        AND     s2.idno = g.asn_idno
              )          
              select  VESSEL.llpno||','||VESSEL.lregno||',"'||VESSEL.name||'",'||VESSEL.mmsi||','||a.ais_positions.mmsi_nb||','||b.ais_positions.mmsi_nb||','||
            Round(A.AIS_Positions.Latitude/600000,6) ||','||Round(A.AIS_Positions.Longitude/600000,6) ||','||
            Round(B.AIS_Positions.Latitude/600000,6) ||','||Round(B.AIS_Positions.Longitude/600000,6) ||','||
              trunc( ssgis.nm_between_pts (a.ais_positions.geopos.sdo_point.y,
                                           a.ais_positions.geopos.sdo_point.x,
                                           b.ais_positions.geopos.sdo_point.y,
                                           b.ais_positions.geopos.sdo_point.x),2)||',"'||
            To_Char(A.AIS_Positions.Message_Ts,'DD/MM/YYYY HH24:MI:SS') ||'","'||
            To_Char(B.AIS_Positions.Message_Ts,'DD/MM/YYYY HH24:MI:SS') ||'",'||
            A.AIS_Positions.COG/10 ||','||A.AIS_Positions.SOG/10 ||','||
            B.AIS_Positions.COG/10 ||','||B.AIS_Positions.SOG/10 ||',"'||
            NVL(dp.name,REPLACE(A.AIS_Static_Voyage.Destination,'"','''')) ||'","'||
            To_Char(A.AIS_Static_Voyage.ETA,'DD/MM/YYYY HH24:MI:SS') ||'",'||
            A.AIS_Static_Voyage.actual_draught/10 ||','||
            ROUND(a.distance_to_place,1) 
        FROM    VESSEL
            INNER JOIN  LATEST L ON L.LLPNo = VESSEL.LLPNo
            INNER JOIN  EARLIEST E ON E.LLPNo = VESSEL.LLPNo
            INNER JOIN  AIS.AIS_Latest A ON A.LLPNo = L.LLPNo AND A.RowID = E.Row_ID
            INNER JOIN  AIS.AIS_Latest B ON B.LLPNo = L.LLPNo AND B.RowID = L.Row_ID
            INNER JOIN  AIS.AIS_Stations S ON S.IDNo = A.AIS_Positions.ASN_IDNo
            LEFT JOIN   sid.places dp ON ( presid.get_location(A.AIS_static_voyage.destination,'') = dp.idno )
           where 
               ssgis.nm_between_pts (a.ais_positions.geopos.sdo_point.y,
                                           a.ais_positions.geopos.sdo_point.x,
                                           b.ais_positions.geopos.sdo_point.y,
                                           b.ais_positions.geopos.sdo_point.x) >= 200      ORDER BY    VESSEL.llpno ;
    SPOOL OFF
    EXIT
