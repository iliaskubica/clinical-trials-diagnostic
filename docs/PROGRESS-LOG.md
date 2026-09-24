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

## Day 3 - Trial status breakdown
- Added a quick status breakdown: 3,511 completed vs 626 terminated trials (~85/15 split)

## Day 4 - Relational structure built
- Distinguished genuine missing data from "not applicable" in the phase column
- Built a second table (locations) using a nested loop - 53,031 trial-location rows from 4,143 trials
- Confirmed real one-to-many relational structure, ready for SQL joins

## Day 5 - SQLite database setup

- Added sqlite3 and connected the project to a local SQLite database
- Loaded both trials and locations dataframes into separate SQL tables using .to_sql()
- Successfully reran the full extraction and loaded 4,148 trials and 53,043 trial-location rows into the database
- Moved the project from Python-only dataframe analysis into a relational SQL database, ready for the first real JOIN

## Day 6 - First real SQL joins
- Wrote two JOINs connecting trials and locations tables
- Found US dominates trial volume by a wide margin (28,230 vs Spain's 2,801)
- Found Australia has the highest termination rate (24.1%) among high-volume countries
- Learned CASE WHEN, SUM for conditional counting, and HAVING for filtering aggregated groups