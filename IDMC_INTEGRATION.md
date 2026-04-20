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
