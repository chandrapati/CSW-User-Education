# Cisco Secure Workload — User Education

**A practical, vendor-neutral learning path for understanding and explaining Cisco Secure Workload (CSW).**

> **Disclaimer:** This repository is **not** official Cisco product documentation. It is companion learning material maintained for customer and partner education. Always validate design, scope, and supported features against your tenant's in-product documentation and [Cisco Secure Workload product documentation](https://www.cisco.com/c/en/us/products/security/workload-security/index.html) before production decisions.
>
> **Video attributions:** All videos linked in this repository are the property of their respective creators and channels. Full credit to:
> - **Jason Maynard** — ["How Hard Can It Be?" CSW series](https://www.youtube.com/@jasonmaynard8773) and the [Cisco Secure Workload deep-dive playlist](https://www.youtube.com/playlist?list=PLyf18hdY22ESRYAoYLcJaehao1W8y9XFv) (Modules 1–8, and deep-dive content in Modules 3, 5, 6, 7, 11, 13, 16)
> - **Jorge Quintero, Jason Lunde & Amandeep Singh** (Cisco TMEs) — [Cisco Secure Workload official YouTube channel](https://www.youtube.com/@ciscosecureworkload) (Modules 9–15)
> - **BarrySecure** — [BarrySecure YouTube channel](https://www.youtube.com/@BarrySecure) (CSW 101 overview demo)
>
> This repo curates and organizes their publicly available content into a structured learning path. No content has been reproduced or modified — all links go directly to the original videos.

Cisco Secure Workload is a workload visibility and micro-segmentation platform. It discovers how applications communicate, turns that into label-based policy, and lets teams roll out least-privilege segmentation across data centers, public cloud, containers, and supported workload environments — without breaking the apps. This repo gives you everything you need to learn it: a written guide (Markdown / Word / PDF), a curated **84-entry** video catalog with direct links, an onboarding runbook, and discovery and evidence checklists for POVs.

> **In one sentence:** CSW exists so that when — not if — one workload is compromised, the attacker cannot reach the next one.

## Contents

- [Who This Repo Is For](#who-this-repo-is-for)
- [The Problem CSW Solves](#the-problem-csw-solves)
- [How Cisco Secure Workload Works](#how-cisco-secure-workload-works)
- [Micro-segmentation Is a Journey](#micro-segmentation-is-a-journey)
- [Phased Adoption Roadmap](#phased-adoption-roadmap)
- [Quick Start: Where to Begin](#quick-start-where-to-begin)
- [Video Library (Learning Path Order)](#video-library-learning-path-order)
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

Visually, here is the difference CSW makes — the *same* ransomware attack **without** micro-segmentation (it fans out and encrypts the whole estate) versus **with** Cisco Secure Workload (the breach is contained to the one workload the attacker landed on):

![Ransomware blast radius: without micro-segmentation the entire estate is encrypted; with Cisco Secure Workload the breach is contained to a single workload](assets/csw-containment.gif)

> **What the animation shows:** CSW intervenes between **steps 4 and 5** of the kill chain. Least-privilege policy removes the workload-to-workload network paths that recon, credential theft, lateral movement, and privilege escalation all depend on. The attacker can still land on host 1, but cannot reach hosts 2..N from there — so the blast radius is a single workload instead of the entire data center.

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

## How Cisco Secure Workload Works

CSW runs one repeatable pipeline — **see everything → add context → discover the policy → prove it's safe → enforce it everywhere** — driven from a single policy “brain” with distributed enforcement at the workload (agent), the network (Cisco Secure Firewall, agentless), and the cloud (security groups):

![How Cisco Secure Workload works: visibility, context, ADM discovery, analysis and simulation, then enforcement across agent, Secure Firewall, and cloud security groups](assets/csw-architecture.gif)

| Stage | What happens |
|---|---|
| **1 · Visibility** | Agents and connectors stream every flow and process across VM, bare-metal, container, cloud, and Kubernetes workloads. |
| **2 · Context** | Workloads are labeled from systems of record — CMDB, cloud tags, ISE, DNS — so policy is written in human terms, not IP addresses. |
| **3 · Discovery** | ADM + machine learning auto-discover application dependencies and propose least-privilege allow-list policy. |
| **4 · Analysis** | Policy is simulated and validated against live traffic so it won't break the application before enforcement. |
| **5 · Enforcement** | One policy is pushed everywhere: host OS firewall (agent), Cisco Secure Firewall (agentless), and cloud security groups. |

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

![Phased adoption roadmap: Phase 1 Visibility (weeks 0–2), Phase 2 Macro Segmentation (weeks 2–4), Phase 3 ADM-driven App micro-segmentation (weeks 4–12), and Phases 4–5 (Vulnerability-Driven Risk Reduction and Forensics & IR) running continuously from week 8 onward](assets/csw-roadmap.png)

| Phase | Window | What you do | What you ship | Primary value |
|---|---|---|---|---|
| **1 — Visibility** | Week 0–2 | Deploy agents on a representative slice. Turn on cloud, CMDB, identity, and DNS connectors. Import existing labels. | Workload inventory, label dictionary, L3 / L4 + process flow data, baseline dependency view. | See what you actually have, with real flow truth — often the first time application owners can answer "who does this server talk to?". |
| **2 — Macro Segmentation** | Week 2–4 | Apply broad zone-to-zone policy in monitor mode, then enforcement: prod ↔ non-prod, prod ↔ dev / test / staging, user VLANs ↔ server zones. Deny lateral admin protocols (SMB, RDP, WinRM, WMI, PsExec, SSH) where no business app needs them. Isolate the backup tier and identity tier. | Enforced macro policy with monitor-mode evidence and rollback plan. | **Biggest blast-radius reduction for the lowest effort.** Ransomware fan-out paths are cut. The prod / non-prod story holds up in audit. High-value tiers (backup, AD, hypervisor) are reachable only from where they should be. |
| **3 — ADM + App-Scope Micro-Segmentation** | Week 4–12 (per application wave) | Run ADM on a chosen application. Review the dependency map with the app owner. Convert observed flows + labels into recommended allow rules. Move to monitor mode, tune, then staged enforcement. Repeat for the next app wave. | Per-app dependency map, modeled policy, blocked-flow evidence, allowed-business-transaction evidence, app-owner signoff. | True micro-segmentation around the application itself. Per-tier policy (web → app → db). App teams understand their own application, sometimes for the first time. |
| **4 — Vulnerability-Driven Risk Reduction** | Continuous from ~Week 8 | Ingest vulnerability data (scanner exports, CVE feeds). Tag workloads with risk labels (for example `risk:high`, `cve:exploitable`). Tighten policy automatically for high-risk workloads — restrict their reachable surface to admin / patch paths only until remediated. | Risk-tagged inventory, tightened policy on vulnerable workloads, security and audit evidence. | Defenders work the problems attackers actually try. When the next Log4J / Log4Shell-class CVE lands, exposure can be shrunk within the same day instead of waiting on patch cycles. |
| **5 — Forensics and Anomaly Detection** | Continuous from ~Week 8 | Use Secure Workload forensics events, flow-pattern anomaly detection, and SIEM / SOAR integration. Build playbooks that pair policy violations with host evidence. | Forensics events, anomaly findings, SOC playbooks, IR evidence trails. | Detection compounds with segmentation. Every blocked flow becomes evidence. Mean-time-to-detect drops because workload behavior is bounded by policy. |

**Key idea:** every phase is independently valuable. A customer who stops after Phase 2 still wins — ransomware fan-out is gone and prod is isolated from non-prod. A customer who reaches Phase 5 has continuous defense in depth — and should keep operating there, because [applications and policy both keep changing](#micro-segmentation-is-a-journey).

### Mapping phases to videos in the catalog

- **Phase 1 — Visibility:** Agent Configuration Profile, Scopes, Labels, Inventory Filters, Flow Analysis.
- **Phase 2 — Macro Segmentation:** SSH Risk Reduction, Terminal Services Segmentation, Production and Test Risk Reduction, VDI Segmentation.
- **Phase 3 — ADM + App-Scope Micro:** Application Dependency Mapping & Policy Analysis, Policy Visual and Quick Analysis, Dynamic Workloads & Policy, AI-Driven Policy Suggestions, Policy Statistics with AI Engine.
- **Phase 4 — Vulnerability-Driven Risk Reduction:** Vulnerabilities and Risk Reduction, Log4J Risk Reduction, Security Dashboard.
- **Phase 5 — Forensics and Anomaly Detection:** Forensics, Flow Analysis, Security Dashboard.

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

84 videos and references arranged in the order that builds CSW skills fastest: concepts first, then agents, then visibility → policy, then security outcomes, then environment-specific depth. Modules 1–8 are the original learning-path series; **Modules 9–15 add the newer official Cisco Secure Workload channel demos (2025–2026)**; **Module 16 covers Incident Response scenarios**. **Watch top to bottom** within each module; skip modules that do not match your POV (for example, skip Module 2 VDI if you are not deploying to golden-image desktops).

---

### 🎬 Start Here — CSW 101 Introduction

> **New to Cisco Secure Workload? Watch this first.**
> A complete product overview and end-to-end live demo — covers what CSW is, how it discovers application dependencies, and how it enforces least-privilege policy.

| Video | Description |
|---|---|
| [Cisco Secure Workload — Overview & Live Demo](https://www.youtube.com/watch?v=8v6BQYrO5v8&t=2s) | End-to-end product walkthrough — what CSW does, how it works, and why it matters. Best first watch before any module below. |

---

### Module 1 — Foundations (start here)

Learn how CSW organizes workloads before any policy work.

| Video | Description |
|---|---|
| [Cisco Secure Workload: Scopes](https://www.youtube.com/watch?v=3KBmanCNm4U) | Group workloads logically for policy application and management. |
| [Cisco Secure Workload: Labels](https://www.youtube.com/watch?v=NLoZq0wiTU8) | Tag workloads for granular policy enforcement and visibility. |
| [Cisco Secure Workload: Inventory Filters](https://www.youtube.com/watch?v=fJd6V15UiZM) | Filter inventory to focus on specific workloads or groups. |

### Module 2 — Agent deployment

Roll out telemetry collection on workloads.

| Video | Description |
|---|---|
| [Cisco Secure Workload: Agent Configuration Profile](https://www.youtube.com/watch?v=4mFriUr4WHk) | Configure agent profiles to manage workload agents for security enforcement. |
| [Agent Configuration and Deployment – Golden Image VDI](https://www.youtube.com/watch?v=LYHnU_QjKfI) | Deploy agents in VDI environments using golden images. *Skip if VDI is not in scope.* |
| [Windows Deep Visibility Agent Install](https://www.youtube.com/watch?v=Nsju3KePVtc) | Step-by-step Windows agent installation for deep visibility and enforcement. |

### Module 3 — Visibility and dependency discovery

See what talks to what — the core CSW value story.

| Video | Description |
|---|---|
| [Production and Test Risk Reduction](https://www.youtube.com/watch?v=HKT18Ylt4IY) | Macro-segment prod vs non-prod — fast blast-radius win. |
| [Flow Analysis](https://www.youtube.com/watch?v=Tuw06kPjeyQ) | Understand traffic patterns and anomalies from observed flows. |
| [Application Dependency Mapping & Policy Analysis](https://www.youtube.com/watch?v=Jzzblea25UA) | Map application dependencies and derive microsegmentation policy. |
| [Dynamic Workloads & Policy](https://www.youtube.com/watch?v=Aajlx7JT2G4) | Adapt policy as workloads move or scale. |
| [Policy Visual and Quick Analysis](https://www.youtube.com/watch?v=uBxrJaVLHy4) | Visualize and analyze policy impact before enforcement. |
| [Manual Inventory Upload (Tagging)](https://www.youtube.com/watch?v=b5cegbbA3UM) | Bulk-upload and tag workload inventory when agents are not yet deployed. |
| [Application Dependency Mapping Discovery](https://www.youtube.com/watch?v=PZ4wNulQVek) | Run first-pass ADM to surface all application communication flows. |
| [Application Dependency Mapping Drilling into Policies](https://www.youtube.com/watch?v=NsGuQiooziY) | Deep-dive into ADM results: drill flows into policy rules. |

### Module 4 — AI-assisted policy (after Module 3)

Accelerate policy creation once the manual workflow is clear.

| Video | Description |
|---|---|
| [AI-Driven Policy Suggestions](https://www.youtube.com/watch?v=UwUJnEMZoTk) | AI-generated policy recommendations from observed behavior. |
| [Policy Statistics with Cisco Workloads AI Engine](https://www.youtube.com/watch?v=kvnAoT5ZYXl) | Policy statistics, anomalies, and tuning insights at scale. |

### Module 5 — Security, risk, and forensics

Operationalize risk reduction and incident evidence.

| Video | Description |
|---|---|
| [Security Dashboard](https://www.youtube.com/watch?v=_faK3p9tN4A) | Posture, risk indicators, and drill-downs. |
| [Vulnerabilities and Risk Reduction](https://www.youtube.com/watch?v=l7LwZHXBYUA) | Prioritize and reduce exposure on vulnerable workloads. |
| [SSH Risk Reduction](https://www.youtube.com/watch?v=RV7To1MF6Es) | Control SSH paths between workloads. |
| [Log4J Risk Reduction](https://www.youtube.com/watch?v=FTXsWtFUJZM) | Identify and contain Log4Shell-class exposure. |
| [Forensics](https://www.youtube.com/watch?v=ZPBcj4e6M34) | Process and flow evidence for investigations. |
| [Software Vulnerability and Adaptive Policy](https://www.youtube.com/watch?v=MSJcNB2xtBk) | Automatically tighten policy for vulnerable workloads using CVE data. |
| [Vulnerabilities Dashboard](https://www.youtube.com/watch?v=29-S5hl4g7M) | Explore the vulnerability dashboard: CVSS scores, workload exposure, and risk reduction. |

### Module 6 — Segmentation use cases

Deep dives when the customer environment matches.

| Video | Description |
|---|---|
| [Terminal Services Segmentation](https://www.youtube.com/watch?v=pfv42g3FJEk) | Segment RDS / Terminal Services environments. |
| [VDI Segmentation](https://www.youtube.com/watch?v=SFVjiPQFsYA) | Segment shared golden-image VDI estates. |
| [Security Mandate: Secured SSH Access](https://www.youtube.com/watch?v=CEIt5LZ0_98) | Enforce SSH access control across IT and SecOps workloads using policy mandates. |
| [Shared Services Mandate: Time Services](https://www.youtube.com/watch?v=sPHxgp65Ols) | Allow NTP/time services to all datacenter resources while blocking everything else. |
| [Web Services Mandate: Prod/Test Isolation](https://www.youtube.com/watch?v=xu78UvPXbMw) | Enforce that production and test environments cannot communicate. |
| [Retail Web Services Mandate: Limit Web Access](https://www.youtube.com/watch?v=i9EI9FpuDeE) | Restrict outbound web access for retail workloads using scoped mandates. |
| [Deep Dive Segmentation](https://www.youtube.com/watch?v=8zcKVLJQuzw) | Advanced segmentation walkthrough: absolute policy, catch-alls, and enforcement tuning. |

### Module 7 — Integrations (pick what matches the stack)

Watch only the rows relevant to the customer POV.

| Video | Description |
|---|---|
| [Secure Workload & Firewall Integration (Part 1)](https://youtu.be/vdHjAl48SuI) | Introduction, design, and architecture. |
| [Secure Workload & Firewall Integration (Part 2)](https://www.youtube.com/watch?v=xpbg3s0vrcI) | Deployment patterns and policy flow. |
| [Secure Workload & Firewall Integration (Part 3)](https://www.youtube.com/watch?v=X65mwN7kJGg&t=53s) | Enforcement, telemetry, and operations. |
| [Secure Workload and Secure Firewall White Paper](https://www.cisco.com/c/en/us/products/collateral/security/secure-workload/sec-workload-firewall-wp.html) | Joint architecture reference (Cisco.com). |
| [Secure Workload & Firewall Integration Deep Dive](https://secure.cisco.com/secure-workload/docs/secure-workload-whitepaper) | Design principles and use cases. |
| [F5 BIG-IP and Cisco Tetration: APM Visibility](https://www.youtube.com/watch?v=dqbWhvFNsso&t=90s) | F5 APM data for application visibility. |
| [Cisco Tetration and F5 BIG-IP AFM](https://www.youtube.com/watch?v=HcF3yQHmeXc) | F5 AFM flow context integration. |
| [F5 BIG-IP IPFIX Configuration](https://www.youtube.com/watch?v=aJZEcZtUXDg) | Send IPFIX from BIG-IP into Secure Workload. |
| [DNS Server Integration](https://www.youtube.com/watch?v=hD0WpBRLCiM) | DNS context for flow attribution and policy. |
| [Infoblox Integration](https://www.youtube.com/watch?v=gdhMWviAZig) | Infoblox DNS / IPAM context in CSW. |
| [Algosec Integration](https://www.youtube.com/watch?v=FUyESTLLZE8) | Firewall-policy lifecycle alongside CSW. |
| [ISE (In Action)](https://www.youtube.com/watch?v=KUJfuuhP1dc) | User and device identity from Cisco ISE. |
| [FMC Integration with Edge / Ingest / Appliance](https://youtu.be/13AZ33dpCxU) | FMC through Edge, Ingest, and appliance paths. |
| [ACI and CSW Integration](https://www.youtube.com/watch?v=u7jh3Zw1hlg) | ACI fabric policy with workload segmentation. |
| [Splunk Integration (SIEM)](https://youtu.be/CRnkH9imTZk) | Three patterns: Cisco Security Cloud App for baseline dashboards/datasets, CSW → Splunk Syslog alerts, and Splunk-driven Python against the CSW API for arbitrary metadata. |
| [CI/CD Pipeline Integration](https://www.youtube.com/watch?v=0wsSA69ol0M) | Treat CSW like any other declarative system: labels, scopes, and policy live in git and reach the tenant through pipeline-driven API calls. |
| [Agentless with Firepower Threat Defence](https://www.youtube.com/watch?v=S9TFfvbiJdc) | Use FTD as an agentless telemetry source for workloads where agent install is not possible. |

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

**Cisco Secure Firewall (NSEL + FMC enforcement) — all the relevant videos are rows 20–24, 32, and 59 above.** For a full step-by-step guide covering NSEL ingest, FlexConfig, FMC connector, and enforcement validation, see [**CSW-Secure-Firewall-Integration-Guide**](https://github.com/chandrapati/CSW-Secure-Firewall-Integration-Guide) — the complete guide is also available locally at [`docs/user-education/CSW-Secure-Firewall-Integration-Guide.md`](docs/user-education/CSW-Secure-Firewall-Integration-Guide.md).

### Module 8 — Containers and Kubernetes

When Kubernetes is in scope.

| Video | Description |
|---|---|
| [Agent K8s](https://www.youtube.com/watch?v=h9PW25UhXKs) | Secure Workload agent in Kubernetes environments. |

### Module 9 — Official Channel: Getting Started

Newer overview content published directly on the [Cisco Secure Workload YouTube channel](https://www.youtube.com/@ciscosecureworkload) (2025–2026). Use these as the most current "start here" demos.

| Video | Description |
|---|---|
| [Introduction to Secure Workload & Overview Demo](https://youtu.be/8HpUkYXbHnw) | Current product overview and end-to-end demo from the official Cisco channel. |
| [Inventory Filters (channel version)](https://youtu.be/ymCB_PkFYcI) | Official-channel refresh of inventory filtering. |

### Module 10 — Connectors, Telemetry & Application Discovery

How CSW ingests context and discovers applications before policy work.

| Video | Description |
|---|---|
| [Connector Overview](https://youtu.be/H6QxuouzeC8) | What connectors do and how they enrich telemetry. |
| [Connector Deployment](https://youtu.be/H0as2ppS84Q) | Deploying connectors on the virtual appliances. |
| [Provided Services](https://youtu.be/2dGQ9winZwE) | Built-in services on the appliances. |
| [Basic Application Discovery](https://youtu.be/HGvtBonFiE4) | First-pass ADM to surface application dependencies. |
| [Enhancing Application Discovery](https://youtu.be/4wa7PiHGUnM) | Improve ADM fidelity with labels and context. |

### Module 11 — Policy Lifecycle & Enforcement (deep dive)

The full policy workflow from modeling through enforcement placement.

| Video | Description |
|---|---|
| [Policy Lifecycle](https://youtu.be/Cm-cUwRorDc) | End-to-end policy lifecycle overview. |
| [Policy Validation and Analysis](https://youtu.be/DgaZpQ0lnAI) | Validate and analyze policy before enforcing. |
| [Policy Ordering](https://youtu.be/fG1Kn1C7QRM) | How rule order affects enforcement outcomes. |
| [Policy Enforcement Overview](https://youtu.be/A8rOXQ-y4Cw) | How enforcement is applied across workloads. |
| [Where to Enforce](https://youtu.be/urFJyDERMFs) | Choosing the right enforcement point (host / network / cloud). |
| [Container Enforcement](https://youtu.be/6Z_y_keYyE0) | Enforce policy on containerized workloads. |
| [Windows Process-Level Enforcement](https://youtu.be/frhcPHXQkNw) | Process-aware enforcement on Windows hosts. |
| [Policy Analysis and Enforcement](https://www.youtube.com/watch?v=NUKFwkZfdug) | Analyse policy intent vs enforcement state; identify gaps before locking down. |
| [Quick Analysis and Absolute Policy](https://www.youtube.com/watch?v=UjdBrDLpmGg) | Use quick analysis to validate flows, then lock scope with absolute policy. |
| [Security Incident and Absolute Policy](https://www.youtube.com/watch?v=DVrswUyuplM) | Use absolute policy to contain a scope during an active security incident. |

### Module 12 — Security, Forensics & Alerting

| Video | Description |
|---|---|
| [Security Dashboard and Forensics](https://youtu.be/PVRkzWRAa08) | Combined posture, risk, and forensic evidence walkthrough. |
| [Alerting](https://youtu.be/RqM6vbDEDPc) | Configure and route CSW alerts. |

### Module 13 — Day-2 Operations & Platform Management

Operate, audit, and protect the CSW platform itself.

| Video | Description |
|---|---|
| [Agent Operations](https://youtu.be/EIqPiPgpDqc) | Manage and maintain deployed agents. |
| [Auditing](https://youtu.be/_5K62x49c_I) | Audit trails for changes and access. |
| [Data Backup and Restore](https://youtu.be/dVK0xe4RWh4) | Back up and restore tenant/cluster data. |
| [Federation](https://youtu.be/465loG3VlZE) | Multi-cluster federation for scale. |
| [Managing Secure Workload in Security Cloud Control](https://youtu.be/UVTkxaUJSHA) | SaaS management via Security Cloud Control (SCC). |
| [Global Visualization Updates](https://youtu.be/kGLEKRltV2M) | Visualization enhancements. |
| [Global Visualization (deep-dive)](https://www.youtube.com/watch?v=KRbnrk0ge_Q) | Detailed walkthrough of the global visualization view across all scopes. |
| [Reports](https://www.youtube.com/watch?v=sbpEz0pU-Wc) | Generate and schedule compliance and operational reports from CSW. |

### Module 14 — Integrations (newer)

| Video | Description |
|---|---|
| [Secure Workload & Secure Firewall Integration Updates](https://youtu.be/IEqbz44YvOQ) | Latest firewall integration updates (supersedes the 3-part series for current behavior). |

### Module 15 — Strategy & Architecture

Executive- and architecture-level framing for segmentation programs.

| Video | Description |
|---|---|
| [Campus and Zero Trust](https://youtu.be/hX9Q6IYcgXA) | Extend Zero Trust segmentation into the campus. |
| [Enabling Consistent Multi-Cloud Security, Forensics & IR](https://youtu.be/x-dMr3Kg4dg) | Consistent policy and IR across multi-cloud. |
| [How to Create a Comprehensive Zero Trust Strategy](https://youtu.be/1jvgXt906m8) | Building an end-to-end Zero Trust strategy. |
| [Modern-Day Risk Reduction in Healthcare: Prescriptive-Based Policy](https://www.youtube.com/watch?v=eYbojr_h5ic) | Industry use case — applying CSW prescriptive policy to reduce healthcare workload exposure. |


### Module 16 — Incident Response (IR Deep Dive)

Use CSW forensics, flow evidence, and MITRE ATT&CK–mapped scenarios to investigate and contain incidents. Watch when a breach or suspicious behavior is under investigation.

| Video | Description |
|---|---|
| [Incident Response: Network Traffic](https://www.youtube.com/watch?v=cqkPbdq0hzM) | Use CSW flow data and forensics to investigate suspicious network traffic during an incident. |
| [Incident Response: T1156 — Create User](https://www.youtube.com/watch?v=ggTtqyzXaMM) | Detect and investigate MITRE ATT&CK T1156 (local account creation) with CSW process forensics. |
| [Incident Response: T1552 — Unsecured Credentials](https://www.youtube.com/watch?v=z-8Lw5fMeNw) | Detect credential harvesting (T1552) using CSW process and flow evidence. |
| [Incident Response: Vulnerability RDP Client](https://www.youtube.com/watch?v=dmpt3zjqrME) | Investigate an RDP-based vulnerability exploitation attempt using CSW telemetry. |

> **Video credits:** All linked videos are the property of their respective creators — this repo organizes and links to their public content without modification.
> - **Jason Maynard** ([@jasonmaynard8773](https://www.youtube.com/@jasonmaynard8773)) — "How Hard Can It Be?" CSW series (Modules 1–8) and the [Cisco Secure Workload deep-dive playlist](https://www.youtube.com/playlist?list=PLyf18hdY22ESRYAoYLcJaehao1W8y9XFv) (additional content in Modules 3, 5, 6, 7, 11, 13, 16). His recent channel uploads have shifted toward Cisco Secure Access / SOC topics.
> - **Jorge Quintero, Jason Lunde & Amandeep Singh** — Cisco TMEs publishing on the official [Cisco Secure Workload channel](https://www.youtube.com/@ciscosecureworkload) (Modules 9–15). Use these for the most current product behavior.
> - **BarrySecure** ([@BarrySecure](https://www.youtube.com/@BarrySecure)) — Cisco security practitioner demos covering CSW and the broader Cisco security portfolio (CSW 101 intro).

## Repository Layout

| Path | What it is |
|---|---|
| [`README.md`](README.md) | This file: intro, value story, video library in learning-path order. |
| [`docs/user-education/CSW-User-Education-Guide.md`](docs/user-education/CSW-User-Education-Guide.md) | Full Markdown guide: intro, concepts, video library, onboarding runbook, discovery questions, POV evidence checklist, pitfalls, talk track. |
| [`docs/user-education/CSW-Secure-Firewall-Integration-Guide.md`](docs/user-education/CSW-Secure-Firewall-Integration-Guide.md) | Step-by-step Secure Firewall NSEL ingest + FMC enforcement integration with video links. |
| [`docs/user-education/CSW-User-Education-Guide.docx`](docs/user-education/CSW-User-Education-Guide.docx) | Generated Word version of the guide. |
| [`docs/user-education/CSW-User-Education-Guide.pdf`](docs/user-education/CSW-User-Education-Guide.pdf) | Generated PDF version of the guide. |

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

---

## Related Cisco Secure Workload Resources

| Repository | Description | Best for |
|------------|-------------|---------|
| [User Education](https://github.com/chandrapati/CSW-User-Education) | Onboarding guides and concept explainers | New CSW users |
| [Agent Installation](https://github.com/chandrapati/CSW-Agent-Installation-Guide) | Deploy CSW agents on Linux / Windows / cloud | Day-1 sensor deployment |
| [Policy Lifecycle](https://github.com/chandrapati/CSW-Policy-Lifecycle) | Policy discovery → enforcement workflow | Policy management |
| [ISE / pxGrid](https://github.com/chandrapati/csw-ise-integration) | ISE/pxGrid: user-identity–aware microsegmentation | Identity & Zero Trust |
| [AnyConnect NVM](https://github.com/chandrapati/csw-anyconnect-nvm) | Endpoint process flows + user identity via NVM | Endpoint telemetry |
| [ServiceNow CMDB](https://github.com/chandrapati/csw-servicenow-integration) | ServiceNow CMDB label enrichment for workload scopes | CMDB-driven policy |
| [AWS Connector](https://github.com/chandrapati/csw-aws-connector) | EC2 tag ingestion + VPC flow logs + Security Group enforcement | AWS workloads |
| [Azure Connector](https://github.com/chandrapati/csw-azure-connector) | Azure VM tag ingestion + VNet flow logs + NSG enforcement | Azure workloads |
| [GCP Connector](https://github.com/chandrapati/csw-gcp-connector) | GCE label ingestion + VPC flow logs + firewall enforcement | GCP workloads |
| [NetFlow](https://github.com/chandrapati/csw-netflow-integration) | NetFlow v9/IPFIX agentless flow ingestion from switches | Network fabric visibility |
| [ERSPAN](https://github.com/chandrapati/csw-erspan-integration) | Agentless packet mirroring for legacy / OT / IoT devices | Deep agentless visibility |
| [Secure Firewall](https://github.com/chandrapati/CSW-Secure-Firewall-Integration-Guide) | NSEL flow ingestion from Cisco Secure Firewall (FTD/ASA) | Firewall flow visibility |
| [Splunk Integration](https://github.com/chandrapati/csw-splunk-integration) | CSW syslog alerts → Splunk SIEM | SecOps / SIEM teams |
| [Compliance Mapping](https://github.com/chandrapati/CSW-Compliance-Mapping) | Map CSW controls to NIST, PCI-DSS, HIPAA, CIS | Compliance & audit |
| [Tenant Insights](https://github.com/chandrapati/CSW-Tenant-Insights) | Tenant-level reporting and analytics | Visibility metrics |
| [Operations Toolkit](https://github.com/chandrapati/CSW-Operations-Toolkit) | Day-2 ops scripts: health checks, reporting, policy analysis | Ongoing operations |

> **Suggested customer journey:**  
> User Education → Agent Installation → Policy Lifecycle → ISE/pxGrid → ServiceNow CMDB → Splunk Integration → Compliance Mapping → Operations Toolkit