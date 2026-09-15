# Project Roadmap: Oncology Clinical Trials Diagnostic

## What I'm doing

Building a diagnostic analysis of oncology clinical trial performance using real, public data from ClinicalTrials.gov. Rather than looking at health system outcomes (my first project), this one looks at the R&D pipeline itself: which sponsors run efficient trials, how trial duration varies by phase, and where trials most often stall, get terminated, or take longer than expected.

Concretely, I'll:
1. Pull real oncology trial data from the ClinicalTrials.gov public API - interventional trials, completed or terminated, from the last several years
2. Load it into a SQL database with a genuine relational structure (trials, sponsors, conditions, locations), since this dataset naturally splits into related tables rather than one flat file
3. Write SQL queries using real joins and window functions - ranking sponsors by completion rate, running totals of trials by year, average duration by phase
4. Analyse the data in Python - trial duration distributions, completion vs termination rates, sponsor-level patterns
5. Build a Power BI dashboard visualising the findings
6. Write a short findings briefing, same consultancy-style format as the first project

## Why I want to do this

**Closing a real skill gap.** My first project used a single flat table, so every SQL query was a simple filter and sort. This project is specifically chosen because the data structure forces genuine joins, subqueries, and window functions, the level of SQL that actually comes up in technical interview screens.

**Proving range beyond health outcomes.** My first project and my CV are entirely health-systems focused. This project stays in a related, genuinely interesting space (life sciences, closer to pharma/R&D than public health), which is directly relevant to life sciences consultancy roles specifically, while proving I can work with a different kind of dataset and a different kind of question.

**Real interest.** I want to move toward consultancy and life sciences roles, and clinical trial performance is a genuine, current, commercially relevant question in that space, not just an exercise.

## How I plan to achieve it

- **Data sourcing:** ClinicalTrials.gov API v2, a free, unauthenticated, well-documented public API. Scoped to oncology, interventional trials, completed or terminated status, to keep the dataset focused and finishable rather than trying to cover all therapeutic areas.
- **Ethics:** the API can return real personal contact information for trial investigators (names, emails, phone numbers) via specific fields. I will deliberately exclude these fields from every pull, keeping only institutional data (sponsor organisation name and class, country-level locations), documented clearly in the README.
- **SQL:** structure the data relationally rather than as one flat table, and deliberately practise joins, window functions (ranking, running totals), and subqueries, since this is the specific skill gap this project exists to close.
- **Python:** pandas for cleaning and reshaping, matplotlib for visuals, similar statistical approach to the first project (distributions, comparisons) but applied to trial-level data rather than country-level data.
- **Dashboard:** Power BI, building on everything learned in the first project rather than relearning the tool from scratch.
- **Process:** same iterative, daily-commit approach as the first project, with the same dev diary and progress log structure.

## How this is applicable beyond clinical trials

The underlying method, real relational data, structured SQL analysis, diagnosing where performance diverges from expectation, applies to any operational dataset with related entities: a sales pipeline (customers, orders, products), a service delivery programme (clients, interventions, outcomes), or a project portfolio (projects, teams, budgets, timelines). Clinical trials data is simply the vehicle for practising joins and window functions on a genuinely real, multi-table dataset relevant to the roles I'm targeting.

## Potential issues I may run into

- **Personal data exposure:** the API can return real contact information for named individuals. Mitigation: explicitly exclude these fields from every request, and state this clearly as a deliberate data-handling decision in the documentation, not just an oversight avoided.
- **Pagination complexity:** this API uses cursor-based pagination (a `nextPageToken`), which is a new pattern compared to the single-request pull in my first project. Mitigation: build and test the pagination loop carefully with a small page size first, before pulling the full dataset.
- **Data volume and scope creep:** the full registry has hundreds of thousands of studies. Mitigation: scope tightly to oncology, interventional, completed/terminated trials from a defined recent date range, and treat anything broader as future work, not a mid-project expansion.
- **Messy/incomplete fields:** real-world registry data will have missing sponsors, unclear phase labels, or incomplete dates. Mitigation: check data completeness explicitly before analysing, the same discipline used in the first project when physician density data was found to be incomplete.
- **Time consistency:** same risk as before, mitigated the same way, daily progress however small, honestly logged.

## Status
Planning complete. Repo, environment, and folder structure set up. Data sourcing begins next session.