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

## Day 2 - Pagination and Nested Data Extraction
**Date:** 16 September 2026

**What I did:**
Built the data fetch script for the second project - used a while loop with cursor-based pagination (nextPageToken) to pull real oncology trial data from ClinicalTrials.gov, a genuinely new pattern compared to the single-request pull in the first project. Initially scoped too broadly ("cancer", all time) and had to narrow to breast cancer trials completed since 2019 after watching the count climb past 6,000. Wrote extraction code to pull specific fields out of the deeply nested API response into a clean 10-column table, and saved the raw data to a local JSON file so future runs don't need to re-fetch from the API every time.

**Why I made that choice:**
Chose to narrow the scope live, mid-session, once the trial count made it clear "cancer" broadly was too large to be a manageable, finishable dataset - same scope-creep risk flagged in the roadmap on Day 1, caught in practice rather than just in planning. Saved the raw data locally because re-fetching over 4,000 trials across 42 pages every single run would be slow and unnecessarily repetitive load on a public API.

**What I learned:**
The difference between a for loop (fixed number of repeats) and a while loop (repeats until a condition becomes false) - pagination is a natural while loop use case since the number of pages isn't known in advance. How to safely navigate deeply nested dictionaries using chained .get() calls with defaults, so missing fields don't crash the script. Confirmed the ethics decision from the roadmap in practice - saw real investigator names in the raw data (contactsLocationsModule) and deliberately excluded that field from extraction.

