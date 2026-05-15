# Cisco Secure Workload User Education

Generic learning material for understanding, explaining, and onboarding **Cisco Secure Workload (CSW)**.

This repository is designed for anyone who needs a practical CSW learning path: customers, partners, SEs, account teams, delivery teams, and engineers.

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

## Video URLs

The current video section includes placeholder rows because the screenshot provided only showed visible **Watch here** text, not the underlying URLs. Replace `URL needed` with the actual video links when available.

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

