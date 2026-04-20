# IDMC Integration Documentation: Snowflake to MDS

## Overview

This repository contains an Informatica Intelligent Data Management Cloud (IDMC)
export package for loading customer data from Snowflake into MDS.

The package name is:

- `Snowflake_To_MDS-1776707133925`

Primary integration flow:

1. Taskflow `tf_CM_T_CUSTOMER` starts.
2. Taskflow runs mapping task `mt_CM_T_CUSTOMER`.
3. Mapping task executes mapping `m_CM_T_CUSTOMER`.
4. Data is moved from Snowflake source connection to MDS target connection.

---

## IDMC Assets Included

From `ContentsofExportPackage_Snowflake_To_MDS-1776707133925.csv` and
`exportMetadata.v2.json`:

### Connections and Runtime

- **Source Connection**: `US_Snowflake` (`/SYS`)
- **Target Connection**: `US_DW_SnowflakeToMDS` (`/SYS`)
- **Secure Agent Group**: `DT_US_Secure_Agent` (`/SYS`)

### Data Integration Objects

- **Project**: `Data _Integration` (`/Explore`)
- **Folder**: `Snowflake_To_MDS` (`/Explore/Data _Integration`)
- **Mapping**: `m_CM_T_CUSTOMER`
- **Mapping Task**: `mt_CM_T_CUSTOMER`
- **Taskflow**: `tf_CM_T_CUSTOMER`

---

## Repository File Map

- `exportMetadata.v2.json`  
  Export manifest with object names, IDs, types, and references.
- `ContentsofExportPackage_Snowflake_To_MDS-1776707133925.csv`  
  Flat list of exported assets.
- `Explore/Data _Integration/Snowflake_To_MDS/tf_CM_T_CUSTOMER.TASKFLOW.xml`  
  Taskflow XML with execution settings and task references.
- `Explore/Data _Integration/Snowflake_To_MDS.Folder.json`  
  Folder metadata in IDMC object format.

---

## Runtime Behavior (Taskflow)

The taskflow `tf_CM_T_CUSTOMER` calls the IDMC service
`ICSExecuteDataTask` to run `mt_CM_T_CUSTOMER`.

Notable execution parameters in the taskflow XML:

- `Wait for Task to Complete = true`
- `Max Wait = 604800` (seconds; 7 days)
- `Task Type = MCT`
- InOut parameter support enabled (`Has Inout Parameters = true`)

Task output fields captured include:

- Run identifiers (`Run Id`, `Log Id`, `Task Id`)
- Status (`Task Status`)
- Row counts (success/failure source and target rows)
- Timing (`Start Time`, `End Time`)
- Error details (`Error Message`, `First Error Code`, transformation errors)
- InOut value `LastChgDateTime`

This design allows the taskflow to wait for completion and return operational
details useful for monitoring and restart logic.

---

## Deployment and Setup in IDMC

## 1) Import package assets

Import the package into the target IDMC org using the exported artifacts in this
repository.

## 2) Validate/assign runtime dependencies

After import, verify that:

- `US_Snowflake` points to the correct Snowflake environment.
- `US_DW_SnowflakeToMDS` points to the correct MDS target.
- `DT_US_Secure_Agent` is available and healthy.
- Imported objects remain under:
  `/Explore/Data _Integration/Snowflake_To_MDS`.

## 3) Confirm mapping task configuration

Open `mt_CM_T_CUSTOMER` and verify:

- Source/target connections are bound correctly.
- Any parameter defaults (including `LastChgDateTime`) are appropriate.
- Session/task options match environment expectations.

## 4) Execute the taskflow

Run `tf_CM_T_CUSTOMER` for orchestrated execution, or schedule it based on your
load cadence.

---

## Operations and Monitoring

For each run, monitor:

- Taskflow run status
- Mapping task status
- Source/target row counts
- Start/end timestamps and duration
- Error message and first error code when failures occur

Recommended operational checks:

- Alert on non-success `Task Status`.
- Track row count anomalies against historical baselines.
- Persist `Run Id` and `Log Id` for troubleshooting.

---

## Troubleshooting Quick Guide

