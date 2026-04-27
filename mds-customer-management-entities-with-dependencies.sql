USE [MDS];
GO

SELECT
    m.[Name] AS Model_Name,
    e.[Name] AS Entity_Name,
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM mdm.tblAttribute a
            WHERE a.Entity_ID = e.ID
              AND a.DomainEntity_ID > 0
        )
        THEN 'Yes' ELSE 'No'
    END AS Has_Entity_Dependencies,
    ISNULL(
        STUFF((
            SELECT DISTINCT ', ' + de.[Name]
            FROM mdm.tblAttribute a2
            JOIN mdm.tblEntity de
              ON de.ID = a2.DomainEntity_ID
            WHERE a2.Entity_ID = e.ID
              AND a2.DomainEntity_ID > 0
            FOR XML PATH(''), TYPE
        ).value('.', 'nvarchar(max)'), 1, 2, ''),
        ''
    ) AS Depends_On_Entities
FROM mdm.tblModel m
JOIN mdm.tblEntity e
  ON e.Model_ID = m.ID
WHERE m.[Name] = N'Customer Management'
ORDER BY e.[Name];
