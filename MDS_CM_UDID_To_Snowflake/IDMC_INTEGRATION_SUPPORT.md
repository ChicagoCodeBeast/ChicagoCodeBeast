# IDMC Integration Support Documentation: MDS_CM_UDID_To_Snowflake

## Overview

This repository folder contains an Informatica Intelligent Data Management Cloud
(IDMC) export package for the `MDS_CM_UDID_To_Snowflake` integration.

Export package name:

- `MDS_CM_UDID_To_Snowflake-1776711226691`

Primary orchestration object:

- Taskflow `tf_MDS_CM_UDID`

---

## IDMC Assets Included

Based on `ContentsofExportPackage_MDS_CM_UDID_To_Snowflake-1776711226691.csv`
and `exportMetadata.v2.json`.

### Runtime and Connections

- **Secure Agent Group**: `DT_US_Secure_Agent` (`/SYS`)
- **Connection**: `US_Snowflake` (`/SYS`)
- **Connection**: `US_SQL_SERVER_MDS` (`/SYS`)

### Data Integration Container Objects

- **Project**: `Data _Integration` (`/Explore`)
- **Folder**: `MDS_CM_UDID_To_Snowflake` (`/Explore/Data _Integration`)

### Taskflow

- **Taskflow**: `tf_MDS_CM_UDID`

### Mapping Tasks (MTT)

- `mt_CM_Spotnana_Trip_API_Field`
- `mt_CM_STD_Ext_RPT_Field`
- `mt_UDID_MAPPING_CUSTOM`
- `mt_UDID_MAPPING_STANDARD`

### Mappings (DTEMPLATE)

- `m_CM_Spotnana_Trip_API_Field`
- `m_CM_STD_Ext_RPT_Field`
- `m_UDID_MAPPING_CUSTOM`
- `m_UDID_MAPPING_STANDARD`

---

## Repository File Map

- `exportMetadata.v2.json`  
  Export manifest containing object IDs, types, references, and metadata.
- `ContentsofExportPackage_MDS_CM_UDID_To_Snowflake-1776711226691.csv`  
  Flat asset inventory (path, object name, object type, object id).
- `Explore/Data _Integration/MDS_CM_UDID_To_Snowflake/tf_MDS_CM_UDID.TASKFLOW.xml`  
  Taskflow definition with service calls and output mappings.
- `Explore/Data _Integration/MDS_CM_UDID_To_Snowflake.Folder.json`  
  Folder-level metadata including parent location.
- `exportPackage.chksum`  
  Package checksum file from IDMC export.

---

## Runtime Behavior (Taskflow)

Taskflow `tf_MDS_CM_UDID` uses `ICSExecuteDataTask` service steps to invoke
four mapping tasks in **parallel**:

- `mt_CM_Spotnana_Trip_API_Field`
- `mt_CM_STD_Ext_RPT_Field`
- `mt_UDID_MAPPING_CUSTOM`
- `mt_UDID_MAPPING_STANDARD`

Observed taskflow execution settings for each service step:

- `Wait for Task to Complete = true`
- `Max Wait = 604800` seconds (7 days)
- `Task Type = MCT`
- `Has Inout Parameters = true`

Each branch captures operational output fields such as:

- `Run Id`, `Log Id`, `Task Id`
- `Task Status`
- `Success/Failed Source Rows`
- `Success/Failed Target Rows`
- `Start Time`, `End Time`
- `Error Message`, `Total Transformation Errors`, `First Error Code`
- InOut value `LastChgDateTime`

Taskflow branch behavior note:

- Branch `dt_CM_STD_Ext_RPT_Field` has `failOnNotRun = false` and
  `failOnFault = false`.
- The other three branches are configured with both flags set to `true`.

This setup is intended for centralized orchestration and run-level observability
across UDID-related mapping tasks.

---

## Deployment and Setup Checklist

## 1) Import package assets

Import the exported package artifacts into the target IDMC organization.

## 2) Validate runtime dependencies

After import, verify:

- `DT_US_Secure_Agent` is online and assigned.
- Connection objects are valid for the target environment:
  - `US_Snowflake`
  - `US_SQL_SERVER_MDS`
- Imported objects are located under:
  `/Explore/Data _Integration/MDS_CM_UDID_To_Snowflake`.

## 3) Confirm each mapping task configuration

For each mapping task:

- Verify source and target connection bindings for the intended environment.
- Validate runtime options and parameter defaults.
- Confirm the correct mapping is referenced.

## 4) Execute orchestration

Run `tf_MDS_CM_UDID` to trigger all configured mapping tasks in parallel, or
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
  Validate credentials, role/database access, and network reachability for
  referenced connections.
- **Secure Agent unavailable**  
  Confirm `DT_US_Secure_Agent` health, assignment, and host connectivity.
- **Taskflow branch failure**  
  Use branch-level `Run Id` and `Log Id` from task output to isolate the
  failing mapping task.
- **Data mismatch between systems**  
  Compare per-task row counts and validate mapping logic in each mapping.
- **Incremental behavior issues**  
  Verify `LastChgDateTime` inout behavior per branch.

---

## Change Management Notes

When updating this integration:

1. Update mapping logic in the relevant mapping object (`m_*`).
2. Re-validate corresponding mapping task (`mt_*`) settings.
3. Confirm `tf_MDS_CM_UDID` still references the intended task set.
4. Re-export package artifacts and commit updated metadata files.

Keeping mappings, mapping tasks, taskflow references, and connection bindings
synchronized avoids post-deployment runtime failures.
