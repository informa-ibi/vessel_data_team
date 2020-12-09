# MMSI Concatenation Examples

Within Oracle, the MMSI is contained as two separate fields:

- `mmsi_country_code`: 3 letter country code relating to the flag of the vessel; and
- `mmsi_vessel_code`: 6 letter code

For `mmsi_vessel_code` this number may have leading zeroes and so will need to be forward filled before combining the two columns into one MMSI column.

  E.g. 
  - `mmsi_country_code` = 123
  - `mmsi_vessel_code`  = 456 will be forward filled to 000456
  - the resulting `MMSI` will then be 123000456
  
  
  The following can be used in Oracle:


    select 
    Vessel_Name, 
    Flag, 
    Gross, 
    IMO_Number,
    mmsi_country_code,
    --mmsi_vessel_code,
    --length,
    --length(mmsi_vessel_code_new),
    mmsi_vessel_code_new,
    concat(MMSI_country_code,MMSI_vessel_code_new) as MMSI_Number,
    LLI_Number, 
    Vessel_Type 

    from
    (
    select 
    v.Name as Vessel_Name, 
    Flag, 
    Gross, 
    LRegNo as IMO_Number,
    v.mmsi_country_code,
    v.mmsi_vessel_code,
    length(mmsi_vessel_code) as length,
    coalesce(
    case when length(mmsi_vessel_code) = 2 then concat('0000',v.mmsi_vessel_code) else null end,
    case when length(mmsi_vessel_code) = 3 then concat('000',v.mmsi_vessel_code) else null end,
    case when length(mmsi_vessel_code) = 4 then concat('00',v.mmsi_vessel_code) else null end,
    case when length(mmsi_vessel_code) = 5 then concat('0',v.mmsi_vessel_code) else to_char(v.mmsi_vessel_code)  
    end)
    as mmsi_vessel_code_new,
    --concat(MMSI_country_code,MMSI_vessel_code) as MMSI_Number, 
    LLPNO as LLI_Number, 
    Type as Vessel_Type 
    FROM sid.vessels v

    WHERE (v.name like '%No.8'
    OR v.name like '%no.8'
    OR v.name like '%no 8'
    OR v.name like '%No 8'
    OR v.name like '%no. 8'
    OR v.name like '%No. 8')
    AND status = 'L'
    and (v.mmsi_country_code is not null and MMSI_vessel_code is not null)
    )
    --Order by name desc;

    OR USING LPAD FUNCTION

    select 
    v.Name as Vessel_Name, 
    Flag, 
    Gross, 
    LRegNo as IMO_Number,
    v.mmsi_country_code,
    v.mmsi_vessel_code,
    --LPAD(mmsi_vessel_code,6,0),
    concat(MMSI_country_code,LPAD(MMSI_vessel_code,6,0)) as MMSI_Number, 
    LLPNO as LLI_Number, 
    Type as Vessel_Type 
    FROM sid.vessels v

    WHERE (v.name like '%No.8'
    OR v.name like '%no.8'
    OR v.name like '%no 8'
    OR v.name like '%No 8'
    OR v.name like '%no. 8'
    OR v.name like '%No. 8')
    AND status = 'L'
    and (v.mmsi_country_code is not null and MMSI_vessel_code is not null)

