# GeoNames Timezone Lookup (SQL Server)

This guide explains how to use GeoNames `allCountries.txt` to map airport coordinates in `[MDS].[mdm].[Airport]` to an IANA timezone (for example, `America/Chicago`).

## Quick start

1. Load `allCountries.txt` into `dbo.geonames_allcountries`.
2. Add computed `GeoPoint` and a spatial index.
3. Run the preview query to inspect matches and distances.
4. Populate `[MDS].[mdm].[Airport].[TimeZone]` from nearest matches.

---

## 1) Data source and required fields

- GeoNames: `https://www.geonames.org/`
- File: `allCountries.txt` (tab-delimited, UTF-8)
- Fields used:
  - `latitude`
  - `longitude`
  - `timezone`

Your airport table shape:

```sql
SELECT
    Name,
    [Lat],
    [Long]
FROM [MDS].[mdm].[Airport];
```

Assumption: `[Lat]` and `[Long]` are decimal numeric values.

---

## 2) Optional load example (if table is not already populated)

If you already have `dbo.geonames_allcountries`, skip this section.

```sql
-- Example structure (minimum needed for timezone matching)
CREATE TABLE dbo.geonames_allcountries (
    geonameid BIGINT NOT NULL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    timezone NVARCHAR(64) NULL
);
```

Load data (example only; adjust path and full schema as needed):

```sql
BULK INSERT dbo.geonames_allcountries
FROM 'C:\data\allCountries.txt'
WITH (
    FIELDTERMINATOR = '\t',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK
);
```

---

## 3) Spatial setup (recommended)

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

---

## 4) Preview matches before updating

Use this to validate quality and capture distance in meters:

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

---

## 5) Update airport timezone

Add destination column if needed:

```sql
IF COL_LENGTH('[MDS].[mdm].[Airport]', 'TimeZone') IS NULL
BEGIN
    ALTER TABLE [MDS].[mdm].[Airport]
    ADD [TimeZone] NVARCHAR(64) NULL;
END
```

Populate timezone from nearest GeoNames point:

```sql
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

---

## 6) Recommended quality checks

Review far-distance matches (possible low-confidence results):

```sql
SELECT TOP (200)
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
WHERE nn.distance_m > 50000 -- 50 km threshold example
ORDER BY nn.distance_m DESC;
```

---

## 7) Accuracy notes

- This method is nearest-point matching, not polygon boundary matching.
- It is usually effective for airports, but can be wrong near timezone borders.
- Keep `distance_m` for QA and investigate outliers.
- For strict boundary accuracy, use timezone boundary polygons.

---

## 8) Related repository files

- SQL implementation script: `SQL/TimeZone/sqlserver-airport-timezone-from-geonames.sql`
- Conversation log: `SQL/TimeZone/conversation-log.md`

