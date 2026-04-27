# GeoNames `timeZones.txt` Offset Documentation

This document explains how to use GeoNames `timeZones.txt` to get UTC offsets, and what each offset value means.

Source file:
- `https://download.geonames.org/export/dump/timeZones.txt`

---

## 1) What `timeZones.txt` contains

`timeZones.txt` is a timezone reference table keyed by IANA timezone ID (for example, `America/Chicago`).

Header pattern (example year):

```
CountryCode  TimeZoneId  GMT offset 1. Jan 2026  DST offset 1. Jul 2026  rawOffset (independant of DST)
```

The year in the Jan/Jul column labels can change as GeoNames refreshes the file.

---

## 2) Column meanings

For each row:

- `CountryCode`
  - ISO country code (for example, `US`, `GB`, `AU`).
  - Not unique by itself.

- `TimeZoneId`
  - IANA timezone ID (for example, `America/Chicago`, `Europe/London`).
  - This is the key used to join from airport timezone values.

- `GMT offset 1. Jan <year>`
  - UTC offset (hours) for **January 1** of that year.
  - Includes any DST that may be active on that date in that location.

- `DST offset 1. Jul <year>`
  - UTC offset (hours) for **July 1** of that year.
  - Includes any DST that may be active on that date in that location.

- `rawOffset (independant of DST)`
  - Base offset without DST adjustments.
  - This is the "standard time" offset.

Notes:
- Offsets are decimal hours and may be fractional (`5.5`, `5.75`, etc.).
- Jan/Jul values are date snapshots, not a full DST rule engine.

---

## 3) How this is used with airport timezone mapping

Typical flow in this repository:

1. Use GeoNames `allCountries.txt` (or nearest-point match) to assign airport `TimeZone` as IANA ID.
2. Join airport `TimeZone` to `timeZones.txt` `TimeZoneId`.
3. Read offset columns from `timeZones.txt` as needed.

This gives you:
- a baseline offset (`rawOffset`)
- two seasonal samples (`Jan`, `Jul`) for quick reporting

---

## 4) SQL Server staging table for `timeZones.txt`

```sql
CREATE TABLE dbo.geonames_timezones (
    CountryCode      CHAR(2)       NOT NULL,
    TimeZoneId       NVARCHAR(64)  NOT NULL,
    GmtOffsetJan     DECIMAL(6,2)  NULL, -- "GMT offset 1. Jan <year>"
    DstOffsetJul     DECIMAL(6,2)  NULL, -- "DST offset 1. Jul <year>"
    RawOffset        DECIMAL(6,2)  NULL  -- "rawOffset (independant of DST)"
);
```

Load example (tab-delimited, skip header row):

```sql
BULK INSERT dbo.geonames_timezones
FROM 'C:\data\timeZones.txt'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = '\t',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK
);
```

---

## 5) Join offsets to airport table

Assuming:
- Airport timezone column is `[MDS].[mdm].[Airport].[TimeZone]`
- Value is IANA ID from GeoNames (for example, `America/Chicago`)

```sql
SELECT
    a.Name,
    a.[Lat],
    a.[Long],
    a.[TimeZone]                      AS AirportTimeZoneId,
    tz.RawOffset                      AS UtcOffsetStandardHours,
    tz.GmtOffsetJan                   AS UtcOffsetJanHours,
    tz.DstOffsetJul                   AS UtcOffsetJulHours
FROM [MDS].[mdm].[Airport] a
LEFT JOIN dbo.geonames_timezones tz
    ON tz.TimeZoneId = a.[TimeZone];
```

---

## 6) Choosing which offset to use

Use case guidance:

- If you need a stable base offset:
  - use `RawOffset`

- If you need simple seasonal display:
  - show both `GmtOffsetJan` and `DstOffsetJul`

- If you need exact offset for an arbitrary timestamp:
  - do not rely only on Jan/Jul snapshot columns
  - use a timezone rules engine (or SQL Server `AT TIME ZONE` with Windows timezone mapping)

`timeZones.txt` is best treated as a reference lookup, not as a complete DST transition schedule.

---

## 7) Practical interpretation examples

- `America/Chicago`: `RawOffset=-6`, Jan often `-6`, Jul often `-5`
- `Asia/Kathmandu`: `RawOffset=5.75`, Jan/Jul both `5.75` (no DST)
- `Australia/Sydney`: Jan may be `11`, Jul `10` (southern hemisphere season reversal)

This is why Jan/Jul should be interpreted as date-specific snapshots, not "always standard vs DST."