- **Connection failures**: Validate credentials/networking for both connections.
- **Agent unavailable**: Confirm `DT_US_Secure_Agent` is online and assigned.
- **Task timeout**: Review run duration and adjust schedule/volume strategy.
- **Data discrepancies**: Compare source and target row counts from run outputs.
- **Incremental load issues**: Verify `LastChgDateTime` inout handling.

---

## Change Management Notes

When modifying this integration:

1. Update mapping `m_CM_T_CUSTOMER` first.
2. Re-validate `mt_CM_T_CUSTOMER` task settings.
3. Confirm `tf_CM_T_CUSTOMER` parameter mappings still match task outputs.
4. Re-export package artifacts and commit updated metadata files.

Keeping taskflow, mapping task, and connection metadata synchronized prevents
runtime mismatch errors after deployment.

---

## Additional Integration: MDS_CM_UDID_To_Snowflake

### Overview

This repository also contains an Informatica Intelligent Data Management Cloud
(IDMC) export package for loading UDID-related data from MDS into Snowflake.

The package name is:

- `MDS_CM_UDID_To_Snowflake-1776711226691`

Primary integration flow:

1. Taskflow `tf_MDS_CM_UDID` starts.
2. The taskflow runs four mapping tasks in parallel.
3. Each mapping task executes its mapped data template.
4. Data is moved through `US_SQL_SERVER_MDS` and `US_Snowflake` connections.

---

### IDMC Assets Included

From `ContentsofExportPackage_MDS_CM_UDID_To_Snowflake-1776711226691.csv` and
`MDS_CM_UDID_To_Snowflake/exportMetadata.v2.json`:

#### Connections and Runtime

- **Connection**: `US_Snowflake` (`/SYS`)
- **Connection**: `US_SQL_SERVER_MDS` (`/SYS`)
- **Secure Agent Group**: `DT_US_Secure_Agent` (`/SYS`)

#### Data Integration Objects

- **Project**: `Data _Integration` (`/Explore`)
- **Folder**: `MDS_CM_UDID_To_Snowflake` (`/Explore/Data _Integration`)
- **Taskflow**: `tf_MDS_CM_UDID`

Mapping tasks:

- `mt_CM_Spotnana_Trip_API_Field`
- `mt_CM_STD_Ext_RPT_Field`
- `mt_UDID_MAPPING_CUSTOM`
- `mt_UDID_MAPPING_STANDARD`

Mappings:

- `m_CM_Spotnana_Trip_API_Field`
- `m_CM_STD_Ext_RPT_Field`
- `m_UDID_MAPPING_CUSTOM`
- `m_UDID_MAPPING_STANDARD`

---

### Runtime Behavior (Taskflow)

The taskflow `tf_MDS_CM_UDID` calls `ICSExecuteDataTask` service steps for the
four mapping tasks in parallel.

Observed execution settings:

- `Wait for Task to Complete = true`
- `Max Wait = 604800` seconds (7 days)
- `Task Type = MCT`
- `Has Inout Parameters = true`

Task outputs captured per branch include run identifiers, status, row counts,
timing fields, error fields, and inout value `LastChgDateTime`.

Branch behavior note:

- `dt_CM_STD_Ext_RPT_Field` has `failOnNotRun = false` and `failOnFault = false`.
- Other branches are configured with both values set to `true`.

---

### Repository File Map (UDID Package)

- `MDS_CM_UDID_To_Snowflake/exportMetadata.v2.json`
- `MDS_CM_UDID_To_Snowflake/ContentsofExportPackage_MDS_CM_UDID_To_Snowflake-1776711226691.csv`
- `MDS_CM_UDID_To_Snowflake/Explore/Data _Integration/MDS_CM_UDID_To_Snowflake/tf_MDS_CM_UDID.TASKFLOW.xml`
- `MDS_CM_UDID_To_Snowflake/Explore/Data _Integration/MDS_CM_UDID_To_Snowflake.Folder.json`
- `MDS_CM_UDID_To_Snowflake/exportPackage.chksum`

Detailed support doc:

- `MDS_CM_UDID_To_Snowflake/IDMC_INTEGRATION_SUPPORT.md`
