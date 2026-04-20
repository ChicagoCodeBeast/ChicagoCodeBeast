# IDMC Integration Support Documentation: MDS_SM_SupplierManagement_To_Snowflake

## Overview

This repository folder contains an Informatica Intelligent Data Management Cloud
(IDMC) export package for the `MDS_SM_SupplierManagement_To_Snowflake`
integration.

Export package name:

- `MDS_SM_SupplierManagement_To_Snowflake-1776711807250`

Primary orchestration object:

- Taskflow `tf_Load_MDS_SM`

---

## IDMC Assets Included

Based on `ContentsofExportPackage_MDS_SM_SupplierManagement_To_Snowflake-1776711807250.csv`
and `exportMetadata.v2.json`.

### Runtime and Connections

- **Secure Agent Group**: `DT_US_Secure_Agent` (`/SYS`)
- **Connection**: `US_Snowflake` (`/SYS`)
- **Connection**: `US_SQL_SERVER_MDS` (`/SYS`)

### Data Integration Container Objects

- **Project**: `Data _Integration` (`/Explore`)
- **Folder**: `MDS_SM_SupplierManagement_To_Snowflake`
  (`/Explore/Data _Integration`)

### Taskflow

- **Taskflow**: `tf_Load_MDS_SM`

### Mapping Tasks (MTT)

- `mt_SM_Airport`
- `mt_SM_Airport_City`
- `mt_SM_City`
- `mt_SM_Country`
- `mt_SM_DT_Region`
- `mt_SM_GDS`
- `mt_SM_GDS_Hotel_Property`
- `mt_SM_GDS_Rate_Code`
- `mt_SM_Hotel_Chain`
- `mt_SM_Hotel_Master_Chain`
- `mt_SM_Hotel_Property`
- `mt_SM_IATA_Location`
- `mt_SM_Rate_Category`
- `mt_SM_State_Province`
- `mt_SM_World_Region`

### Mappings (DTEMPLATE)

- `m_SM_Airport`
- `m_SM_Airport_City`
- `m_SM_City`
- `m_SM_Country`
- `m_SM_DT_Region`
- `m_SM_GDS`
- `m_SM_GDS_Hotel_Property`
- `m_SM_GDS_Rate_Code`
- `m_SM_Hotel_Chain`
- `m_SM_Hotel_Master_Chain`
- `m_SM_Hotel_Property`
- `m_SM_IATA_Location`
- `m_SM_Rate_Category`
- `m_SM_State_Province`
- `m_SM_World_Region`

---

## Repository File Map

- `exportMetadata.v2.json`  
  Export manifest containing object IDs, types, references, and metadata.
- `ContentsofExportPackage_MDS_SM_SupplierManagement_To_Snowflake-1776711807250.csv`  
  Flat asset inventory (path, object name, object type, object id).
- `Explore/Data _Integration/MDS_SM_SupplierManagement_To_Snowflake/tf_Load_MDS_SM.TASKFLOW.xml`  
  Taskflow definition with service calls and output mappings.
- `Explore/Data _Integration/MDS_SM_SupplierManagement_To_Snowflake.Folder.json`  
  Folder-level metadata including parent location.
- `Explore/Data _Integration.Project.json`  
  Project metadata for `Data _Integration`.
- `exportPackage.chksum`  
  Package checksum file from IDMC export.

---

## Runtime Behavior (Taskflow)

Taskflow `tf_Load_MDS_SM` uses `ICSExecuteDataTask` service steps to invoke
fifteen mapping tasks in **parallel**.

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

Branch behavior note:

- All task references in this taskflow are configured with:
  - `failOnNotRun = true`
  - `failOnFault = true`

This setup provides centralized orchestration and run-level observability
across all supplier management data tasks.

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
  `/Explore/Data _Integration/MDS_SM_SupplierManagement_To_Snowflake`.

## 3) Confirm each mapping task configuration

For each `mt_SM_*` mapping task:

- Verify source and target connection bindings for the intended environment.
- Validate runtime options and parameter defaults.
- Confirm the correct mapping (`m_SM_*`) is referenced.

## 4) Execute orchestration

Run `tf_Load_MDS_SM` to trigger all configured mapping tasks in parallel, or
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
- **Taskflow branch failure**  
  Use branch-level `Run Id` and `Log Id` from task output to isolate the
  failing mapping task.
- **Data mismatch between systems**  
  Compare per-task row counts and validate mapping logic in each `m_SM_*`.
- **Incremental behavior issues**  
  Verify `LastChgDateTime` inout behavior per branch.

---

## Change Management Notes

When updating this integration:

1. Update mapping logic in the relevant `m_SM_*` object.
2. Re-validate corresponding `mt_SM_*` task settings.
3. Confirm `tf_Load_MDS_SM` still references the intended task set.
4. Re-export package artifacts and commit updated metadata files.

Keeping mappings, mapping tasks, taskflow references, and connection bindings
synchronized avoids post-deployment runtime failures.
