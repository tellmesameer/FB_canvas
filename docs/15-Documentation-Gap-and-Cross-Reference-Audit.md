# 15. Documentation Gap & Cross-Reference Audit

## 1. Purpose
This audit re-checks every documentation file in scope and reports:

1. Documentation coverage gaps
2. Cross-reference section status
3. Recommended links to strengthen traceability

Scope reviewed:
- `docs/00` through `docs/14`
- `backend/README.md`
- `frontend/README.md`

---

## 2. Re-Check Summary (Current State)

- All core documents contain useful content, and most include at least some inline links to related docs.
- **No reviewed file currently has a dedicated `Cross-References` section**.
- `backend/README.md` and `frontend/README.md` now include setup/run/test guidance and documentation map links (improved from placeholder state).
- Operational traceability between NFRs, deployment, risks, and change controls remains weak and should be tightened.

---

## 3. File-by-File Audit

| File | Doc Gap Check | Cross-Reference Check | Suggested Additions |
| :--- | :--- | :--- | :--- |
| `docs/00-Architecture-Index.md` | Good map; add quick “how to navigate by role” note. | Missing dedicated `Cross-References` section. | Add links to `08` (verification flow) and `15` (audit results). |
| `docs/01-BRD.md` | Strong feature detail; add assumptions/constraints and out-of-scope summary. | Missing dedicated `Cross-References` section. | Link to `02`, `08`, `11`. |
| `docs/02-FRS.md` | Strong behavior definitions; add explicit out-of-scope and non-goals. | Missing dedicated `Cross-References` section. | Link to `01`, `07`, `08`, `09`. |
| `docs/03-WebSocket-Protocol-Spec.md` | Good protocol coverage; add more negative/error event examples. | Missing dedicated `Cross-References` section. | Link to `05`, `06`, `09`, `11`. |
| `docs/04-REST-API-Spec.md` | Comprehensive endpoints; add consolidated auth/error model table. | Missing dedicated `Cross-References` section. | Link to `10`, `12`, `14`. |
| `docs/05-Backend-TDD.md` | Good implementation detail; add module ownership and coding standard references. | Missing dedicated `Cross-References` section. | Link to `03`, `04`, `09`, `10`. |
| `docs/06-Frontend-TDD.md` | Strong architecture detail; add rendering/perf budgets and accessibility acceptance notes. | Missing dedicated `Cross-References` section. | Link to `01`, `03`, `07`, `11`. |
| `docs/07-Test-Plan-QA-Strategy.md` | Good test coverage; add defect severity matrix and release exit criteria. | Missing dedicated `Cross-References` section. | Link to `08`, `11`, `13`, `14`. |
| `docs/08-Requirements-Traceability-Matrix.md` | Clear mapping; add owner/status/last-verified columns. | Missing dedicated `Cross-References` section. | Add direct backlinks to BRD/FRS section anchors and `07`. |
| `docs/09-State-Machines.md` | Clear diagrams; add timeout/retry constants and event source notes. | Missing dedicated `Cross-References` section. | Link to `03`, `05`, `07`. |
| `docs/10-Database-Schema-Spec.md` | Good schema detail; add rollback examples and seed/test data policy. | Missing dedicated `Cross-References` section. | Link to `04`, `05`, `12`, `14`. |
| `docs/11-Non-Functional-Requirements.md` | Good baseline NFRs; add observability SLOs and capacity thresholds. | Missing dedicated `Cross-References` section. | Link to `07`, `12`, `13`. |
| `docs/12-Deployment-Plan.md` | Good deployment baseline; add promotion workflow and rollback checklist. | Missing dedicated `Cross-References` section. | Link to `10`, `11`, `13`, `14`. |
| `docs/13-Risk-Register.md` | Good initial risks; add owner, target date, residual risk, and status fields. | Missing dedicated `Cross-References` section. | Link to `07`, `11`, `12`, `14`. |
| `docs/14-Change-Management.md` | Good versioning baseline; add approval workflow and sign-off ownership. | Missing dedicated `Cross-References` section. | Link to `03`, `04`, `10`, `12`. |
| `backend/README.md` | **Improved**: now includes prerequisites, setup, run, tests, structure. | Missing dedicated `Cross-References` section. | Add explicit “Cross-References” block linking `03/04/05/10/12`. |
| `frontend/README.md` | **Improved**: now includes prerequisites, setup, run, tests, build, structure. | Missing dedicated `Cross-References` section. | Add explicit “Cross-References” block linking `01/03/06/07/11`. |

---

## 4. Standard Cross-References Section (Recommended)

Use this section in each major document:

```md
## Cross-References
- Upstream requirements: [BRD](01-BRD.md), [FRS](02-FRS.md)
- Interfaces/contracts: [WebSocket](03-WebSocket-Protocol-Spec.md), [REST](04-REST-API-Spec.md)
- Implementation: [Backend TDD](05-Backend-TDD.md), [Frontend TDD](06-Frontend-TDD.md), [State Machines](09-State-Machines.md), [DB Spec](10-Database-Schema-Spec.md)
- Validation/operations: [Test Plan](07-Test-Plan-QA-Strategy.md), [RTM](08-Requirements-Traceability-Matrix.md), [NFR](11-Non-Functional-Requirements.md), [Deployment](12-Deployment-Plan.md), [Risk](13-Risk-Register.md), [Change Mgmt](14-Change-Management.md)
```

---

## 5. Priority Actions

1. **High**: Add a dedicated `Cross-References` section to `docs/01`–`docs/14` and both README files.
2. **High**: Strengthen operational traceability across `11`/`12`/`13`/`14`.
3. **Medium**: Expand RTM (`08`) with owner/status/verification date fields.
4. **Medium**: Add assumptions/out-of-scope statements in BRD and FRS.
5. **Low**: Add role-based navigation guidance in the architecture index.

---

## 6. Change Log

| Version | Date | Notes |
| :--- | :--- | :--- |
| v1.1 | 2026-02-14 | Re-check completed after documentation updates; backend/frontend README improvements acknowledged; cross-reference section gaps remain across all reviewed files. |
| v1.0 | 2026-02-14 | Initial audit covering all repository documentation files. |
