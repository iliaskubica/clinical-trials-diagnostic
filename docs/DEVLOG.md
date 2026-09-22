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

**Next up:**

Day 6 - write the first real SQL JOIN between the trials and locations tables, then start using the relational structure to answer an actual question about the clinical trial data.

---