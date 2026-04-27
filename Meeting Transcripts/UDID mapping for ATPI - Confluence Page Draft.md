# UDID Mapping for ATPI – Meeting Summary and Action Plan

## Meeting Context
- **Topic:** UDID mapping approach for ATPI customers
- **Primary goal:** Align on a scalable mapping approach for ATPI (including standalone ATPI customers) and identify implementation tasks across MDS, Snowflake, and CentComm.
- **Participants referenced in transcript:** Andrew Nielsen, Sean Tomas, Norma Barrett, Cindy Barr, Nadine Carson, Amanda Albers, Hamta Fakhravar

## Executive Summary
The team agreed to stop treating standalone ATPI customers as a special case and move to the same core mapping model used elsewhere: map primarily at the **customer rollup** level in MDS, then apply **customer-level overrides** only when required (for example, known exceptions like McDonald's).

In the short term, ATPI customer IDs will be added **manually in MDS** and tied to the correct customer rollups. This avoids continuing the temporary workaround of creating placeholder US customer IDs just to force mappings.

This decision introduces scope across multiple areas:
- MDS customer entity/process changes
- Customer sync behavior changes (to protect manually added records)
- Reload/review of UDID mappings
- Push pipeline updates into CentComm (flexi fields + new ATPI custom table path)
- Data engineering updates for downstream Snowflake consumption

## Key Decisions Made
1. **Adopt one approach for all ATPI customers**
   - Do not handle standalone ATPI customers differently from non-standalone/global ATPI customers.

2. **Use customer rollup as default mapping level**
   - ATPI customer IDs are tied to customer rollups; UDID/unit mappings should be inherited from rollup where possible.

3. **Allow customer-level overrides when needed**
   - Keep override capability for exceptions (explicitly discussed: McDonald's scenario).

4. **Manual MDS entry is the immediate path**
   - ATPI customer IDs will be manually created/maintained in MDS for now.

5. **Separate ATPI push path in CentComm**
   - Continue existing flexi-field flow for non-ATPI/core data.
   - Add a separate custom-table flow for ATPI data.

6. **Reload and validate mappings before test/go-live**
   - Reload process includes manual decision points (rollup vs customer-level mapping).

## Action Items
| # | Action | Proposed Owner(s) | Priority | Notes |
|---|---|---|---|---|
| 1 | Document and circulate meeting summary | Sean Tomas | High | Explicitly requested and accepted in meeting |
| 2 | Add field in MDS customer entity to distinguish synced vs manually managed records (name TBD) | Andrew Nielsen + Sean Tomas | High | Needed for safe business rules and sync behavior |
| 3 | Pre-populate the new MDS field for existing records | Sean Tomas / MDS team | High | Called out with entity change task |
| 4 | Update customer sync process so it does not overwrite manually added ATPI records | Sean Tomas | High | Mentioned as a minor but required sync change |
| 5 | Review/update MDS business rules so ATPI creation does not require irrelevant fields | Sean Tomas + Andrew Nielsen | High | Reduce manual burden for ATPI-only records |
| 6 | Populate current ATPI customers from existing CentComm data into MDS | MDS/ops team (Andrew/Sean coordinating) | High | Required baseline load |
| 7 | Reload UDID mappings from production and re-evaluate rollup-vs-customer-level placement | Sean Tomas + Andrew Nielsen | High | Must be done before testing/go-live |
| 8 | Handle known exception mappings (e.g., McDonald's) with customer-level overrides | MDS team | Medium | Most others expected to inherit from rollup |
| 9 | Create CentComm custom table for ATPI push path | Sean Tomas + CentComm team | High | New data path alongside flexi fields |
| 10 | Update/extend CentComm view used by custom object/web API to include ATPI data | CentComm team + Sean Tomas | High | Ownership to be agreed with David/team |
| 11 | Add Snowflake/Data Engineering intake for ATPI customer IDs from MDS customer table | Data Engineering (Hamta Fakhravar volunteered) | High | Needed because ATPI IDs are not from standard CentComm sync |
| 12 | Provide two Snowflake outputs/views for downstream integration (flexi-field feed + ATPI custom-table feed) | Amanda Albers + Sean Tomas | Medium | Agreed as simpler than carrying a flag in downstream logic |
| 13 | Confirm routing for new customer rollup requests in this flow | Nadine Carson + Norma Barrett | Medium | Route through CentCom Help for non-standard/workflow gaps |

## Next Steps (Sequenced)
1. **Design the ATPI custom table schema first** (to establish downstream target and unblock dependent teams).
2. Finalize MDS customer-entity change (including field naming and default values).
3. Implement customer sync protection for manual ATPI records.
4. Execute one-time ATPI customer population and mapping reload.
5. Validate rollup inheritance and apply exception overrides (McDonald's and any others).
6. Build and test dual outbound paths:
   - Flexi field updates (existing path)
   - ATPI custom table updates (new path)
7. Coordinate with Data Engineering and CentComm teams for:
   - Snowflake ingestion updates
   - View/custom-object integration changes
8. Run end-to-end testing using refreshed mappings immediately before go-live.

## Risks / Open Questions
- **Field definition not finalized:** the “ATPI/manual source” discriminator is agreed conceptually, but naming/values still need confirmation.
- **Ownership split across teams:** some tasks require handoff between MDS, Data Engineering, and CentComm teams; clear handoff owners should be confirmed.
- **Manual process dependency:** short-term process still relies on manual steps and decision points.
- **Flexi-field update complexity:** sequence handling and update mechanics require careful implementation/testing.

## Suggested Confluence Labels
`udid` `atpi` `mds` `centcomm` `snowflake` `integration` `action-items`

