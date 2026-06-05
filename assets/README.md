# Diagram assets

Original, vendor-neutral animated diagrams for the repo README. No Cisco
copyrighted artwork is used.

| File | Shows |
|---|---|
| `csw-containment.gif` | Ransomware blast radius **without** micro-segmentation (fans out across the estate) vs **with** Cisco Secure Workload (contained to one workload). |
| `csw-architecture.gif` | How CSW works: visibility → context → ADM discovery → analysis/simulation → enforcement across agent, Secure Firewall, and cloud. |

Regenerate (requires `pillow`):

```bash
python3 assets/make_gifs.py
```
