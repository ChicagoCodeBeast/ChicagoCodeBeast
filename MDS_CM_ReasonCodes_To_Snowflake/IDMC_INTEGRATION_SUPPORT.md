# IDMC Integration Support Documentation: MDS_CM_ReasonCodes_To_Snowflake

## Overview

This repository folder contains an Informatica Intelligent Data Management Cloud
(IDMC) export package for the `MDS_CM_ReasonCodes_To_Snowflake` integration.

Export package name:

- `MDS_CM_ReasonCodes_To_Snowflake-1776710572449`

Primary orchestration object:

- Taskflow `tf_RAW_ReasonCode`

Folder description in metadata:

- "Pipelines to ingest Reason Code data from MDS into Snowlfake RAW.MDS_CM"

---

## IDMC Assets Included

Based on `ContentsofExportPackage_MDS_CM_ReasonCodes_To_Snowflake-1776710572449.csv`
and `exportMetadata.v2.json`.

### Runtime and Connections

- **Secure Agent Group**: `DT_US_Secure_Agent` (`/SYS`)
- **Connection**: `CAN_Snowflake` (`/SYS`)
- **Connection**: `US_Snowflake` (`/SYS`)
- **Connection**: `US_SQL_SERVER_MDS` (`/SYS`)

### Data Integration Container Objects

- **Project**: `Data _Integration` (`/Explore`)
- **Folder**: `MDS_CM_ReasonCodes_To_Snowflake`
  (`/Explore/Data _Integration`)

### Taskflow

- **Taskflow**: `tf_RAW_ReasonCode`

### Mapping Tasks (MTT)

- `mt_V_SL_AIR_CODES_CLIENT_SPECIFIC`
- `mt_V_SL_AIR_CODES_STANDARD`
- `mt_V_SL_CAR_CODES_CLIENT_SPECIFIC`
- `mt_V_SL_CAR_CODES_STANDARD`
- `mt_V_SL_CODE_TYPES`
- `mt_V_SL_HOTEL_CODES_CLIENT_SPECIFIC`
- `mt_V_SL_HOTEL_CODES_STANDARD`

### Mappings (DTEMPLATE)

- `m_V_SL_AIR_CODES_CLIENT_SPECIFIC`
- `m_V_SL_AIR_CODES_STANDARD`
- `m_V_SL_CAR_CODES_CLIENT_SPECIFIC`
- `m_V_SL_CAR_CODES_STANDARD`
- `m_V_SL_CODE_TYPES`
- `m_V_SL_HOTEL_CODES_CLIENT_SPECIFIC`
- `m_V_SL_HOTEL_CODES_STANDARD`

---

## Repository File Map

- `exportMetadata.v2.json`  
  Export manifest containing object IDs, types, references, and metadata.
- `ContentsofExportPackage_MDS_CM_ReasonCodes_To_Snowflake-1776710572449.csv`  
  Flat asset inventory (path, object name, object type, object id).
- `Explore/Data _Integration/MDS_CM_ReasonCodes_To_Snowflake/tf_RAW_ReasonCode.TASKFLOW.xml`  
  Taskflow definition with service calls and output mappings.
- `Explore/Data _Integration/MDS_CM_ReasonCodes_To_Snowflake.Folder.json`  
  Folder-level metadata including parent location and description.
- `exportPackage.chksum`  
  Package checksum file from IDMC export.

---

## Runtime Behavior (Taskflow)

Taskflow `tf_RAW_ReasonCode` uses `ICSExecuteDataTask` service steps to invoke
seven mapping tasks in **parallel**.

Observed taskflow execution settings for each service step:

- `Wait for Task to Complete = true`
- `Max Wait = 604800` seconds (7 days)
- `Task Type = MCT`
- `Has Inout Parameters = false`

Each branch captures operational output fields such as:

- `Run Id`, `Log Id`, `Task Id`
- `Task Status`
- `Success/Failed Source Rows`
- `Success/Failed Target Rows`
- `Start Time`, `End Time`
- `Error Message`, `Total Transformation Errors`, `First Error Code`

This setup is intended for centralized orchestration and run-level observability
across all reason-code data tasks.

---

## Deployment and Setup Checklist

## 1) Import package assets

Import the exported package artifacts into the target IDMC organization.

## 2) Validate runtime dependencies

After import, verify:

- `DT_US_Secure_Agent` is online and assigned.
- Connection objects are valid for the target environment:
  - `CAN_Snowflake`
  - `US_Snowflake`
  - `US_SQL_SERVER_MDS`
- Imported objects are located under:
  `/Explore/Data _Integration/MDS_CM_ReasonCodes_To_Snowflake`.

## 3) Confirm each mapping task configuration

For each `mt_V_SL_*` mapping task:

- Verify connection bindings (source/target) for the intended environment.
- Validate runtime options and parameter defaults.
- Confirm the correct mapping (`m_V_SL_*`) is referenced.

## 4) Execute orchestration

Run `tf_RAW_ReasonCode` to trigger all configured mapping tasks in parallel, or
schedule based on operational cadence.

---

## Operations and Monitoring

For each run, monitor:

- Taskflow status
- Individual mapping task status
- Source and target row counts
- Start/end timestamps and duration
- Error message and first error code for failures

Recommended support actions:

- Alert on non-success `Task Status`.
- Track row-count anomalies against normal baselines.
- Retain `Run Id` and `Log Id` for incident troubleshooting.

---

## Troubleshooting Quick Guide

- **Connection/authentication failure**  
  Validate credentials, role/database access, and network reachability for all
  referenced connections.
- **Secure Agent unavailable**  
  Confirm `DT_US_Secure_Agent` health, assignment, and host connectivity.
- **Taskflow appears hung/slow**  
  Review long-running mapping tasks and verify workload sizing on the agent.
- **Data mismatch between systems**  
  Compare per-task row counts and validate mapping logic in each `m_V_SL_*`.
- **One branch fails while others succeed**  
  Use branch-level `Run Id` and `Log Id` from task output to isolate the failing
  mapping task.

---

## Change Management Notes

When updating this integration:

1. Update mapping logic in the relevant `m_V_SL_*` object.
2. Re-validate corresponding `mt_V_SL_*` task settings.
3. Confirm `tf_RAW_ReasonCode` still references the intended task set.
4. Re-export package artifacts and commit updated metadata files.

Keeping mappings, mapping tasks, taskflow references, and connection bindings
synchronized avoids post-deployment runtime failures.
