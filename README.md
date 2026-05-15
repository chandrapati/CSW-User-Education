# Cisco Secure Workload User Education

Generic learning material for understanding, explaining, and onboarding **Cisco Secure Workload (CSW)**.

This repository is designed for anyone who needs a practical CSW learning path: customers, partners, SEs, account teams, delivery teams, and engineers.

## What CSW Solves

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
| Spreading to dev/test/lab | Hard-segment prod from non-prod so a non-prod compromise cannot pivot into prod. |
| Long undetected dwell time | Surface every blocked or anomalous flow as evidence for SOC and incident response. |

The result is that **ransomware that lands on one workload finds the network around it almost empty**: the protocols it needs to spread are blocked by policy, and every attempt is logged.

### Why We Need It

- **Flat networks no longer match the threat model.** Perimeter firewalls do not stop an attacker who is already inside.
- **Identity-based and EDR controls are necessary but not sufficient.** They catch behavior on the host; CSW removes the network paths the attacker would use between hosts.
- **Crown-jewel applications need explicit protection.** Payments, claims, customer data, intellectual property, and backup infrastructure should not be reachable from a random user workstation or low-tier dev server.
- **Compliance and audit demand it.** PCI, HIPAA, SOX, and most internal security frameworks expect documented segmentation between regulated and non-regulated systems.
- **It must not break applications.** CSW's discovery-first model (map dependencies → label workloads → model policy → enforce in stages) is what makes segmentation finally feasible in real enterprises.

In one sentence: **CSW exists so that when — not if — one workload is compromised, the attacker cannot reach the next one.**

## Contents

| File | Purpose |
|---|---|
| `docs/user-education/CSW-User-Education-Guide.md` | Main editable Markdown guide |
| `docs/user-education/CSW-User-Education-Guide.docx` | Generated Word version |
| `docs/user-education/CSW-User-Education-Guide.pdf` | Generated PDF version |

## What This Guide Covers

- What CSW is, in practical user-friendly language.
- How to position CSW for application dependency mapping and micro-segmentation.
- A curated video-library section with short descriptions.
- A lightweight onboarding runbook from discovery to enforcement.
- A checklist for what teams should collect before a CSW POV.

## Video Library

The guide includes a curated **CSW Video Library** with 31 entries grouped into seven sub-sections:

| Sub-section | Coverage |
|---|---|
| 5.1 Core CSW Training | Foundational ten videos from the Cisco source slide (Agent Configuration Profile, Golden Image VDI, Scopes, Labels, Inventory Filters, Production / Test Risk Reduction, ADM and Policy Analysis, Policy Visual and Quick Analysis, Dynamic Workloads, Flow Analysis). |
| 5.2 Security and Risk Reduction | Vulnerabilities and Risk Reduction, Security Dashboard, Forensics, Log4J, SSH. |
| 5.3 Segmentation Use Cases | Terminal Services, VDI segmentation. |
| 5.4 Secure Workload + Secure Firewall | Three-part integration series plus public and deep-dive whitepapers. |
| 5.5 F5 / BIG-IP | APM visibility, AFM, and IPFIX configuration. |
| 5.6 Identity, DNS, and Other Integrations | DNS, Infoblox, Algosec, ISE, FMC (via Edge / Ingest / Appliance). |
| 5.7 Containers and Kubernetes | Agent K8s. |

All entries link to YouTube unless explicitly marked otherwise (the two firewall whitepapers point to cisco.com). The guide also includes a **Suggested Watch Order** that moves a new user from foundations → agent rollout → policy → security → use cases → integrations → containers.

Open `docs/user-education/CSW-User-Education-Guide.md` (or the generated `.docx` / `.pdf`) for the full table with links.

## Regenerating the Documents

From the repo root:

```bash
pandoc docs/user-education/CSW-User-Education-Guide.md \
  --from gfm \
  --to docx \
  --toc \
  --toc-depth=2 \
  -o docs/user-education/CSW-User-Education-Guide.docx

cd docs/user-education
soffice --headless --convert-to pdf CSW-User-Education-Guide.docx
```

