# Dev Diary - Oncology Clinical Trials Diagnostic

This is my day-by-day build log for the second project: what I did, what I decided and why, what I learned, and what confused me.

---

## Day 1 - Project Setup
**Date:** 15 September 2026

**What I did:**
Set up the repo, local environment, and folder structure for the second project - a diagnostic of oncology clinical trial performance using real ClinicalTrials.gov data. Researched the ClinicalTrials.gov API v2 (real, current documentation) and wrote the roadmap doc, same structure as the first project.

**Why I made that choice:**
Chose clinical trials data specifically to close a real gap from the first project - the health indicators dataset was a single flat table, so no query ever needed a real join. This dataset naturally splits into related entities (trials, sponsors, conditions), which forces genuine joins and window functions, the SQL depth that actually shows up in technical interviews.

**What I learned:**
Setup went much faster and smoother this time - venv, packages, Git init, remote linking, folder structure, all with no real confusion, compared to how much troubleshooting the same steps needed on the first project. First real evidence that the fundamentals have actually stuck.

**What confused me / what I'd do differently:**
Small Git hiccup - the first push failed because the branch had no upstream set yet, same first-push issue as the very first project. Recognised the fix immediately from the error message itself rather than needing it explained.

**Next up:**
Day 2 - build the data fetch script, including a genuinely new concept: cursor-based pagination (nextPageToken), since this API works differently from the World Bank's simple single-request pull.

---

## Day 2 - [Title]
**Date:**

**What I did:**


**Why I made that choice:**


**What I learned:**


**What confused me / what I'd do differently:**


**Next up:**