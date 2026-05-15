# Cisco Secure Workload — User Education

**A practical, vendor-neutral learning path for understanding and explaining Cisco Secure Workload (CSW).**

Cisco Secure Workload is a workload visibility and micro-segmentation platform. It discovers how applications communicate, turns that into label-based policy, and lets teams roll out least-privilege segmentation across data centers, public cloud, containers, and supported workload environments — without breaking the apps. This repo gives you everything you need to learn it: a written guide (Markdown / Word / PDF), a curated 31-entry video catalog with direct links, an onboarding runbook, and discovery and evidence checklists for POVs.

> **In one sentence:** CSW exists so that when — not if — one workload is compromised, the attacker cannot reach the next one.

## Contents

- [Who This Repo Is For](#who-this-repo-is-for)
- [The Problem CSW Solves](#the-problem-csw-solves)
- [Phased Adoption Roadmap](#phased-adoption-roadmap)
- [Quick Start: Where to Begin](#quick-start-where-to-begin)
- [Video Library](#video-library)
- [Suggested Watch Order](#suggested-watch-order)
- [Repository Layout](#repository-layout)
- [Regenerating the Documents](#regenerating-the-documents)
- [Related Cisco Secure Workload Repositories](#related-cisco-secure-workload-repositories)

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

**Key idea:** every phase is independently valuable. A customer who stops after Phase 2 still wins — ransomware fan-out is gone and prod is isolated from non-prod. A customer who reaches Phase 5 has continuous defense in depth, not a one-off project.

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
| **2 hours** | All ten videos in [Core CSW Training](#core-csw-training). |
| **A POV is on the table** | Skim Core CSW Training, watch [Production and Test Risk Reduction](https://www.youtube.com/watch?v=HKT18Ylt4IY) plus the integration videos that match the customer stack (firewall, F5, ISE, FMC). Then open [`docs/user-education/CSW-User-Education-Guide.md`](docs/user-education/CSW-User-Education-Guide.md) for the onboarding runbook and POV evidence checklist. |

## Video Library

34 videos and references grouped by theme. All links are YouTube unless explicitly marked otherwise (the firewall white-paper rows point to cisco.com).

### Core CSW Training

The foundational ten videos from the source Cisco slide.

| # | Video | Description | Link |
|---|---|---|---|
| 1 | Cisco Secure Workload: Agent Configuration Profile | Overview of configuring agent profiles to manage workload agents efficiently for security enforcement. | [Watch](https://www.youtube.com/watch?v=4mFriUr4WHk) |
| 2 | Cisco Secure Workload: Agent Configuration and Deployment – Golden Image VDI | Demonstrates deploying Secure Workload agents in virtual desktop infrastructure environments using golden images. | [Watch](https://www.youtube.com/watch?v=LYHnU_QjKfI) |
| 3 | Cisco Secure Workload: Scopes | Explains how to use scopes to group workloads logically for policy application and management. | [Watch](https://www.youtube.com/watch?v=3KBmanCNm4U) |
| 4 | Cisco Secure Workload: Labels | Details the use of labels to tag workloads for granular policy enforcement and visibility. | [Watch](https://www.youtube.com/watch?v=NLoZq0wiTU8) |
| 5 | Cisco Secure Workload: Inventory Filters | Shows how to filter inventory to focus on specific workloads or groups for analysis and policy. | [Watch](https://www.youtube.com/watch?v=fJd6V15UiZM) |
| 6 | Cisco Secure Workload: Production and Test Risk Reduction | Covers strategies to reduce risk in production and test environments using Secure Workload policies. | [Watch](https://www.youtube.com/watch?v=HKT18Ylt4IY) |
| 7 | Cisco Secure Workload: Application Dependency Mapping & Policy Analysis | Demonstrates mapping application dependencies and analyzing policies for effective microsegmentation. | [Watch](https://www.youtube.com/watch?v=Jzzblea25UA) |
| 8 | Cisco Secure Workload: Policy Visual and Quick Analysis | Provides tools for visualizing and quickly analyzing security policies and their impact. | [Watch](https://www.youtube.com/watch?v=uBxrJaVLHy4) |
| 9 | Cisco Secure Workload: Dynamic Workloads & Policy | Explains handling dynamic workloads and adapting policies accordingly. | [Watch](https://www.youtube.com/watch?v=Aajlx7JT2G4) |
| 10 | Cisco Secure Workload: Flow Analysis | Details flow analysis capabilities to understand traffic patterns and detect anomalies. | [Watch](https://www.youtube.com/watch?v=Tuw06kPjeyQ) |

### Security and Risk Reduction

| # | Video | Description | Link |
|---|---|---|---|
| 11 | Cisco Secure Workload: Vulnerabilities and Risk Reduction | Covers using Secure Workload to identify vulnerable workloads, prioritize risk, and reduce exposure. | [Watch](https://www.youtube.com/watch?v=l7LwZHXBYUA) |
| 12 | Cisco Secure Workload: Security Dashboard | Walks through the Secure Workload security dashboard: posture, risk indicators, and drill-downs. | [Watch](https://www.youtube.com/watch?v=_faK3p9tN4A) |
| 13 | Cisco Secure Workload: Forensics | Demonstrates Secure Workload's forensics capability for capturing process and flow evidence during investigations. | [Watch](https://www.youtube.com/watch?v=ZPBcj4e6M34) |
| 14 | Cisco Secure Workload: Log4J Risk Reduction | Shows how to use Secure Workload to identify and contain Log4J (Log4Shell) exposure across workloads. | [Watch](https://www.youtube.com/watch?v=FTXsWtFUJZM) |
| 15 | Cisco Secure Workload: SSH Risk Reduction | Demonstrates segmenting and controlling SSH paths between workloads using Secure Workload policy. | [Watch](https://www.youtube.com/watch?v=RV7To1MF6Es) |

### Segmentation Use Cases

| # | Video | Description | Link |
|---|---|---|---|
| 16 | Cisco Secure Workload: Terminal Services Segmentation | Covers segmenting Microsoft Terminal Services / Remote Desktop Services environments with Secure Workload. | [Watch](https://www.youtube.com/watch?v=pfv42g3FJEk) |
| 17 | Cisco Secure Workload: Virtual Desktop Interface (VDI) Segmentation | Covers segmenting VDI environments where many users share a small set of golden images. | [Watch](https://www.youtube.com/watch?v=SFVjiPQFsYA) |

### Secure Workload and Secure Firewall Integration

| # | Resource | Description | Link |
|---|---|---|---|
| 18 | Secure Workload & Firewall Integration (Part 1) | Part 1 of the integration series: introduction, design, and architecture. | [Watch](https://youtu.be/vdHjAl48SuI) |
| 19 | Secure Workload & Firewall Integration (Part 2) | Part 2: deployment patterns and policy flow. | [Watch](https://www.youtube.com/watch?v=xpbg3s0vrcI) |
| 20 | Secure Workload & Firewall Integration (Part 3) | Part 3: enforcement, telemetry, and operational considerations. | [Watch](https://www.youtube.com/watch?v=X65mwN7kJGg&t=53s) |
| 21 | Cisco Secure Workload and Secure Firewall White Paper | Public Cisco reference paper covering the joint architecture and design principles. | [Cisco.com](https://www.cisco.com/c/en/us/products/collateral/security/secure-workload/sec-workload-firewall-wp.html) |
| 22 | Secure Workload & Firewall Integration Deep Dive | Detailed reference on integration design principles, architecture, and use-cases. | [Read](https://secure.cisco.com/secure-workload/docs/secure-workload-whitepaper) |

### F5 / BIG-IP Integration

| # | Video | Description | Link |
|---|---|---|---|
| 23 | F5 BIG-IP and Cisco Tetration: APM Visibility | Shows how Secure Workload (formerly Tetration) ingests F5 BIG-IP APM data for application visibility. | [Watch](https://www.youtube.com/watch?v=dqbWhvFNsso&t=90s) |
| 24 | Cisco Tetration and F5 BIG-IP AFM | Covers integration with F5 BIG-IP AFM (Advanced Firewall Manager) for additional flow context. | [Watch](https://www.youtube.com/watch?v=HcF3yQHmeXc) |
| 25 | Cisco Tetration and F5 BIG-IP IPFIX Configuration | Configuration walk-through for sending IPFIX flow records from F5 BIG-IP into Secure Workload. | [Watch](https://www.youtube.com/watch?v=aJZEcZtUXDg) |

### Identity, DNS, and Other Integrations

| # | Video | Description | Link |
|---|---|---|---|
| 26 | Cisco Secure Workload — DNS Server Integration | Covers integrating DNS server context so workload-to-name mappings improve flow attribution and policy. | [Watch](https://www.youtube.com/watch?v=hD0WpBRLCiM) |
| 27 | Cisco Secure Workload — Infoblox Integration | Covers integrating Infoblox DNS / IPAM data for richer workload context inside Secure Workload. | [Watch](https://www.youtube.com/watch?v=gdhMWviAZig) |
| 28 | Cisco Secure Workload and Algosec Integration | Covers integrating Algosec for policy analysis and firewall-policy lifecycle alongside Secure Workload. | [Watch](https://www.youtube.com/watch?v=FUyESTLLZE8) |
| 29 | Cisco Secure Workload and ISE (In Action) | Demonstrates Secure Workload integration with Cisco ISE for user and device identity context. | [Watch](https://www.youtube.com/watch?v=KUJfuuhP1dc) |
| 30 | FMC Integration with Edge / Ingest / Appliance | Covers integrating Cisco FMC (Firewall Management Center) through Secure Workload's Edge, Ingest, and Appliance integration paths. | [Watch](https://youtu.be/13AZ33dpCxU) |
| 31 | Cisco ACI and CSW Integration | Covers integrating Cisco ACI (Application Centric Infrastructure) with Secure Workload so fabric-level network policy and workload-level segmentation work together. | [Watch](https://www.youtube.com/watch?v=u7jh3Zw1hlg) |

### Containers and Kubernetes

| # | Video | Description | Link |
|---|---|---|---|
| 32 | Cisco Secure Workload: Agent K8s | Demonstrates the Secure Workload agent in Kubernetes / containerized environments. | [Watch](https://www.youtube.com/watch?v=h9PW25UhXKs) |

### AI-Driven Policy and Analytics

| # | Video | Description | Link |
|---|---|---|---|
| 33 | Cisco Secure Workload: AI-Driven Policy Suggestions | Demonstrates how Secure Workload's AI engine generates policy recommendations from observed workload behavior, accelerating policy creation and tuning. | [Watch](https://www.youtube.com/watch?v=UwUJnEMZoTk) |
| 34 | Policy Statistics with Cisco Workloads AI Engine | Covers using the Secure Workload AI engine to surface policy statistics, anomalies, and tuning insights at scale. | [Watch](https://www.youtube.com/watch?v=kvnAoT5ZYXl) |

## Suggested Watch Order

The source Cisco slide does not prescribe a viewing order. For a new user, the progression below moves from foundations to deployment to policy and analytics, then opens up by use case and integration:

1. **Foundations** — Scopes (#3), Labels (#4), Inventory Filters (#5).
2. **Agent rollout** — Agent Configuration Profile (#1), then Agent Configuration and Deployment – Golden Image VDI (#2) if VDI is in scope.
3. **Core value: visibility → policy** — Application Dependency Mapping and Policy Analysis (#7), Flow Analysis (#10), Dynamic Workloads and Policy (#9), Policy Visual and Quick Analysis (#8), Production and Test Risk Reduction (#6).
4. **AI-augmented policy (advanced)** — AI-Driven Policy Suggestions (#33), Policy Statistics with AI Engine (#34) once the foundational policy workflow is understood.
5. **Security and risk** — Security Dashboard (#12), Vulnerabilities and Risk Reduction (#11), Forensics (#13), Log4J Risk Reduction (#14), SSH Risk Reduction (#15).
6. **Specific segmentation use cases** — Terminal Services (#16), VDI Segmentation (#17).
7. **Integrations as needed by the deal / POV** — Firewall (#18–#22), F5 / BIG-IP (#23–#25), DNS / Infoblox (#26, #27), Algosec (#28), ISE (#29), FMC (#30), ACI (#31).
8. **Containers** — Agent K8s (#32) when Kubernetes is in scope.

## Repository Layout

| Path | What it is |
|---|---|
| `README.md` | This file: intro, value story, full video catalog, suggested watch order. |
| `docs/user-education/CSW-User-Education-Guide.md` | Full Markdown guide: intro, concepts, video library, onboarding runbook, discovery questions, POV evidence checklist, pitfalls, talk track. |
| `docs/user-education/CSW-User-Education-Guide.docx` | Generated Word version of the guide. |
| `docs/user-education/CSW-User-Education-Guide.pdf` | Generated PDF version of the guide. |

The Markdown files are the source of truth. The `.docx` and `.pdf` artefacts are regenerated from Markdown — see below.

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

## Related Cisco Secure Workload Repositories

This repo is part of a family of public Cisco Secure Workload assets. Pick the one that matches the question on your desk.

| Repo | Use it for |
|---|---|
| [chandrapati/CSW-Compliance-Mapping](https://github.com/chandrapati/CSW-Compliance-Mapping) | Customer-facing compliance reports and matching SA / SE technical runbooks for 30+ frameworks (HIPAA, SOC 2, PCI DSS v4, NIST 800-53, ISO 27001:2022, CISA ZTMM, FIPS 140, NIST 800-207 / 207A, DORA, NIS2, NERC CIP, TSA Pipeline, CIS Controls v8.1, NIST CSF 2.0, CMMC 2.0, and more). |
| [chandrapati/CSW-Agent-Installation-Guide](https://github.com/chandrapati/CSW-Agent-Installation-Guide) | Practitioner reference for installing and operating the CSW host agent across Linux, Windows, cloud, container, and agentless environments. |
| [chandrapati/CSW-Policy-Lifecycle](https://github.com/chandrapati/CSW-Policy-Lifecycle) | Practitioner guide to the CSW policy lifecycle: discovery (ADM), analysis, enforcement (Monitor → Simulate → Enforce), and day-2 operations. |
| [chandrapati/CSW-Tenant-Insights](https://github.com/chandrapati/CSW-Tenant-Insights) | CISO and POV report flavors driven from live tenant evidence; companion to the compliance and automation repos. |
| [chandrapati/CSW_POV_Template](https://github.com/chandrapati/CSW_POV_Template) | Reusable CSW POV toolkit — clone once per engagement. |
| [chandrapati/csw_blast_radius_demo](https://github.com/chandrapati/csw_blast_radius_demo) | Hands-on blast-radius reduction demo. |
| [chandrapati/CSW-SE-Helper-Repo](https://github.com/chandrapati/CSW-SE-Helper-Repo) | SE helper utilities. |

Suggested reading order for a new SE / partner: **this repo → CSW-Agent-Installation-Guide → CSW-Policy-Lifecycle → CSW-Compliance-Mapping → CSW-Tenant-Insights**.
