# Avenir UDID Mapping Regroup - Meeting Summary

- **Date:** April 22, 2026
- **Start Time:** 5:01 PM
- **End Time:** 5:32:55 PM
- **Duration:** 31m 55s

## Summary

The team confirmed that upstream UDID source-table changes are finalized, signed off, and already active. MDS now needs to implement matching schema updates and adjust ingestion so unit mapping data remains aligned. The scope discussed is focused on UDID unit mapping updates, with follow-on coordination needed for reporting and downstream consumers.

## Key Decisions

- Proceed now with MDS-side changes; no additional waiting on source-system design.
- Add required attributes in both **Standard** and **Custom** unit mapping entities.
- Keep current field names for now (with internal naming conventions), even though some names are confusing; any relabeling can happen later.
- Defer dev-environment requests until needed.

## Action Items

1. **Sean**
   - Add 3 new MDS attributes for UDID mapping in both Standard and Custom entities:
     - `field_logic_override_1`
     - `spot_trip_atpi_field_2`
     - `field_logic_override_2`
   - Use standard underscore naming conventions.

2. **Sean**
   - Update ingestion/subscription flow so the 3 new columns are available downstream and loaded into Snowflake/bronze.
   - Confirm if any pipeline pause is required during rollout.

3. **Sean**
   - After implementation is complete, raise a ticket/notify downstream stakeholders (e.g., Rob/Graham/reporting side) about source-table schema changes.

4. **Sean**
   - Request **read-only** Central Command access to unit mapping for:
     - Sean
     - Hampton

5. **Andrew**
   - Prioritize and complete testing for the blocked task: initial silver modeling for Trips ATPI field definition.

6. **Amanda**
   - Mark Sean as reviewer/tester on the standard external reporting field materialized-view ticket.
   - Move that ticket to **Done** (review approved).

7. **Andrew**
   - Coordinate with David to formally add Amanda and Hampton to the project/meeting distribution.

## Next Steps

1. Complete access requests.
2. Implement the 3 MDS attributes in both entities.
3. Update ingestion and Snowflake/bronze references.
4. Validate known production cases using the secondary Spot Trip field.
5. Notify downstream teams after implementation.
6. In parallel, unblock Trips ATPI modeling so dependent work can proceed.
