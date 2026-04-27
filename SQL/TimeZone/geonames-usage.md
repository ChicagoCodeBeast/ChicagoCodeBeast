# GeoNames Timezone Lookup (SQL Server)

This guide documents how to use GeoNames `allCountries.txt` with SQL Server to map airport latitude/longitude to an IANA timezone (for example, `America/Chicago`).

---

## 1) Data source

- GeoNames download page: `https://www.geonames.org/`
- File used: `allCountries.txt` (tab-delimited)

Relevant columns used in this workflow:
- `latitude`
- `longitude`
- `timezone`

---

## 2) Target airport table

Current airport source:

```sql
SELECT
    Name,
    [Lat],
    [Long]
FROM [MDS].[mdm].[Airport];
```

Assumption:
- `[Lat]` and `[Long]` are decimal numeric values.

---

## 3) SQL workflow summary

1. Load GeoNames rows into `dbo.geonames_allcountries`.
2. Add computed `geography` point on GeoNames rows.
3. Create a spatial index on the computed point.
4. For each airport row, pick the nearest GeoNames row and use its `timezone`.

This is a nearest-neighbor method. It is usually good, but can be incorrect close to timezone borders.

---

## 4) Core query pattern

Preview timezone mapping for each airport:

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

## 5) Update airport timezone column

If needed, add destination column:

```sql
ALTER TABLE [MDS].[mdm].[Airport]
ADD [TimeZone] NVARCHAR(64) NULL;
```

Populate timezone from nearest GeoNames row:

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

## 6) Performance recommendations

- Keep a computed point column on GeoNames:

```sql
ALTER TABLE dbo.geonames_allcountries
ADD GeoPoint AS geography::Point(latitude, longitude, 4326) PERSISTED;
```

- Add a spatial index:

```sql
CREATE SPATIAL INDEX IX_geonames_allcountries_GeoPoint
ON dbo.geonames_allcountries(GeoPoint)
USING GEOGRAPHY_AUTO_GRID;
```

---

## 7) Accuracy considerations

- Nearest-point matching may fail near timezone boundaries.
- Record and review `distance_m` for quality control.
- Optionally enforce a max distance threshold and manually review outliers.
- For strict boundary accuracy, consider a timezone polygon dataset.

---

## 8) Repository files

- SQL implementation script: `SQL/TimeZone/sqlserver-airport-timezone-from-geonames.sql`
- Conversation context log: `SQL/TimeZone/conversation-log.md`

