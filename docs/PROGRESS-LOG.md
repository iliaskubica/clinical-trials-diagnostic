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

## Day 7 - Sponsor-level trial analysis

- Added a SQL aggregation to calculate trial volume and termination rate by sponsor
- Filtered to sponsors with at least 10 trials and returned the top 10 sponsors by trial volume
- Used COUNT(), SUM(CASE WHEN), GROUP BY, HAVING and ORDER BY in a single analytical query
- Calculated termination rates in pandas using the SQL result
- Confirmed the analysis did not require a JOIN because sponsor and status are both stored in the trials table

## Day 8 - Date arithmetic and window functions
- Calculated average trial duration by country using julianday() date arithmetic (Ireland longest at 3,300+ days)
- Wrote the project's first window function, ranking sponsors within their class using RANK() OVER (PARTITION BY ...)
- Completed every SQL goal from the original roadmap: joins, conditional aggregation, date arithmetic, window functions

## Day 9 - Subqueries filtering window functions
- Learned subqueries and used one to filter yesterday's sponsor ranking to top 3 per class
- Correctly preserved tied ranks rather than arbitrarily cutting one
- Completed full SQL skill set for this project: joins, conditional aggregation, date arithmetic, window functions, subqueries

## Day 10 - Country summary export
- Exported country-level termination rate data to CSV for Power BI
- Caught and fixed a silent unsaved-file issue before it was pushed

## Day 11 - First chart, handled US outlier
- Built first bar chart (trials by country), filtered out US outlier using a condition-based filter
- Learned static vs condition-based filtering tradeoffs

## Day 12 - US callout card
- Built a Card visual showing the US total separately from the main comparison chart
- Used a visual-level filter to isolate the outlier without distorting the main chart

## Day 13 - Code cleanup
- Renamed and reorganized variables/columns in fetch_trials.py for clarity

## Day 14 - Enrollment by phase
- Added pandas groupby analysis of average enrollment by trial phase

## Day 15 - README update
- Updated the README status section to reflect completed work and current dashboard progress

## Day 16 - Aggregation fix
- Found that country-level counts were weighted by trial sites rather than trials
- Fixed three queries (trials per country, termination rate, average duration) using COUNT(DISTINCT ...) and a subquery
- Tested the fixes on dummy data and checked outputs against the dataset total
- Noted that earlier findings and the Power BI data need refreshing

## Day 17 - Re-ranking by termination rate
- Re-ran the pipeline and verified the corrected counts (US now 2,017 trials of 4,201)
- Ranked all 32 countries with 50+ trials by termination rate
- Australia's finding survived the fix but is statistically weak; Turkey and Egypt are the clear low outliers
- Added correction notes to earlier entries that used the faulty figures

## Day 18 - Updating the Country Dashboard

- Refreshed the Power BI data using the corrected country summary export
- Changed the country chart from total trial count to termination rate
- Confirmed the US count now shows roughly 2,000 distinct trials rather than the previous 28K
- Dashboard now reflects the corrected country-level analysis

## Day 19 - Trial mix test
- Compared the phase mix of Turkey and Egypt against the whole dataset
- Found both run far more non-drug trials and far fewer Phase 1 trials than average
- Showed their termination rates are too low to be chance alone, but left the cause open pending a termination-rate-by-phase check

## Day 20 - Trial mix test finished
- Calculated termination rate by phase across all countries
- Compared expected against observed terminations for Turkey and Egypt using their phase mix (indirect standardisation)
- Concluded the phase mix does not explain their low rates
- Finished the country-level chart in Power BI (title, caption, axis label)

## Day 21 - Data snapshot and sponsor dashboard
- Added a REFETCH flag so the pipeline loads a saved snapshot, making results reproducible
- Exported a sponsor summary (20+ trials) and built the sponsor-level chart in Power BI
- Documented the snapshot approach in the README

## Day 22 - Dashboard Completed
- Added phase summary and country duration analysis exports to the Python script
- Built a four-chart Power BI dashboard covering country, sponsor, phase and duration comparisons

## Day 23 - Dashboard Refinements
- Made several layout and presentation changes to the four-chart Power BI dashboard
- Identified remaining fixes to chart types, labels and captions before publishing

## Day 24 - Dashboard shipped
- Replaced the phase pie chart with a column chart and polished the other three charts
- Added a caption to each chart
- Saved the Power BI file and screenshot into the repo and updated the README