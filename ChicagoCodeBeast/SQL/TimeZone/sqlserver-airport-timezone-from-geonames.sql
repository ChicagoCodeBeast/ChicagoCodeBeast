/*
  SQL Server: map Airport lat/long to IANA timezone using GeoNames allCountries data.

  Assumptions:
  - GeoNames table exists as dbo.geonames_allcountries with:
      latitude (float), longitude (float), timezone (nvarchar)
  - Airport table is [MDS].[mdm].[Airport] with:
      Name, [Lat], [Long]
*/

/* 1) Optional but recommended: add computed geography point + spatial index */
IF COL_LENGTH('dbo.geonames_allcountries', 'GeoPoint') IS NULL
BEGIN
    ALTER TABLE dbo.geonames_allcountries
    ADD GeoPoint AS geography::Point(latitude, longitude, 4326) PERSISTED;
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_geonames_allcountries_GeoPoint'
      AND object_id = OBJECT_ID('dbo.geonames_allcountries')
)
BEGIN
    CREATE SPATIAL INDEX IX_geonames_allcountries_GeoPoint
    ON dbo.geonames_allcountries(GeoPoint)
    USING GEOGRAPHY_AUTO_GRID;
END
GO

/* 2) Preview: nearest timezone match for each airport */
SELECT
    a.Name,
    a.[Lat],
    a.[Long],
    nn.timezone,
    nn.distance_m
FROM [MDS].[mdm].[Airport] a
OUTER APPLY (
    SELECT TOP (1)
        g.timezone,
        g.GeoPoint.STDistance(geography::Point(a.[Lat], a.[Long], 4326)) AS distance_m
    FROM dbo.geonames_allcountries g
    WHERE g.timezone IS NOT NULL
    ORDER BY g.GeoPoint.STDistance(geography::Point(a.[Lat], a.[Long], 4326))
) nn
WHERE a.[Lat] IS NOT NULL
  AND a.[Long] IS NOT NULL
  AND a.[Lat] BETWEEN -90 AND 90
  AND a.[Long] BETWEEN -180 AND 180;
GO

/* 3) Optional: add destination timezone column on Airport table */
IF COL_LENGTH('[MDS].[mdm].[Airport]', 'TimeZone') IS NULL
BEGIN
    ALTER TABLE [MDS].[mdm].[Airport]
    ADD [TimeZone] NVARCHAR(64) NULL;
END
GO

/* 4) Update Airport.TimeZone from nearest GeoNames match */
UPDATE a
SET a.[TimeZone] = nn.timezone
FROM [MDS].[mdm].[Airport] a
CROSS APPLY (
    SELECT TOP (1)
        g.timezone
    FROM dbo.geonames_allcountries g
    WHERE g.timezone IS NOT NULL
    ORDER BY g.GeoPoint.STDistance(geography::Point(a.[Lat], a.[Long], 4326))
) nn
WHERE a.[TimeZone] IS NULL
  AND a.[Lat] IS NOT NULL
  AND a.[Long] IS NOT NULL
  AND a.[Lat] BETWEEN -90 AND 90
  AND a.[Long] BETWEEN -180 AND 180;
GO