**What confused me / what I'd do differently:**
Wasn't immediately sure where the pagination loop actually ended in the code, since indentation is the only visual signal of where a block stops - needed it pointed out explicitly with the surrounding code shown. Also hit a real Git limit: the raw trial data saved as JSON was 139MB, over GitHub's 100MB file size cap, and the push was rejected. Fixed it properly rather than just deleting the file - added a .gitignore rule to exclude data/raw/*.json going forward, untracked the file with git rm --cached (keeping it locally, just not pushed), and amended the commit since it hadn't been shared to GitHub yet. Good real lesson: large generated data files generally shouldn't be committed to Git at all, similar to why venv/ is already excluded.

**Next up:**
Day 3 - review the extracted data properly, check for missing/messy values, and start designing how this splits into multiple related tables (trials, sponsors, locations) for real SQL joins.

---

## Day 3 - Trial Status Breakdown
**Date:** [today's date]

**What I did:**
Had an assessment today and was low on energy, but added one small, real piece of code: a status breakdown using .value_counts() on the trials table. Found 3,511 completed trials vs 626 terminated, roughly an 85/15 split.

**Why I made that choice:**
Wanted to keep making genuine progress even on a low-energy day, rather than a placeholder entry or skipping entirely - one small real result is worth more than a token log with nothing behind it.

**What I learned:**
.value_counts() counts how many times each unique value appears in a column - a quick, useful way to get an overview of a categorical column before deeper analysis. This completed/terminated split is a real baseline worth remembering for later - useful for spotting which sponsors have a disproportionately high termination rate compared to it.

**What confused me / what I'd do differently:**


**Next up:**
Day 4 - review the extracted trial data more fully for gaps/messiness, start designing the relational table structure (trials, sponsors, locations) for real SQL joins.

---

## Day 4 - Building Relational Structure
**Date:** 19 September 2026

**What I did:**
Checked for missing values across the trials table and found two genuinely different kinds of gaps in the phase column - "NA" (1,503 trials, meaning phase genuinely doesn't apply, e.g. behavioral studies) versus real NaN (911 trials, genuinely incomplete data). Kept both as distinct categories rather than treating them the same. Built a second table, locations_df, using a nested loop to extract every location per trial rather than just the first one - resulting in 53,031 trial-location rows from 4,143 trials, confirming many trials run across multiple countries.

**Why I made that choice:**
Conflating "not applicable" with "genuinely missing" would have been a real analytical mistake - they mean different things and should be handled differently in any later analysis. Built the locations table specifically to create genuine one-to-many relational structure (one trial, many locations), which is exactly what's needed to write real SQL joins rather than working with a single flat table like the first project.

**What I learned:**
How a nested loop works - a for loop inside another for loop, where the inner loop runs completely through its own list for every single pass of the outer loop. Caught a real indentation bug myself before running the code (a JSON-saving block that was mismatched between inside and outside the while loop), rather than needing it flagged externally first.

**What confused me / what I'd do differently:**


**Next up:**
Day 5 - load both tables into a SQL database and write the first real join between trials and locations.

---

## Day 5 - Loading the Data into SQL

**Date:** 22 September 2026

**What I did:**

Loaded both the trials and locations tables into a SQLite database using Python's sqlite3 library and pandas .to_sql() method. Added sqlite3 to the standard-library imports alongside json and time, then connected to a new trials.db file and wrote trials_df and locations_df as two separate SQL tables. Re-ran the full extraction successfully, with the final dataset containing 4,148 trials and 53,043 trial-location rows. The existing status breakdown also updated slightly to 3,521 completed vs 627 terminated trials.

**Why I made that choice:**

The whole point of building the locations table on Day 4 was to create a genuine relationship between the data rather than keeping everything as one flat dataframe. Loading both tables into the same SQLite database means the trial-level data and location-level data can now be queried together using SQL, which is the actual purpose of creating the relational structure in the first place.

**What I learned:**

How sqlite3 connects Python to a local SQLite database, and how .to_sql() takes a pandas dataframe and creates a SQL table from it. Also learned a small but useful Python convention around imports - standard-library modules like json, sqlite3 and time are grouped separately from third-party packages like pandas and requests. More importantly, this was the first time the project moved from manipulating data in Python to actually storing related tables in a SQL database.

**What confused me / what I'd do differently:**

The actual sqlite3 connection and .to_sql() code was mostly a new pattern, so I needed the individual parts explained rather than immediately understanding what was happening. The distinction between the pandas dataframes and the SQL tables is also something I'm still getting used to - they contain the same underlying data, but now exist in different stages of the workflow. I also hadn't written the JOIN yet, so the next step is to actually use the relationship between the two tables rather than just creating it.

## Day 6 - First Real SQL Joins
**Date:** 24 September 2026

**What I did:**
Wrote the first two real SQL JOINs of the project, connecting the trials and locations tables via nct_id. The first counted trials per country - the US dominates by a wide margin (28,230 trial-location entries vs Spain's 2,801, the next highest). The second calculated termination rate by country using conditional aggregation (CASE WHEN, SUM, HAVING), filtered to countries with 50+ trials to keep the rate meaningful. Australia stood out with the highest termination rate (24.1%) among countries with substantial trial volume, notably higher than the UK (13.2%) or Canada (13.8%).

**Why I made that choice:**
This is the entire reason the second project exists - moving from a flat, single-table dataset (project one) to genuinely relational data that requires real joins to answer meaningful questions. Filtered to countries with a minimum trial count using HAVING specifically to avoid a small-sample country showing a misleadingly extreme rate (e.g. 1 trial that terminated showing 100%).

**What I learned:**
The actual JOIN syntax - matching rows across two tables on a shared column (nct_id) rather than treating them as separate. CASE WHEN is SQL's version of if/else, letting you turn a category into a countable 1 or 0 inside an aggregation. HAVING filters groups after aggregation, which is different from WHERE, which filters individual rows before grouping - a genuinely important distinction I hadn't needed before.

**What confused me / what I'd do differently:**


**Next up:**
Day 7 - explore the Australia termination-rate finding further, and start looking at sponsor-level patterns (e.g. which sponsors have the highest completion vs termination rates) using window functions.

**Correction (Day 17):** the country figures above came from site-weighted counts, which were fixed on Day 16. Corrected figures: the US has 2,017 distinct trials; Ireland no longer ranks in the top 10 for trial duration (Hungary leads); Australia still has the highest termination rate (26.8%) but is not clearly different from the US.

---

## Day 7 - Sponsor-Level Trial Analysis

**Date:** 25 September 2026

**What I did:**

Added a small sponsor-level analysis using SQL to group trials by sponsor, count total trials, count terminated trials, and calculate a termination rate. Filtered to sponsors with at least 10 trials and returned the top 10 by trial volume. The query was run through pandas using read_sql(), with the final result showing sponsor-level trial volume alongside termination rates - for example, Novartis Pharmaceuticals had 75 trials with a 21.3% termination rate, while Memorial Sloan Kettering Cancer Center had 66 trials with a 3.0% termination rate.

**Why I made that choice:**

Wanted to make a small amount of genuine progress rather than forcing a large new feature just to get another green square. Sponsor-level performance is also directly relevant to the eventual diagnostic because it moves beyond simple overall counts into comparing trial outcomes across organisations. Kept the minimum at 10 trials so the rates aren't dominated by sponsors with only one or two trials.

**What I learned:**

How SQL can combine aggregation with conditional logic - COUNT(*) gives total trials, while SUM(CASE WHEN ... THEN 1 ELSE 0 END) can count only the trials matching a specific condition such as TERMINATED. Also learned that not every useful query needs a JOIN - this analysis only uses sponsor and status, which already exist in the trials table, so adding a JOIN would have been unnecessary. Used pandas read_sql() to bring the SQL result back into a dataframe and then calculated the percentage termination rate.

**What confused me / what I'd do differently:**

The biggest thing to understand was the distinction between a query that genuinely needs a JOIN and one that doesn't. Because the project is specifically designed around relational SQL, there is a temptation to use the second table just because it exists, but that would make the query more complicated without adding anything useful. The sponsor results also showed why rates need to be interpreted alongside trial volume - a percentage on a small number of trials can be much less informative than one based on dozens of trials.

**Next up:**

Continue building the diagnostic with another targeted SQL analysis, ideally using the relational structure to answer a question that genuinely requires joining the trials and locations tables.

## Day 8 - Date Arithmetic and Window Functions
**Date:** 27 September 2026

**What I did:**
Added two genuinely new SQL patterns. First, calculated average trial duration by country using date arithmetic (julianday() to convert dates into numbers so they can be subtracted) - Ireland had the longest average duration among high-volume countries at over 3,300 days (roughly 9 years), followed by South Africa and the US. Second, wrote the project's first window function - RANK() OVER (PARTITION BY sponsor_class ORDER BY trial_count DESC) - ranking sponsors by trial volume within their own category (industry, NIH, academic/other, network) rather than one global ranking.

**Why I made that choice:**
Date arithmetic and window functions were both explicitly named as goals in the original Day 1 roadmap for this project - the whole reason this project uses relational, multi-table data rather than a flat file like the first project. A window function specifically lets you rank or compare rows without collapsing them into a single summary row per group, which a plain GROUP BY can't do.

**What I learned:**
julianday() converts a date into a single number, making subtraction between two dates possible. PARTITION BY splits data into separate groups for ranking purposes - similar in spirit to GROUP BY, but instead of collapsing rows into one summary per group, every original row is kept, just with a rank added. Also observed RANK() correctly handling ties - two sponsors tied at rank 3 both received rank 3, with the next sponsor skipping to rank 5 rather than getting rank 4, which is standard, correct ranking behaviour rather than a bug.

**What confused me / what I'd do differently:**


**Next up:**
Day 9 - use the ranking to filter down to just the top 3 sponsors per class (a common window-function follow-up pattern), then start planning the Power BI dashboard for this project.

**Correction (Day 17):** the country figures above came from site-weighted counts, which were fixed on Day 16. Corrected figures: the US has 2,017 distinct trials; Ireland no longer ranks in the top 10 for trial duration (Hungary leads); Australia still has the highest termination rate (26.8%) but is not clearly different from the US.
---

## Day 9 - Subqueries and Filtering Window Functions
**Date:** 29 September 2026

**What I did:**
Learned and used subqueries to filter the results of yesterday's window function - wrapped the sponsor ranking query inside another query so WHERE rank_in_class <= 3 could actually be applied, since window function results can't be filtered directly in the same query they're calculated in. Result correctly kept both tied sponsors at rank 3 (AstraZeneca and Hoffmann-La Roche), rather than arbitrarily cutting one.

**Why I made that choice:**
This is a natural, common follow-up to yesterday's ranking - having a rank column is only useful if you can then filter on it, and a subquery is the standard way to do that in SQL.

**What I learned:**
A subquery is a query used as input to another query - SQL runs the inner one first and treats its result like a temporary table for the outer query to filter or work with further. This exists specifically because WHERE normally runs before window functions are calculated, so you can't filter on a window function's output in the same step it's created.

**What confused me / what I'd do differently:**


**Next up:**
Day 10 - start planning and building the Power BI dashboard for this project: trial volume by country, termination rate comparison, and sponsor ranking visuals.

---

## Day 10 - Country Summary Export
**Date:** 30 September 2026

**What I did:**
Exported the country-level termination rate data (result2) to a clean CSV for Power BI. Hit the same "empty commit" issue as before - the first run happened before the code was actually saved, so the commit showed 0 real changes. Confirmed the fix by checking the terminal output directly for the "Saved country summary..." confirmation line before trusting the commit.

**Why I made that choice:**
Starting the dashboard at the country level first, then narrowing to sponsors next, rather than building everything at once - same macro-to-micro approach used in the first project's dashboard planning.

**What I learned:**
Reinforced a habit that's now paying off - checking the actual terminal output for a specific expected line, rather than assuming a run worked just because it didn't error, catches silent problems like an unsaved file before they get pushed.

**What confused me / what I'd do differently:**


**Next up:**
Day 11 - import country_trial_summary.csv into Power BI and build the first chart for this project's dashboard.

---

## Day 11 - First Chart and the US Outlier Problem
**Date:** 2 October 2026

**What I did:**
Imported country_trial_summary.csv into Power BI and built the first bar chart (total trials by country). The US dwarfed every other country, making the chart unreadable. Filtered it out using an "is not" condition rather than manually deselecting it from a list, since a condition-based filter automatically applies to future data, while a manual selection would silently miss new countries added later.

**Why I made that choice:**
Log scale, which worked well for the scatter plot in the first project, isn't appropriate for a bar chart, since bar length is meant to be read literally and a log scale on bars risks misleading a viewer who doesn't check the axis. Decided the standard, honest approach is to separate the outlier into its own callout rather than hide or distort it.

**What I learned:**
The difference between a static filter (manually selecting which values to include, which can silently miss new data later) and a condition-based filter (a rule like "is not X", which automatically applies to any future data). Good general practice for any dashboard that gets refreshed over time, even if less critical for a one-off snapshot like this project.

**What confused me / what I'd do differently:**


**Next up:**
Day 12 - add a Card visual showing the US total separately, then continue building out the country-level chart.

---

## Day 12 - US Callout Card
**Date:** 5 October 2026

**What I did:**
Built a Card visual showing the US total trial count (28K) separately from the main bar chart, using a visual-level filter set to "Is" United States. This keeps the extreme outlier visible without letting it crush the readability of the comparison chart for the remaining countries.

**Why I made that choice:**
Following on from last session's plan - the standard, honest way to handle one value massively dwarfing everything else is to show it separately rather than hide or distort it with a log scale that isn't appropriate for bar charts.

**What I learned:**
Power BI automatically abbreviates large numbers on Card visuals (28,276 shown as "28K") by default - a Display units setting can switch this to the exact number if needed, but the abbreviation is standard, readable default behaviour, not an error.

**What confused me / what I'd do differently:**


**Next up:**
Day 13 - add a text label explaining the US card, then continue building out the dashboard with the sponsor-level data.

**Correction (Day 17):** the country figures above came from site-weighted counts, which were fixed on Day 16. Corrected figures: the US has 2,017 distinct trials; Ireland no longer ranks in the top 10 for trial duration (Hungary leads); Australia still has the highest termination rate (26.8%) but is not clearly different from the US.

---

## Day 13 - Code Cleanup
**Date:** 7 October 2026

**What I did:**
Went back through fetch_trials.py and cleaned up variable and column naming for clarity, reorganizing the tables to be more readable rather than adding new functionality.

**Why I made that choice:**
Clear, consistent naming matters for anyone else (or future me) reading the code - this project has grown quite a bit script-by-script, so it was worth a pass to tidy things up before adding more analysis on top.

**What I learned:**


**What confused me / what I'd do differently:**


**Next up:**
Day 14 - add a text label explaining the US callout card, then continue building out the dashboard with the sponsor-level data.

---

## Day 14 - Enrollment by Phase
**Date:** 8 October 2026

**What I did:**
Light session. Added a pandas groupby to calculate average trial enrollment by phase, the pandas equivalent of a SQL GROUP BY.

**Why I made that choice:**
Wanted to keep momentum on a short-on-time day with one small, real piece of analysis rather than skipping.

**What I learned:**
.groupby() splits a table into groups by a column and lets you summarise each group, mirroring SQL GROUP BY but done in pandas.

**What confused me / what I'd do differently:**


**Next up:**
Day 15 - add a text label for the US card, then build the sponsor-level dashboard visuals.

---

## Day 15 - README Update
**Date:** 16 October 2026

**What I did:**
Light session. Updated the project README so the Status section lists what is actually built so far (data pipeline, relational tables, SQL techniques, country-level export) and what is still in progress (the Power BI dashboard).

**Why I made that choice:**
The README had fallen behind the real state of the project. A recruiter reading it should see the SQL work immediately, rather than having to dig through the dev diary to find it.

**What I learned:**
Documentation drifts out of date quickly when the work moves faster than the write-up, and a short checkpoint like this stops that happening.

**What confused me / what I'd do differently:**


**Next up:**
Day 16 - add a text label explaining the US callout card, then build the sponsor-level dashboard visuals.

---

## Day 16 - Fixing an Aggregation Error
**Date:** 17 October 2026

**What I did:**
On review, found that my country-level counts were wrong. COUNT(*) on the joined trials and locations tables counts trial-site rows, not trials, so a trial running at many sites was counted many times. This inflated the US to 28K "trials" in a dataset of only about 4,160, and made the termination rates site-weighted rather than trial-weighted. Rewrote three queries (trials per country, termination rate by country, and average duration by country) so each trial counts once per country, using COUNT(DISTINCT ...) and a subquery. Tested the new queries on a small dummy database first, then reran the full script and checked the outputs against the dataset total.

**Why I made that choice:**
A number that can't be true (more trials for one country than exist in the whole dataset) means the grain of the query is wrong. Better to fix it now than publish a dashboard built on it.

**What I learned:**
When you join a one-to-many relationship, COUNT(*) counts rows in the joined result, not entities in either table. DISTINCT counts each entity once. Sanity-checking an output against the size of the dataset catches this kind of error quickly, and testing a query on tiny dummy data confirms the logic before running it on the real thing.

**What confused me / what I'd do differently:**
The earlier Day 6 and Day 8 findings and the Day 12 US callout card used the inflated figures, so they need revisiting. The termination rate query also ranks countries by number of terminated trials rather than by rate, so the earlier claim that Australia had the highest rate was only true among the ten countries with the most terminations. Next time, sanity-check any count against the dataset total as soon as I write a join.

**Next up:**
Day 17 - refresh the Power BI data with the corrected counts, reassess whether the US still needs its own card, and decide whether to rank countries by termination rate instead of terminated count.

---

## Day 17 - Re-ranking Countries by Termination Rate
**Date:** 18 October 2026

**What I did:**
Re-ran the full pipeline after the aggregation fix and checked the output against the dataset total. The US dropped from about 28,000 site rows to 2,017 distinct trials, in a dataset of 4,201 trials, which is plausible (about 48% of trials have at least one US site). Changed the country termination query to rank by termination rate and removed the LIMIT, so the export now covers all 32 countries with 50+ trials.

**Why I made that choice:**
The old query ranked by number of terminations, so a country with a high rate but fewer trials could be missing from the results, and my earlier Australia claim was not actually proven.

**What I learned:**
ORDER BY decides which rows survive a LIMIT, so the ranking metric changes the findings, not just the order. Australia still has the highest rate (26.8%, 40 of 149 trials), so the finding survived the fix, but with that sample size the margin of error is roughly 7 percentage points, so it is not clearly different from the US (22.7%), Spain or Switzerland. The clearer pattern is at the low end: Turkey (2.9%) and Egypt (0%) are well below everyone else. Average duration by country also changed: Ireland, previously the longest at 3,300+ days, dropped out of the top 10, and Hungary now leads at about 2,440 days, so the earlier Ireland result was an artefact of site-weighting.

**What confused me / what I'd do differently:**
My Day 6, Day 8 and Day 12 entries quote figures from the faulty queries. I left them as written and added correction notes rather than rewriting history. Country rates may also reflect trial mix (sponsor type, phase) rather than anything about the country itself, which I haven't tested yet. A multinational trial also counts in every country where it has a site, so countries are not independent.

**Next up:**
Day 18 - test whether Turkey and Egypt's low termination rates are explained by trial mix (sponsor class and phase), then finish the country-level dashboard visuals.

---

## Day 18 - Updating the Country Dashboard
**Date:** 19 October 2026


**What I did:**

Refreshed the Power BI data using the corrected country summary export, then changed the existing country chart from total trial count to termination rate. The US now shows roughly 2,000 distinct trials rather than the previous 28K, reflecting the aggregation fix from Day 16. The dashboard is now using the corrected figures and comparing countries by termination rate rather than raw trial volume.


**Why I made that choice:**

The dashboard was still using the old data, so the corrected SQL results needed to be carried through into Power BI before the visuals could be trusted. Switching the country chart to termination rate also makes the comparison more useful: raw trial volume mostly shows where trials are concentrated, whereas termination rate helps identify differences in trial outcomes.


**What I learned:**

Refreshing Power BI updates the imported data from the source file, so changes made in the Python pipeline and SQL analysis do not automatically appear in an existing dashboard. Also reinforced that the metric used in a chart determines the question it answers - ranking countries by total trials and ranking them by termination rate can tell very different stories.


**What confused me / what I'd do differently:**

The original dashboard carried forward the same aggregation error as the SQL queries, which meant the visuals looked plausible but were based on the wrong counts. This is a reminder that fixing the analysis is only part of the job; the exported data and dashboard also need to be refreshed and checked before the results are presented.


**Next up:**

Day 19 - test whether Turkey and Egypt's low termination rates are explained by trial mix (sponsor class and phase), then continue finishing the country-level dashboard visuals.



---



## Day 19 - Testing Whether Trial Mix Explains Turkey and Egypt
**Date:** 20 October 2026

**What I did:**
Tested whether Turkey (2.9%, 7 of 243 trials) and Egypt (0%, 0 of 135) have low termination rates because of the kind of trials run there. Looked at their phase mix against the whole dataset, and at their sponsor class breakdown, using DISTINCT in a subquery so each trial counts once per country.

**Why I made that choice:**
A country-level rate can reflect the mix of trials rather than anything about the country. If most trials there are non-drug academic studies, a low rate may just reflect that.

**What I learned:**
Both countries have an unusual phase mix: 55% (Turkey) and 47% (Egypt) of trials are "NA" non-drug trials versus 36% overall, and they run almost no Phase 1 trials (0.4% and 3% versus 19% overall). But the rates are far lower than chance would produce: at the overall rate of about 15%, I'd expect around 20 terminations in Egypt and 37 in Turkey, and observed 0 and 7. I have not yet computed termination rate by phase, so I can't say how much the mix explains. I'm not claiming a cause. It could be mix, reporting differences, or both, and this data can't separate them.

**What confused me / what I'd do differently:**
My terminal output truncated the key columns in two tables, so I couldn't read the sponsor class results. Fix: set pandas display options at the top of the script. Also, the trial count moved from 4,201 to 4,208 between runs because each run re-pulls the live ClinicalTrials.gov registry, so figures shift slightly. A dated snapshot would make results reproducible.

**Next up:**
Day 20 - add termination rate by phase to finish the mix test, then finish the country-level dashboard visuals (title, caption, remove the stale US card).

---

## Day 20 - Does Trial Mix Explain the Low Rates?
**Date:** 23 October 2026

**What I did:**
Finished the trial mix test for Turkey (7 terminated of 243) and Egypt (0 of 135). Calculated termination rate by phase across the whole dataset, then worked out how many terminations each country would be expected to have if it matched the overall rate within each phase. Compared expected against observed. Also set pandas display options so wide tables no longer truncate, and tidied the country chart in Power BI (title, axis label, caption, removed the stale US card).

**Why I made that choice:**
Last session showed both countries run an unusual mix of trials, but that alone doesn't say whether the mix explains the low rates. Expected-versus-observed answers that directly.

**What I learned:**
This is a simple version of indirect standardisation: applying overall rates for each category to a group's own mix to get an expected count. Result: Egypt had 17.4 expected terminations versus 0 observed, while Turkey had 25 expected versus 7 observed. This suggests that phase mix alone does not explain the low termination rates. The sponsor class tables provide another comparison, showing whether differences in sponsor composition might help explain the gap. I’m not claiming a cause: reporting practices or other differences could also be involved, and this data cannot distinguish between them.

**What confused me / what I'd do differently:**
Figures shift slightly between runs because each run re-pulls the live registry (4,201 trials one day, 4,208 another), so the numbers here are as of this run. A dated snapshot would make results reproducible. Also, multinational trials count in every country where they have a site, so countries are not independent.

**Next up:**
Day 21 - build the sponsor-level dashboard views, then write the findings briefing for this project.

---

## Day 21 - Data Snapshot and Sponsor Dashboard
**Date:** 25 October 2026

**What I did:**
Fixed a reproducibility problem: every run re-pulled the live registry, so counts drifted between runs and each run took minutes. Added a REFETCH flag so the script loads a saved snapshot by default and only calls the API when I choose. Removed the large raw printout. Exported a sponsor summary (sponsors with 20+ trials, termination rate, sponsor type) and built a sponsor-level bar chart in Power BI with sample size in the tooltip.

**Why I made that choice:**
Results that change between runs can't be written up reliably, and I need stable numbers before writing the findings briefing. A 20-trial minimum keeps the sponsor rates from resting on tiny samples.

**What I learned:**
An if/else on a flag, plus os.path.exists, lets a script choose between fetching and loading. Freezing the data is basic reproducibility practice. Indentation decides what belongs inside the if block, so the whole fetch loop had to move one level in. The sponsor chart shows a large spread. I'm not explaining why, because the data can't say.

**What confused me / what I'd do differently:**
Sponsor rates rest on 20 to 75 trials each, so individual rates carry real uncertainty, and trials are counted under their lead sponsor only.

**Next up:**
Day 22 - write the findings briefing for this project, pulling together the country and sponsor results.

---

## Day 22 - Completing the Dashboard
**Date:** 27 October 2026

**What I did:**
Added the phase summary and country duration analysis exports to the Python script. Finished building the four-chart Power BI dashboard, covering termination rates by country, lead sponsor and trial phase, plus average trial duration against termination rate by country.

**Why I made that choice:**
I wanted to expand the dashboard beyond country and sponsor comparisons to investigate whether trial phase and duration reveal further patterns in termination rates.

**What I learned:**
Adding different views helps explore the data from multiple angles, but observed relationships do not establish causation.

**What confused me / what I'd do differently:**
The dashboard is built, but I still need to capture a screenshot and add it to the repository README to make the results visible on the project front page.

**Next up:**
Day 23 - Capture the dashboard screenshot, update the README, and prepare the one-page findings briefing.

---

## Day 23 - Dashboard Refinements
**Date:** 28 October 2026

**What I did:**
Made several changes to the four-chart Power BI dashboard, adjusting the layout and improving how the results are presented. The dashboard still needs a final round of fixes, including changing the phase chart from a pie chart to a column chart, improving labels and adding captions.


**Why I made that choice:**
I wanted the dashboard to communicate the findings clearly and avoid misleading visualisations before publishing it to GitHub.


**What I learned:**
The choice of chart matters as much as the underlying data. Termination rates should be compared directly rather than shown as slices of a whole.


**What confused me / what I'd do differently:**
I expected to finish the dashboard today, but making changes revealed a few more presentation issues. Rather than upload an unfinished version, I'll finish the remaining adjustments first.


**Next up:**
Day 24 - Finalise the dashboard, capture a screenshot, update the README and push the finished project to GitHub.

## Day 24 - Dashboard Polish and Shipping
**Date:** 30 October 2026

**What I did:**
Finished the four-chart dashboard and put it in the repo. Replaced the phase pie chart with a column chart, because termination rates are not parts of a whole and a pie implied they were. Fixed the scatter (title, axes, clipped point), thickened the sponsor bars and added data labels, and wrote a caption for each chart. Saved the .pbix and a screenshot into the dashboard folder and updated the README.

**Why I made that choice:**
A pie chart on rates is a standard chart-choice mistake that a data person would notice immediately. The front page of the repo is what a recruiter sees first, so the dashboard needed to be readable at a glance, with each chart explaining itself.

**What I learned:**
Chart type has to match the data. Rates compare across categories, so bars or columns fit, while pies suit shares that sum to a whole. Also, the two most important sponsor values were hidden behind a scrollbar, so what appears in a screenshot has to be checked, not assumed.

**What confused me / what I'd do differently:**


**Next up:**
Day 24 - write the one-page findings briefing, using the country, sponsor and trial mix results.

---

## Day 25 - [Title]
**Date:**

**What I did:**


**Why I made that choice:**


**What I learned:**


**What confused me / what I'd do differently:**


**Next up:**