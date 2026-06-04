# Cisco Secure Workload — User Education

**A practical, vendor-neutral learning path for understanding and explaining Cisco Secure Workload (CSW).**

> **Disclaimer:** This repository is **not** official Cisco product documentation. It is companion learning material maintained for customer and partner education. Always validate design, scope, and supported features against your tenant's in-product documentation and [Cisco Secure Workload product documentation](https://www.cisco.com/c/en/us/products/security/workload-security/index.html) before production decisions.

Cisco Secure Workload is a workload visibility and micro-segmentation platform. It discovers how applications communicate, turns that into label-based policy, and lets teams roll out least-privilege segmentation across data centers, public cloud, containers, and supported workload environments — without breaking the apps. This repo gives you everything you need to learn it: a written guide (Markdown / Word / PDF), a curated **62-entry** video catalog with direct links, an onboarding runbook, and discovery and evidence checklists for POVs.

> **In one sentence:** CSW exists so that when — not if — one workload is compromised, the attacker cannot reach the next one.

## Contents

- [Who This Repo Is For](#who-this-repo-is-for)
- [The Problem CSW Solves](#the-problem-csw-solves)
- [Micro-segmentation Is a Journey](#micro-segmentation-is-a-journey)
- [Phased Adoption Roadmap](#phased-adoption-roadmap)
- [Quick Start: Where to Begin](#quick-start-where-to-begin)
- [Video Library (Learning Path Order)](#video-library-learning-path-order)
- [Secure Firewall Integration Guide (NetFlow + enforcement)](#secure-firewall-integration-guide-netflow--enforcement)
- [Repository Layout](#repository-layout)
- [Regenerating the Documents](#regenerating-the-documents)
- [Related Cisco Secure Workload Resources](#related-cisco-secure-workload-resources)

## Who This Repo Is For

- **Customers and partners** evaluating or onboarding CSW.
- **Cisco SEs, account teams, and delivery teams** who need a consistent way to explain CSW and run a POV.
- **Security, network, and platform engineers** who want a practical learning path without wading through release notes and product docs.

It is intentionally vendor-neutral in tone — no specific customer names, no marketing fluff — so it can be reused across deals and engagements.

## The Problem CSW Solves

Cisco Secure Workload exists to break the assumption that an attacker who gets inside the network can move freely. Most enterprise networks are still relatively flat at the workload layer — once one server is compromised through a phishing link, an exposed admin port, a vulnerable web app, or a stolen credential, the attacker can usually reach hundreds of other servers, file shares, and databases over the same internal network paths that legitimate applications use.

CSW reduces the **blast radius** of an intrusion by limiting each workload to **only the communication it actually needs**, based on real observed application behavior.

### The Lateral Movement Problem

After initial access, modern attackers (and most ransomware operators) follow a predictable pattern:

1. Land on one workload — phishing, exposed RDP/SSH, exploited service, supply chain.
2. Discover the internal network — port scans, SMB enumeration, AD reconnaissance.
3. Steal credentials — Mimikatz, LSASS dumps, Kerberoasting.
4. Move laterally — RDP, SMB, WinRM, WMI, PsExec, SSH, RPC, lateral admin tools.
5. Escalate to high-value targets — domain controllers, backup servers, file servers, databases, hypervisors.
6. Stage and detonate payload — ransomware, data exfiltration, destruction.

Visually, the kill chain looks like this:

```
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ 1. Initial   │──▶│ 2. Recon &   │──▶│ 3. Credential│
   │    Access    │   │    Enum      │   │    Theft     │
   └──────────────┘   └──────────────┘   └──────┬───────┘
                                                │
       ┌────────────────────────────────────────┘
       ▼
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ 4. Lateral   │──▶│ 5. Privilege │──▶│ 6. Payload   │
   │    Movement  │   │    Escalation│   │    & Impact  │
   └──────────────┘   └──────────────┘   └──────────────┘

           ┌──────────────────────────────────────────┐
           │ * CSW intervenes between steps 4 and 5:  │
           │   least-privilege policy removes the     │
           │   workload-to-workload network paths     │
           │   these steps depend on. The attacker    │
           │   can still land on host 1, but cannot   │
           │   reach hosts 2..N from there.           │
           └──────────────────────────────────────────┘
```

**Steps 2 through 5 all depend on the network allowing workload-to-workload traffic that no business application actually requires.** That is exactly the layer CSW controls.

### How CSW Stops or Slows Ransomware

Ransomware groups make money by encrypting many systems in a short time window. They depend on:

- Unrestricted **SMB / file share access** between workstations and servers.
- Open **RDP / WinRM / WMI / PsExec** paths between servers.
- Reachable **backup servers, file servers, and hypervisors** from compromised endpoints.
- Free **outbound east-west traffic** that lets the malware fan out.

CSW directly attacks every one of those preconditions:

| Ransomware behavior | What CSW does about it |
|---|---|
| SMB / RDP / WinRM fan-out from a compromised workload | Allow only application-required ports between specific workload groups; deny lateral admin protocols by default. |
| Mass file-share encryption | Restrict file-server access to the specific workloads / users / processes that genuinely need it. |
| Reaching backup or recovery systems | Place backup servers in their own scope; permit traffic only from backup agents, not general workloads. |
| Reaching domain controllers / identity tier | Scope identity / AD tier so only required clients and admin jump hosts can reach it. |
| Hopping between application tiers | Enforce per-app and per-tier policy (web → app → db) so a compromised web tier cannot reach unrelated databases. |
| Spreading to dev / test / lab | Hard-segment prod from non-prod so a non-prod compromise cannot pivot into prod. |
| Long undetected dwell time | Surface every blocked or anomalous flow as evidence for SOC and incident response. |

The result is that **ransomware that lands on one workload finds the network around it almost empty**: the protocols it needs to spread are blocked by policy, and every attempt is logged.

### Why We Need It

- **Flat networks no longer match the threat model.** Perimeter firewalls do not stop an attacker who is already inside.
- **Identity-based and EDR controls are necessary but not sufficient.** They catch behavior on the host; CSW removes the network paths the attacker would use between hosts.
- **Crown-jewel applications need explicit protection.** Payments, claims, customer data, intellectual property, and backup infrastructure should not be reachable from a random user workstation or low-tier dev server.
- **Compliance and audit demand it.** PCI, HIPAA, SOX, and most internal security frameworks expect documented segmentation between regulated and non-regulated systems. For framework-by-framework mappings — customer-facing reports and matching SA / SE technical runbooks across HIPAA, SOC 2, PCI DSS v4, NIST 800-53, ISO 27001:2022, CISA ZTMM, FIPS 140, NIST 800-207 / 207A, DORA, NIS2, NERC CIP, TSA Pipeline, CIS Controls v8.1, NIST CSF 2.0, CMMC 2.0, and more — see the companion repository: **[chandrapati/CSW-Compliance-Mapping](https://github.com/chandrapati/CSW-Compliance-Mapping)**. Use it whenever a customer asks "how does CSW map to *&lt;framework&gt;*?".
- **It must not break applications.** CSW's discovery-first model (map dependencies → label workloads → model policy → enforce in stages) is what makes segmentation finally feasible in real enterprises.

## Micro-segmentation Is a Journey

Micro-segmentation is **not** a one-time project you finish and archive. Applications change constantly — new services, refactors, cloud migrations, seasonal traffic, emergency patches, and M&A integrations all shift who talks to whom. A policy that was correct at go-live can be wrong six months later without anyone noticing.

CSW is built for that reality:

- **Continuous visibility** — agents and connectors keep observing flows and process context so dependency truth stays current, not frozen in last year's Visio diagram.
- **Discover change before you break production** — monitor and simulation modes surface new or unexpected conversations so teams can tune policy *before* enforcement blocks a legitimate transaction.
- **Policy that can adapt** — labels, scopes, ADM, and policy modeling let teams adjust allow rules when the application legitimately changes; vulnerability-driven tightening and forensics add another layer when risk spikes.
- **Operational discipline** — change windows, app-owner review, policy-as-code, label sync from CMDB/cloud tags, and drift detection (see CI/CD integration patterns below) are how mature programs keep segmentation aligned with the business over years, not weeks.

Treat the [phased adoption roadmap](#phased-adoption-roadmap) as a **starting path**, not an exit. Phase 5 (forensics, anomaly detection, SIEM integration) and day-2 practices in the onboarding runbook exist precisely because segmentation value compounds when it stays tied to how applications actually behave.

> **Plain language:** You are not buying a static rule set. You are standing up a **program** to see workload communication, govern change, and keep least-privilege policy matched to the apps you protect.

## Phased Adoption Roadmap

CSW value compounds in phases. You do **not** need to wait for full Application Dependency Mapping (ADM) to get value — each phase below delivers a concrete outcome on its own, and a customer who stops after Phase 2 has already shrunk ransomware blast radius and isolated prod from non-prod.

```
Week:      0 ─── 2 ─── 4 ─── 8 ─── 12+

Phase 1:   ███████                              Visibility
Phase 2:         ███████                        Macro Segmentation
Phase 3:               █████████████            ADM + App-Scope Micro-Segmentation
Phase 4:                     ██████████ ▶       Vulnerability-Driven Risk Reduction
Phase 5:                     ██████████ ▶       Forensics and Anomaly Detection
```

| Phase | Window | What you do | What you ship | Primary value |
|---|---|---|---|---|
| **1 — Visibility** | Week 0–2 | Deploy agents on a representative slice. Turn on cloud, CMDB, identity, and DNS connectors. Import existing labels. | Workload inventory, label dictionary, L3 / L4 + process flow data, baseline dependency view. | See what you actually have, with real flow truth — often the first time application owners can answer "who does this server talk to?". |
| **2 — Macro Segmentation** | Week 2–4 | Apply broad zone-to-zone policy in monitor mode, then enforcement: prod ↔ non-prod, prod ↔ dev / test / staging, user VLANs ↔ server zones. Deny lateral admin protocols (SMB, RDP, WinRM, WMI, PsExec, SSH) where no business app needs them. Isolate the backup tier and identity tier. | Enforced macro policy with monitor-mode evidence and rollback plan. | **Biggest blast-radius reduction for the lowest effort.** Ransomware fan-out paths are cut. The prod / non-prod story holds up in audit. High-value tiers (backup, AD, hypervisor) are reachable only from where they should be. |
| **3 — ADM + App-Scope Micro-Segmentation** | Week 4–12 (per application wave) | Run ADM on a chosen application. Review the dependency map with the app owner. Convert observed flows + labels into recommended allow rules. Move to monitor mode, tune, then staged enforcement. Repeat for the next app wave. | Per-app dependency map, modeled policy, blocked-flow evidence, allowed-business-transaction evidence, app-owner signoff. | True micro-segmentation around the application itself. Per-tier policy (web → app → db). App teams understand their own application, sometimes for the first time. |
| **4 — Vulnerability-Driven Risk Reduction** | Continuous from ~Week 8 | Ingest vulnerability data (scanner exports, CVE feeds). Tag workloads with risk labels (for example `risk:high`, `cve:exploitable`). Tighten policy automatically for high-risk workloads — restrict their reachable surface to admin / patch paths only until remediated. | Risk-tagged inventory, tightened policy on vulnerable workloads, security and audit evidence. | Defenders work the problems attackers actually try. When the next Log4J / Log4Shell-class CVE lands, exposure can be shrunk within the same day instead of waiting on patch cycles. |
| **5 — Forensics and Anomaly Detection** | Continuous from ~Week 8 | Use Secure Workload forensics events, flow-pattern anomaly detection, and SIEM / SOAR integration. Build playbooks that pair policy violations with host evidence. | Forensics events, anomaly findings, SOC playbooks, IR evidence trails. | Detection compounds with segmentation. Every blocked flow becomes evidence. Mean-time-to-detect drops because workload behavior is bounded by policy. |

**Key idea:** every phase is independently valuable. A customer who stops after Phase 2 still wins — ransomware fan-out is gone and prod is isolated from non-prod. A customer who reaches Phase 5 has continuous defense in depth — and should keep operating there, because [applications and policy both keep changing](#micro-segmentation-is-a-journey).

### Mapping phases to videos in the catalog

- **Phase 1 — Visibility:** Agent Configuration Profile (#1), Scopes (#3), Labels (#4), Inventory Filters (#5), Flow Analysis (#10).
- **Phase 2 — Macro Segmentation:** SSH Risk Reduction (#15), Terminal Services Segmentation (#16), Production and Test Risk Reduction (#6), VDI Segmentation (#17).
- **Phase 3 — ADM + App-Scope Micro:** Application Dependency Mapping & Policy Analysis (#7), Policy Visual and Quick Analysis (#8), Dynamic Workloads & Policy (#9), AI-Driven Policy Suggestions (#33), Policy Statistics with AI Engine (#34).
- **Phase 4 — Vulnerability-Driven Risk Reduction:** Vulnerabilities and Risk Reduction (#11), Log4J Risk Reduction (#14), Security Dashboard (#12).
- **Phase 5 — Forensics and Anomaly Detection:** Forensics (#13), Flow Analysis (#10), Security Dashboard (#12).

The tactical, step-by-step deployment playbook (tenant prep, agent rollout, label strategy, policy modeling, enforcement testing, operationalization) lives in **§ 8 CSW Onboarding Runbook** of [`docs/user-education/CSW-User-Education-Guide.md`](docs/user-education/CSW-User-Education-Guide.md).

## Quick Start: Where to Begin

Pick the lane that matches your time and role.

| If you have... | Start with |
|---|---|
| **10 minutes** | [Scopes](https://www.youtube.com/watch?v=3KBmanCNm4U) and [Labels](https://www.youtube.com/watch?v=NLoZq0wiTU8) — the two foundational concepts every CSW conversation builds on. |
| **30 minutes** | Add [Application Dependency Mapping & Policy Analysis](https://www.youtube.com/watch?v=Jzzblea25UA) — the primary value of CSW: discover what talks to what, then derive policy. |
| **2 hours** | Modules 1–4 in the [Video Library](#video-library-learning-path-order) (foundations through core policy workflow). |
| **A POV is on the table** | Skim Core CSW Training, watch [Production and Test Risk Reduction](https://www.youtube.com/watch?v=HKT18Ylt4IY) plus the integration videos that match the customer stack (firewall, F5, ISE, FMC). Then open [`docs/user-education/CSW-User-Education-Guide.md`](docs/user-education/CSW-User-Education-Guide.md) for the onboarding runbook and POV evidence checklist. |
| **Secure Firewall + NetFlow in scope** | Start with [**CSW-Secure-Firewall-Integration-Guide**](https://github.com/chandrapati/CSW-Secure-Firewall-Integration-Guide) — step-by-step NSEL ingest and FMC enforcement with linked YouTube videos. |

## Video Library (Learning Path Order)

62 videos and references arranged in the order that builds CSW skills fastest: concepts first, then agents, then visibility → policy, then security outcomes, then environment-specific depth. Modules 1–8 are the original learning-path series; **Modules 9–15 add the newer official Cisco Secure Workload channel demos (2025–2026)**. **Watch top to bottom** within each module; skip modules that do not match your POV (for example, skip Module 2 VDI if you are not deploying to golden-image desktops).

The **Catalog #** column is the original slide numbering — use it when cross-referencing the [Phased Adoption Roadmap](#phased-adoption-roadmap) video mappings.

### Module 1 — Foundations (start here)

Learn how CSW organizes workloads before any policy work.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 1 | 3 | Cisco Secure Workload: Scopes | Group workloads logically for policy application and management. | [Watch](https://www.youtube.com/watch?v=3KBmanCNm4U) |
| 2 | 4 | Cisco Secure Workload: Labels | Tag workloads for granular policy enforcement and visibility. | [Watch](https://www.youtube.com/watch?v=NLoZq0wiTU8) |
| 3 | 5 | Cisco Secure Workload: Inventory Filters | Filter inventory to focus on specific workloads or groups. | [Watch](https://www.youtube.com/watch?v=fJd6V15UiZM) |

### Module 2 — Agent deployment

Roll out telemetry collection on workloads.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 4 | 1 | Cisco Secure Workload: Agent Configuration Profile | Configure agent profiles to manage workload agents for security enforcement. | [Watch](https://www.youtube.com/watch?v=4mFriUr4WHk) |
| 5 | 2 | Agent Configuration and Deployment – Golden Image VDI | Deploy agents in VDI environments using golden images. *Skip if VDI is not in scope.* | [Watch](https://www.youtube.com/watch?v=LYHnU_QjKfI) |

### Module 3 — Visibility and dependency discovery

See what talks to what — the core CSW value story.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 6 | 6 | Production and Test Risk Reduction | Macro-segment prod vs non-prod — fast blast-radius win. | [Watch](https://www.youtube.com/watch?v=HKT18Ylt4IY) |
| 7 | 10 | Flow Analysis | Understand traffic patterns and anomalies from observed flows. | [Watch](https://www.youtube.com/watch?v=Tuw06kPjeyQ) |
| 8 | 7 | Application Dependency Mapping & Policy Analysis | Map application dependencies and derive microsegmentation policy. | [Watch](https://www.youtube.com/watch?v=Jzzblea25UA) |
| 9 | 9 | Dynamic Workloads & Policy | Adapt policy as workloads move or scale. | [Watch](https://www.youtube.com/watch?v=Aajlx7JT2G4) |
| 10 | 8 | Policy Visual and Quick Analysis | Visualize and analyze policy impact before enforcement. | [Watch](https://www.youtube.com/watch?v=uBxrJaVLHy4) |

### Module 4 — AI-assisted policy (after Module 3)

Accelerate policy creation once the manual workflow is clear.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 11 | 33 | AI-Driven Policy Suggestions | AI-generated policy recommendations from observed behavior. | [Watch](https://www.youtube.com/watch?v=UwUJnEMZoTk) |
| 12 | 34 | Policy Statistics with Cisco Workloads AI Engine | Policy statistics, anomalies, and tuning insights at scale. | [Watch](https://www.youtube.com/watch?v=kvnAoT5ZYXl) |

### Module 5 — Security, risk, and forensics

Operationalize risk reduction and incident evidence.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 13 | 12 | Security Dashboard | Posture, risk indicators, and drill-downs. | [Watch](https://www.youtube.com/watch?v=_faK3p9tN4A) |
| 14 | 11 | Vulnerabilities and Risk Reduction | Prioritize and reduce exposure on vulnerable workloads. | [Watch](https://www.youtube.com/watch?v=l7LwZHXBYUA) |
| 15 | 15 | SSH Risk Reduction | Control SSH paths between workloads. | [Watch](https://www.youtube.com/watch?v=RV7To1MF6Es) |
| 16 | 14 | Log4J Risk Reduction | Identify and contain Log4Shell-class exposure. | [Watch](https://www.youtube.com/watch?v=FTXsWtFUJZM) |
| 17 | 13 | Forensics | Process and flow evidence for investigations. | [Watch](https://www.youtube.com/watch?v=ZPBcj4e6M34) |

### Module 6 — Segmentation use cases

Deep dives when the customer environment matches.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 18 | 16 | Terminal Services Segmentation | Segment RDS / Terminal Services environments. | [Watch](https://www.youtube.com/watch?v=pfv42g3FJEk) |
| 19 | 17 | VDI Segmentation | Segment shared golden-image VDI estates. | [Watch](https://www.youtube.com/watch?v=SFVjiPQFsYA) |

### Module 7 — Integrations (pick what matches the stack)

Watch only the rows relevant to the customer POV.

| Watch | Catalog # | Resource | Description | Link |
|:---:|---:|---|---|:---:|
| 20 | 18 | Secure Workload & Firewall Integration (Part 1) | Introduction, design, and architecture. | [Watch](https://youtu.be/vdHjAl48SuI) |
| 21 | 19 | Secure Workload & Firewall Integration (Part 2) | Deployment patterns and policy flow. | [Watch](https://www.youtube.com/watch?v=xpbg3s0vrcI) |
| 22 | 20 | Secure Workload & Firewall Integration (Part 3) | Enforcement, telemetry, and operations. | [Watch](https://www.youtube.com/watch?v=X65mwN7kJGg&t=53s) |
| 23 | 21 | Secure Workload and Secure Firewall White Paper | Joint architecture reference (Cisco.com). | [Read](https://www.cisco.com/c/en/us/products/collateral/security/secure-workload/sec-workload-firewall-wp.html) |
| 24 | 22 | Secure Workload & Firewall Integration Deep Dive | Design principles and use cases. | [Read](https://secure.cisco.com/secure-workload/docs/secure-workload-whitepaper) |
| 25 | 23 | F5 BIG-IP and Cisco Tetration: APM Visibility | F5 APM data for application visibility. | [Watch](https://www.youtube.com/watch?v=dqbWhvFNsso&t=90s) |
| 26 | 24 | Cisco Tetration and F5 BIG-IP AFM | F5 AFM flow context integration. | [Watch](https://www.youtube.com/watch?v=HcF3yQHmeXc) |
| 27 | 25 | F5 BIG-IP IPFIX Configuration | Send IPFIX from BIG-IP into Secure Workload. | [Watch](https://www.youtube.com/watch?v=aJZEcZtUXDg) |
| 28 | 26 | DNS Server Integration | DNS context for flow attribution and policy. | [Watch](https://www.youtube.com/watch?v=hD0WpBRLCiM) |
| 29 | 27 | Infoblox Integration | Infoblox DNS / IPAM context in CSW. | [Watch](https://www.youtube.com/watch?v=gdhMWviAZig) |
| 30 | 28 | Algosec Integration | Firewall-policy lifecycle alongside CSW. | [Watch](https://www.youtube.com/watch?v=FUyESTLLZE8) |
| 31 | 29 | ISE (In Action) | User and device identity from Cisco ISE. | [Watch](https://www.youtube.com/watch?v=KUJfuuhP1dc) |
| 32 | 30 | FMC Integration with Edge / Ingest / Appliance | FMC through Edge, Ingest, and appliance paths. | [Watch](https://youtu.be/13AZ33dpCxU) |
| 33 | 31 | ACI and CSW Integration | ACI fabric policy with workload segmentation. | [Watch](https://www.youtube.com/watch?v=u7jh3Zw1hlg) |
| 34 | 35 | Splunk Integration (SIEM) | Three patterns: Cisco Security Cloud App for baseline dashboards/datasets, CSW → Splunk Syslog alerts, and Splunk-driven Python against the CSW API for arbitrary metadata. | [Watch](https://youtu.be/CRnkH9imTZk) |
| 35 | 36 | CI/CD Pipeline Integration | Treat CSW like any other declarative system: labels, scopes, and policy live in git and reach the tenant through pipeline-driven API calls. | [Watch](https://www.youtube.com/watch?v=0wsSA69ol0M) |

**Splunk integration — three patterns at a glance:**

1. **Cisco Security Cloud App for Splunk** — install the Cisco-published Splunk app; it reaches back to CSW (and other Cisco Security products) to pull a baseline set of datasets and dashboards. Lowest-effort starting point.
2. **CSW → Splunk Syslog alerts** — configure CSW to push alarms/alerts to Splunk over Syslog so SOC sees policy violations, agent health events, and forensic signals alongside everything else they already index.
3. **Splunk → CSW API (Python)** — Splunk can launch Python against the CSW API, so anything the API exposes (inventory, scopes, labels, policies, enforcement state, vulnerabilities, flow summaries — everything except the raw flow data itself) can be pulled into Splunk and indexed, dashboarded, or alerted on. This is where the "sky is the limit" — any custom CSW API script becomes a Splunk-driven data feed.

**CI/CD pipeline integration — what it typically wires up:**

- **Policy-as-code** — intended scopes, labels, and policies live in git; a pipeline job calls the CSW API to apply them, so the tenant matches the repo and changes go through code review instead of console clicks.
- **Promotion across environments** — the same policy bundle is rolled forward from dev → staging → prod, starting in Monitor mode and only flipping to Enforce after the gating checks pass.
- **Label sync from upstream sources of truth** — CMDB / cloud-tag exports get normalized in CI and pushed into CSW so workload labels stay accurate without manual upkeep.
- **Drift detection** — a scheduled pipeline diffs live tenant state against the repo and opens a ticket when something was changed out-of-band.
- **Built on the same API surface as Pattern 3 of the Splunk integration above** — any Python you already have for CSW becomes a pipeline step.

### Module 8 — Containers and Kubernetes

When Kubernetes is in scope.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 36 | 32 | Agent K8s | Secure Workload agent in Kubernetes environments. | [Watch](https://www.youtube.com/watch?v=h9PW25UhXKs) |

### Module 9 — Official Channel: Getting Started

Newer overview content published directly on the [Cisco Secure Workload YouTube channel](https://www.youtube.com/@ciscosecureworkload) (2025–2026). Use these as the most current "start here" demos.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 37 | — | Introduction to Secure Workload & Overview Demo | Current product overview and end-to-end demo — best first watch. | [Watch](https://youtu.be/8HpUkYXbHnw) |
| 38 | — | Inventory Filters (channel version) | Official-channel refresh of inventory filtering. | [Watch](https://youtu.be/ymCB_PkFYcI) |

### Module 10 — Connectors, Telemetry & Application Discovery

How CSW ingests context and discovers applications before policy work.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 39 | — | Connector Overview | What connectors do and how they enrich telemetry. | [Watch](https://youtu.be/H6QxuouzeC8) |
| 40 | — | Connector Deployment | Deploying connectors on the virtual appliances. | [Watch](https://youtu.be/H0as2ppS84Q) |
| 41 | — | Provided Services | Built-in services on the appliances. | [Watch](https://youtu.be/2dGQ9winZwE) |
| 42 | — | Basic Application Discovery | First-pass ADM to surface application dependencies. | [Watch](https://youtu.be/HGvtBonFiE4) |
| 43 | — | Enhancing Application Discovery | Improve ADM fidelity with labels and context. | [Watch](https://youtu.be/4wa7PiHGUnM) |

### Module 11 — Policy Lifecycle & Enforcement (deep dive)

The full policy workflow from modeling through enforcement placement.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 44 | — | Policy Lifecycle | End-to-end policy lifecycle overview. | [Watch](https://youtu.be/Cm-cUwRorDc) |
| 45 | — | Policy Validation and Analysis | Validate and analyze policy before enforcing. | [Watch](https://youtu.be/DgaZpQ0lnAI) |
| 46 | — | Policy Ordering | How rule order affects enforcement outcomes. | [Watch](https://youtu.be/fG1Kn1C7QRM) |
| 47 | — | Policy Enforcement Overview | How enforcement is applied across workloads. | [Watch](https://youtu.be/A8rOXQ-y4Cw) |
| 48 | — | Where to Enforce | Choosing the right enforcement point (host / network / cloud). | [Watch](https://youtu.be/urFJyDERMFs) |
| 49 | — | Container Enforcement | Enforce policy on containerized workloads. | [Watch](https://youtu.be/6Z_y_keYyE0) |
| 50 | — | Windows Process-Level Enforcement | Process-aware enforcement on Windows hosts. | [Watch](https://youtu.be/frhcPHXQkNw) |

### Module 12 — Security, Forensics & Alerting

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 51 | — | Security Dashboard and Forensics | Combined posture, risk, and forensic evidence walkthrough. | [Watch](https://youtu.be/PVRkzWRAa08) |
| 52 | — | Alerting | Configure and route CSW alerts. | [Watch](https://youtu.be/RqM6vbDEDPc) |

### Module 13 — Day-2 Operations & Platform Management

Operate, audit, and protect the CSW platform itself.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 53 | — | Agent Operations | Manage and maintain deployed agents. | [Watch](https://youtu.be/EIqPiPgpDqc) |
| 54 | — | Auditing | Audit trails for changes and access. | [Watch](https://youtu.be/_5K62x49c_I) |
| 55 | — | Data Backup and Restore | Back up and restore tenant/cluster data. | [Watch](https://youtu.be/dVK0xe4RWh4) |
| 56 | — | Federation | Multi-cluster federation for scale. | [Watch](https://youtu.be/465loG3VlZE) |
| 57 | — | Managing Secure Workload in Security Cloud Control | SaaS management via Security Cloud Control (SCC). | [Watch](https://youtu.be/UVTkxaUJSHA) |
| 58 | — | Global Visualization Updates | Visualization enhancements. | [Watch](https://youtu.be/kGLEKRltV2M) |

### Module 14 — Integrations (newer)

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 59 | — | Secure Workload & Secure Firewall Integration Updates | Latest firewall integration updates (supersedes the 3-part series for current behavior). | [Watch](https://youtu.be/IEqbz44YvOQ) |

### Module 15 — Strategy & Architecture

Executive- and architecture-level framing for segmentation programs.

| Watch | Catalog # | Video | Description | Link |
|:---:|---:|---|---|:---:|
| 60 | — | Campus and Zero Trust | Extend Zero Trust segmentation into the campus. | [Watch](https://youtu.be/hX9Q6IYcgXA) |
| 61 | — | Enabling Consistent Multi-Cloud Security, Forensics & IR | Consistent policy and IR across multi-cloud. | [Watch](https://youtu.be/x-dMr3Kg4dg) |
| 62 | — | How to Create a Comprehensive Zero Trust Strategy | Building an end-to-end Zero Trust strategy. | [Watch](https://youtu.be/1jvgXt906m8) |

> **Channel note:** Modules 9–15 are sourced from the official [Cisco Secure Workload YouTube channel](https://www.youtube.com/@ciscosecureworkload), where Cisco TMEs (including Jorge Quintero and Jason Lunde) publish current product demos. Jason Maynard's "How Hard Can It Be?" CSW series (Modules 1–8) lives on his [personal channel](https://www.youtube.com/@jasonmaynard8773); his recent uploads have shifted to Cisco Secure Access / SOC topics outside this repo's CSW scope.

## Secure Firewall Integration Guide (NetFlow + enforcement)

Step-by-step companion for **Cisco Secure Firewall** with CSW — separate paths for **NSEL/NetFlow visibility** (Secure Firewall Connector on Ingest) and **policy enforcement** (FMC Connector).

| Resource | Link |
|---|---|
| **Integration guide (Markdown)** | [**CSW-Secure-Firewall-Integration-Guide**](https://github.com/chandrapati/CSW-Secure-Firewall-Integration-Guide) (standalone repo) |
| Local copy in this repo | [`docs/user-education/CSW-Secure-Firewall-Integration-Guide.md`](docs/user-education/CSW-Secure-Firewall-Integration-Guide.md) |
| Part 1 — design & architecture | [YouTube](https://youtu.be/vdHjAl48SuI) |
| Part 2 — deployment | [YouTube](https://www.youtube.com/watch?v=xpbg3s0vrcI) |
| Part 3 — enforcement & operations | [YouTube](https://www.youtube.com/watch?v=X65mwN7kJGg) |
| **2025–2026 integration updates** | [YouTube](https://youtu.be/IEqbz44YvOQ) |
| FMC + Edge / Ingest / Appliance | [YouTube](https://youtu.be/13AZ33dpCxU) |
| Connector overview & deployment | [YouTube](https://youtu.be/H6QxuouzeC8) · [YouTube](https://youtu.be/H0as2ppS84Q) |
| Where to enforce · Policy enforcement | [YouTube](https://youtu.be/urFJyDERMFs) · [YouTube](https://youtu.be/A8rOXQ-y4Cw) |
| Cisco white paper | [Cisco.com](https://www.cisco.com/c/en/us/products/collateral/security/secure-workload/sec-workload-firewall-wp.html) |

## Repository Layout

| Path | What it is |
|---|---|
| `README.md` | This file: intro, value story, video library in learning-path order. |
| `docs/user-education/CSW-User-Education-Guide.md` | Full Markdown guide: intro, concepts, video library, onboarding runbook, discovery questions, POV evidence checklist, pitfalls, talk track. |
| `docs/user-education/CSW-Secure-Firewall-Integration-Guide.md` | Step-by-step Secure Firewall NSEL ingest + FMC enforcement integration with video links. |
| `docs/user-education/CSW-User-Education-Guide.docx` | Generated Word version of the guide. |
| `docs/user-education/CSW-User-Education-Guide.pdf` | Generated PDF version of the guide. |

The Markdown files are the source of truth for the guide. The `.docx` and `.pdf` artefacts are regenerated from Markdown — see below.

## Regenerating the Documents

After editing either `README.md` or `CSW-User-Education-Guide.md`, rebuild the Word and PDF artefacts:

```bash
# Step 1 - Markdown to DOCX (fast, ~7s)
pandoc docs/user-education/CSW-User-Education-Guide.md \
  --from gfm \
  --to docx \
  --toc \
  --toc-depth=2 \
  -o docs/user-education/CSW-User-Education-Guide.docx

# Step 2 - DOCX to PDF (LibreOffice headless, ~35s)
# Use an isolated user profile so the build does not block
# on a stale lock if a LibreOffice GUI is open elsewhere.
cd docs/user-education
rm -rf /tmp/lo_csw_profile
soffice --headless \
  -env:UserInstallation=file:///tmp/lo_csw_profile \
  --convert-to pdf CSW-User-Education-Guide.docx
```

Keep the two steps separate (do not chain with `&&`): if `soffice` ever hangs on a profile lock, the DOCX is already on disk and you only need to retry the PDF step.

## Related Cisco Secure Workload Resources

Other public repositories covering the full Cisco Secure Workload journey — from onboarding to compliance reporting:

| Repository | What It Covers | Best For |
|---|---|---|
| [**CSW-Secure-Firewall-Integration-Guide**](https://github.com/chandrapati/CSW-Secure-Firewall-Integration-Guide) | Step-by-step NSEL ingest + FMC policy enforcement on Cisco Secure Firewall | Firewall / network teams and POVs with FTD/ASA |
| [**CSW-Identity-Integration-Guide**](https://github.com/chandrapati/CSW-Identity-Integration-Guide) | AD, Entra ID, and DC user-identity reporting for CSW labels | Identity and AD teams |
| [**CSW-ServiceNow-Connector-Guide**](https://github.com/chandrapati/CSW-ServiceNow-Connector-Guide) | ServiceNow inventory enrichment connector setup and operations | CMDB-driven label strategies |
| [**csw-splunk-integration**](https://github.com/chandrapati/csw-splunk-integration) | Step-by-step CSW → Splunk integration via Syslog connector and Cisco Security Cloud App | Security operations teams |
| [**CSW-Agent-Installation-Guide**](https://github.com/chandrapati/CSW-Agent-Installation-Guide) | Host agent install across Linux, Windows, cloud, containers, and agentless environments | Operations and deployment teams |
| [**CSW-Policy-Lifecycle**](https://github.com/chandrapati/CSW-Policy-Lifecycle) | Full policy lifecycle: ADM discovery → Monitor → Simulate → Enforce + day-2 ops | SE/SA and customer engineering |
| [**CSW-Compliance-Mapping**](https://github.com/chandrapati/CSW-Compliance-Mapping) | Compliance reports and SA/SE runbooks for 30+ frameworks (HIPAA, SOC 2, PCI DSS v4, NIST 800-53, ISO 27001, CISA ZTMM, FIPS 140, and more) | CISO, GRC, and audit teams |
| [**CSW-Operations-Toolkit**](https://github.com/chandrapati/CSW-Operations-Toolkit) | Reusable POV engagement toolkit — clone for each new engagement | SEs running a CSW proof-of-value |
| [**csw-logs-check**](https://github.com/chandrapati/csw-logs-check) | Cursor skill: analyze CSW agent diagnostic bundles for enforcement timing | Host enforcement validation |
| [**csw_blast_radius_demo**](https://github.com/chandrapati/csw_blast_radius_demo) | Hands-on demo showing blast radius reduction via microsegmentation | Demo and lab environments |
| [**CSW-SE-Helper-Repo**](https://github.com/chandrapati/CSW-SE-Helper-Repo) | SE helper utilities and scratch tooling | SEs |

> **Suggested path for a new customer:**
> CSW-User-Education → CSW-Agent-Installation-Guide → **CSW-Secure-Firewall-Integration-Guide** (if firewall in scope) → CSW-Identity-Integration-Guide (if identity in scope) → CSW-Policy-Lifecycle → csw-splunk-integration → CSW-Compliance-Mapping → CSW-Operations-Toolkit
