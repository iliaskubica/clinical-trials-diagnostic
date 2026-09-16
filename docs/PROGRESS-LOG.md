# Progress Log

Daily build log for the Oncology Clinical Trials Diagnostic project.

## Day 1 - Project setup
- Set up repo, local environment, and folder structure
- Researched ClinicalTrials.gov API v2
- Wrote project roadmap

## Day 2 - Pagination and data extraction
- Built a fetch script using while-loop pagination to pull real oncology trial data
- Narrowed scope from broad "cancer" (6,000+ trials) to breast cancer since 2019 (4,133 trials)
- Extracted key fields from deeply nested API responses into a clean 10-column table
- Saved raw data locally to avoid re-fetching from the API on every run
- Fixed a Git large-file issue (139MB JSON exceeded GitHub's 100MB limit) via .gitignore and git rm --cached