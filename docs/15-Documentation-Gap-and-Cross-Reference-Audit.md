# 15. Documentation Gap & Cross-Reference Audit

## 1. Purpose
This audit reviews each documentation file in the repository and highlights:

1. Missing or thin documentation areas ("gaps")
2. Missing explicit cross-references to related specs
3. Suggested additions to improve navigation and maintainability

Scope reviewed:
- `docs/00` through `docs/14`
- `backend/README.md`
- `frontend/README.md`

---

## 2. Summary Findings

- Most documents are detailed in their own domain but do **not** include a dedicated `Cross-References` section.
- Navigation works well from `00-Architecture-Index.md`, but reverse linkage from individual files is limited.
- `backend/README.md` and `frontend/README.md` are placeholder-level and should link directly to architecture, API, and TDD docs.
- Operational documents (`11` to `14`) would benefit from tighter traceability to test strategy and risk register.

---

## 3. File-by-File Gap Review

| File | Documentation Gaps | Cross-Reference Gaps | Suggested Cross-Links |
| :--- | :--- | :--- | :--- |
| `docs/00-Architecture-Index.md` | No link to this audit document in the map. | Does not call out how to use RTM for verification flow. | `08`, `15` |
| `docs/01-BRD.md` | Rich requirements, but lacks explicit assumptions/constraints section. | No explicit links to FRS, RTM, or NFR. | `02`, `08`, `11` |
| `docs/02-FRS.md` | Missing a concise "out of scope" section. | Limited direct linkage back to BRD IDs and forward to tests. | `01`, `07`, `08` |
| `docs/03-WebSocket-Protocol-Spec.md` | Event lifecycle examples could include error payload coverage. | No explicit links to state machine and backend TDD. | `05`, `09`, `11` |
| `docs/04-REST-API-Spec.md` | Could include auth/error model summary table. | No explicit links to DB schema and change management. | `10`, `14` |
| `docs/05-Backend-TDD.md` | Could add module ownership boundaries and coding standards reference. | No direct links to WebSocket protocol and state machines. | `03`, `09`, `10` |
| `docs/06-Frontend-TDD.md` | Could add rendering performance budget guidance. | No direct links to BRD visual requirements and WS protocol. | `01`, `03`, `11` |
| `docs/07-Test-Plan-QA-Strategy.md` | Could include defect severity taxonomy and release gates. | Should explicitly link to RTM and risk register for test prioritization. | `08`, `13` |
| `docs/08-Requirements-Traceability-Matrix.md` | Could include owner/status columns for each requirement. | No explicit backlinks to BRD/FRS section anchors. | `01`, `02`, `07` |
| `docs/09-State-Machines.md` | Could include timeout/retry constants and event source notes. | No direct links to WS spec and backend implementation plan. | `03`, `05` |
| `docs/10-Database-Schema-Spec.md` | Could add migration rollback examples and seed data policy. | No direct links to REST spec and deployment backups. | `04`, `12`, `14` |
| `docs/11-Non-Functional-Requirements.md` | Could include measurable observability SLOs beyond performance. | No explicit links to deployment monitoring and risk register. | `12`, `13` |
| `docs/12-Deployment-Plan.md` | Could include staging/prod promotion workflow and rollback checklist. | No direct links to NFR objectives and change versioning policy. | `11`, `14` |
| `docs/13-Risk-Register.md` | Lacks owner, target date, and residual risk fields. | No links to test plan or deployment controls. | `07`, `12` |
| `docs/14-Change-Management.md` | Could include approval workflow (who signs off). | No direct links to API specs and DB migration spec. | `03`, `04`, `10` |
| `backend/README.md` | Placeholder only; lacks setup/run/test instructions. | No links to backend design/API references. | `docs/05`, `docs/03`, `docs/04`, `docs/10` |
| `frontend/README.md` | Placeholder only; lacks setup/run/test instructions. | No links to frontend design and UX constraints. | `docs/06`, `docs/01`, `docs/03` |

---

## 4. Recommended Cross-Reference Section Template

Add this to each primary document:

```md
## Cross-References
- Related upstream requirements: [...]
- Related downstream implementation docs: [...]
- Validation/Test linkage: [...]
- Operational/Change linkage: [...]
```

---

## 5. Priority Actions

1. **High Priority**: Expand both README files with implementation entry points and direct links.
2. **High Priority**: Add `Cross-References` sections to `01`–`14`.
3. **Medium Priority**: Strengthen `08-RTM` with ownership/status tracking.
4. **Medium Priority**: Align `11`/`12`/`13`/`14` for operational traceability.
5. **Low Priority**: Add assumptions/out-of-scope sections in BRD/FRS.

---

## 6. Change Log

| Version | Date | Notes |
| :--- | :--- | :--- |
| v1.0 | 2026-02-14 | Initial audit covering all repository documentation files. |
