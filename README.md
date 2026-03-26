- 👋 Hi, I’m @ChicagoCodeBeast
- 👀 I’m interested in ...
- 🌱 I’m currently learning ...
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me ...
- ⚡ Fun fact: ...

<!---
ChicagoCodeBeast/ChicagoCodeBeast is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

## Build airport code + timezone CSV from OurAirports

This repo includes `ourairports_to_timezones.py`, which downloads `airports.csv`
from OurAirports and derives IANA timezone names from airport latitude/longitude.

### Install dependency

```bash
python3 -m pip install timezonefinder
```

### Run

```bash
python3 ourairports_to_timezones.py
```

Default output: `ourairports-airport-timezones.csv` with columns:

- `iata_code`
- `icao_code`
- `timezone`

### Useful options

- Include extra metadata columns:

  ```bash
  python3 ourairports_to_timezones.py --include-metadata
  ```

- Set custom output path:

  ```bash
  python3 ourairports_to_timezones.py --output airport_timezones.csv
  ```

- Quick test with limited rows:

  ```bash
  python3 ourairports_to_timezones.py --limit 1000
  ```
