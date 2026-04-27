# GeoNames Documentation for Airport Timezone Mapping

This document explains how GeoNames data can be used to map airport coordinates to an IANA timezone in SQL Server.

## What GeoNames provides

GeoNames is a global geographic dataset.  
For timezone mapping, the most useful file is:

- `allCountries.txt` (tab-delimited)

Useful fields from this file:

- `geonameid`
- `latitude`
- `longitude`
- `timezone`

`timezone` is typically an IANA timezone string such as:

- `America/Chicago`
- `Europe/London`
- `Asia/Kolkata`

## Data source

- GeoNames website: `https://www.geonames.org/`
- Download portal: `https://download.geonames.org/export/dump/`

## SQL Server integration approach

Use nearest-neighbor lookup:

1. Load `allCountries.txt` into `dbo.geonames_allcountries`
2. Add computed `geography` point column (`GeoPoint`)
3. Add spatial index
4. For each airport, find nearest GeoNames point and assign `timezone`

This approach is fast and practical for airport datasets.

## Airport table used in this repository context

```sql
SELECT
    Name,
    [Lat],
    [Long]
FROM [MDS].[mdm].[Airport];
```

## Example: spatial setup

```sql
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
```

## Example: preview timezone matches

```sql
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
```

## Example: populate `[TimeZone]`

```sql
IF COL_LENGTH('[MDS].[mdm].[Airport]', 'TimeZone') IS NULL
BEGIN
    ALTER TABLE [MDS].[mdm].[Airport]
    ADD [TimeZone] NVARCHAR(64) NULL;
END;

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
```

## Accuracy notes

- This method uses nearest GeoNames point, not polygon boundaries.
- Results are usually correct for airports but may be wrong near timezone borders.
- Keep and review nearest distance (`distance_m`) for quality control.
- For strict boundary accuracy, use timezone boundary polygons.

## Related files in this repository

- `SQL/TimeZone/sqlserver-airport-timezone-from-geonames.sql`
- `SQL/TimeZone/geonames-usage.md`
- `SQL/TimeZone/conversation-log.md`
