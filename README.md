# Oncology Clinical Trials Diagnostic

A diagnostic analysis of oncology clinical trial performance using real, public data from ClinicalTrials.gov: which sponsors run efficient trials, how duration varies by phase, and where trials most often stall or terminate.

## Project Objective

Using the ClinicalTrials.gov public API, this project identifies patterns in oncology trial performance, sponsor efficiency, phase-level duration, completion vs termination rates, and translates the findings into a consultancy-style diagnostic. Unlike a single flat dataset, this project deliberately works with genuinely relational data (trials, sponsors, conditions, locations), enabling real SQL joins, subqueries, and window functions.

## Structure

clinical-trials-diagnostic/
├── data/
│ ├── raw/ # Original, unmodified source data
│ └── processed/ # Cleaned data ready for analysis
├── sql/ # SQL scripts: schema, queries
├── notebooks/ # Python analysis (exploration, stats, visuals)
├── dashboard/ # Dashboard files (Power BI)
└── docs/ # Findings briefing, methodology notes, dev diary


## Tools

SQL (joins, window functions, subqueries) · Python (pandas, matplotlib) · Power BI

## Data & Ethics Note

Data is sourced from the ClinicalTrials.gov public API (v2). Fields containing real personal contact information for trial investigators (names, emails, phone numbers) are deliberately excluded from every data pull. Only institutional data (sponsor organisation name and class, country-level trial locations) is retained.

## Status

In progress, built iteratively, day by day. See [progress log](docs/progress-log.md) and [dev diary](docs/DEVLOG.md) for daily updates.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full plan: objective, rationale, methodology, and anticipated challenges.

## Author

Ilias Kubica - [LinkedIn](https://linkedin.com/in/iliaskubica) - [GitHub](https://github.com/iliaskubica)