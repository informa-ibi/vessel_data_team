# Extract all offices with specific Business Sector

    SELECT
    COMPANY_ID,
    ROOT_NAME,
    MAX(BUILDER)

    FROM

    (SELECT 
    t1.id as COMPANY_ID,
    t1.root_name,
    t3.business_sector_id,
    CASE WHEN t3.business_sector_id = 21 THEN 1 ELSE 0 END AS BUILDER
    FROM company.company t1
    LEFT JOIN company.office t2
    ON t1.id = t2.company_id
    LEFT JOIN company.office_business_sector t3
    ON t2.id = t3.office_id
    WHERE t1.id IN (232140, 520037, 177696))

    GROUP BY company_ID, ROOT_NAME
