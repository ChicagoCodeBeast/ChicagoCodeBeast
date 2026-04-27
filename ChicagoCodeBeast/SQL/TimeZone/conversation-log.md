# Airport Timezone Data Conversation Log

Date context in session: Tuesday Mar 24, 2026 through Monday Apr 27, 2026 (UTC)

## Transcript

### User
Is there any data that can translate airpot codes to timezone

### Assistant
Not in this repository. It only contains a README and no airport/timezone dataset files. Suggested common sources: OpenFlights, OurAirports + timezone derivation, and GeoNames.

---

### User
what is OpenFlights airports.dat

### Assistant
Explained that `airports.dat` is a CSV-like airport reference file containing fields such as IATA, ICAO, coordinates, UTC offset, DST, and IANA timezone (for example `America/Chicago`), with `\\N` used for missing values.

---

### User
can I download a copy of OpenFlights airports.dat

### Assistant
Confirmed yes and provided direct download URL and curl command.

---

### User
how up to date is openflights data

### Assistant
Verified from OpenFlights docs and GitHub history that the GitHub copy is a sporadically updated static snapshot and that `airports.dat` latest commit date in that repo was 2019-05-13.

---

### User
how can i use OurAirports

### Assistant
Provided download approach, key columns, and explained deriving timezone from coordinates since timezone is typically not a first-class field in the main airports CSV usage pattern.

---

### User
what is timezonefinder

### Assistant
Explained that `timezonefinder` is a Python library that maps latitude/longitude to an IANA timezone name.

---

### User
how can i use latitude and longitude I have stored in the database to find the timezone using geonames.org allcountries.txt

### Assistant
Provided SQL workflow: load GeoNames data, build spatial point/index, nearest-neighbor lookup, and batch update pattern.

---

### User
i need a sql server version

### Assistant
Provided SQL Server-specific DDL/DML using `geography::Point`, spatial index, single lookup, and batch update examples.

---

### User
how can I use my table which is like this
SELECT
       Name,
       [Lat]
      ,[Long]
FROM [MDS].[mdm].[Airport]
lat and long are both decimal

### Assistant
Provided direct SQL Server query and update statements tailored to `[MDS].[mdm].[Airport]` with `OUTER APPLY`/`CROSS APPLY` nearest timezone match logic.

---

### User
can you commit this to my github

### Assistant
Added and pushed SQL script:
- `sqlserver-airport-timezone-from-geonames.sql`
- Commit: `d11634c`
- Branch: `cursor/airport-timezone-data-33a5`

---

### User
commit this conversation as an md as well as well as all sql files into folder SQL/TimeZone

### Assistant
Created `SQL/TimeZone/`, added the conversation log markdown, and moved SQL files into that folder.
