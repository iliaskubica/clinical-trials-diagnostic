import json
import os
import sqlite3
import time

import pandas as pd
import requests

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "COMPLETED,TERMINATED",
    "filter.advanced": "AREA[CompletionDate]RANGE[2019-01-01,MAX]",
    "pageSize": 100,
}

RAW_PATH = "data/raw/trials_raw.json"
REFETCH = False  # set to True only when you want fresh data from the API

if REFETCH or not os.path.exists(RAW_PATH):
    all_trials = []
    page_count = 0

    while True:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        studies = data.get("studies", [])
        all_trials.extend(studies)

        page_count += 1
        print(f"Fetched page {page_count}, total trials so far: {len(all_trials)}")

        next_token = data.get("nextPageToken")
        if not next_token:
            break

        params["pageToken"] = next_token
        time.sleep(0.5)

    with open(RAW_PATH, "w") as f:
        json.dump(all_trials, f)
    print(f"Fetched fresh data and saved it to {RAW_PATH}")
else:
    with open(RAW_PATH) as f:
        all_trials = json.load(f)
    print(f"Loaded {len(all_trials)} trials from saved snapshot {RAW_PATH}")

print(f"\nTotal trials: {len(all_trials)}")

records = []

for trial in all_trials:
    protocol = trial.get("protocolSection", {})
    
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
    design = protocol.get("designModule", {})
    locations = protocol.get("contactsLocationsModule", {}).get("locations", [])
    
    first_country = locations[0].get("country") if locations else None
    
    records.append({
        "nct_id": identification.get("nctId"),
        "title": identification.get("briefTitle"),
        "status": status.get("overallStatus"),
        "start_date": status.get("startDateStruct", {}).get("date"),
        "completion_date": status.get("completionDateStruct", {}).get("date"),
        "sponsor_name": sponsor.get("name"),
        "sponsor_class": sponsor.get("class"),
        "phase": design.get("phases", [None])[0],
        "enrollment_count": design.get("enrollmentInfo", {}).get("count"),
        "primary_country": first_country,
    })

location_records = []

for trial in all_trials:
    nct_id = trial.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
    locations = trial.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations", [])
    
    for location in locations:
        location_records.append({
            "nct_id": nct_id,
            "country": location.get("country"),
        })

locations_df = pd.DataFrame(location_records)
print(f"\nExtracted {len(locations_df)} trial-location rows from {len(all_trials)} trials")
print(locations_df.head(10))

trials_df = pd.DataFrame(records)
print(f"\nExtracted {len(trials_df)} trials into a clean table")
print(trials_df.head())

print("\nTrial status breakdown:")
print(trials_df["status"].value_counts())

print("\nAverage enrollment by phase:")
print(trials_df.groupby("phase")["enrollment_count"].mean().round(0))

print("\nMissing values per column:")
print(trials_df.isnull().sum())

print("\nUnique phase values:")
print(trials_df["phase"].value_counts(dropna=False))

conn = sqlite3.connect("data/processed/trials.db")

trials_df.to_sql("trials", conn, if_exists="replace", index=False)
locations_df.to_sql("locations", conn, if_exists="replace", index=False)

print("\nBoth tables loaded into SQLite database: data/processed/trials.db")

conn = sqlite3.connect("data/processed/trials.db")

query = """
SELECT locations.country, COUNT(DISTINCT locations.nct_id) AS trial_count
FROM locations
JOIN trials ON locations.nct_id = trials.nct_id
GROUP BY locations.country
ORDER BY trial_count DESC
LIMIT 10
"""

result = pd.read_sql(query, conn)
print("\nTop 10 countries by number of trials:")
print(result)

query2 = """
SELECT 
    locations.country,
    COUNT(DISTINCT trials.nct_id) AS total_trials,
    COUNT(DISTINCT CASE WHEN trials.status = 'TERMINATED' THEN trials.nct_id END) AS terminated_trials
FROM locations
JOIN trials ON locations.nct_id = trials.nct_id
GROUP BY locations.country
HAVING total_trials >= 50
ORDER BY 1.0 * terminated_trials / total_trials DESC
"""

result2 = pd.read_sql(query2, conn)
result2["termination_rate"] = (result2["terminated_trials"] / result2["total_trials"] * 100).round(1)
print("\nTermination rate by country (countries with 50+ trials):")
print(result2)

result2.to_csv("data/processed/country_trial_summary.csv", index=False)
print("\nSaved country summary for Power BI: data/processed/country_trial_summary.csv")

query3 = """
SELECT 
    sponsor_name,
    COUNT(*) AS total_trials,
    SUM(CASE WHEN status = 'TERMINATED' THEN 1 ELSE 0 END) AS terminated_trials
FROM trials
GROUP BY sponsor_name
HAVING total_trials >= 10
ORDER BY total_trials DESC
LIMIT 10
"""

result3 = pd.read_sql(query3, conn)
result3["termination_rate"] = (result3["terminated_trials"] / result3["total_trials"] * 100).round(1)
print("\nTop 10 sponsors by trial volume, with termination rate:")
print(result3)

query4 = """
SELECT country,
       AVG(duration) AS avg_duration_days,
       COUNT(*) AS trial_count
FROM (
    SELECT DISTINCT locations.country, trials.nct_id,
           julianday(trials.completion_date) - julianday(trials.start_date) AS duration
    FROM locations
    JOIN trials ON locations.nct_id = trials.nct_id
    WHERE trials.completion_date IS NOT NULL AND trials.start_date IS NOT NULL
)
GROUP BY country
HAVING trial_count >= 50
ORDER BY avg_duration_days DESC
LIMIT 10
"""

result4 = pd.read_sql(query4, conn)
print("\nAverage trial duration by country (50+ trials):")
print(result4)

query5 = """
SELECT sponsor_name, sponsor_class, COUNT(*) AS trial_count,
       RANK() OVER (PARTITION BY sponsor_class ORDER BY COUNT(*) DESC) AS rank_in_class
FROM trials
GROUP BY sponsor_name, sponsor_class
HAVING trial_count >= 10
ORDER BY sponsor_class, rank_in_class
LIMIT 20
"""

result5 = pd.read_sql(query5, conn)
print("\nTop sponsors ranked within their sponsor class:")
print(result5)

query6 = """
SELECT *
FROM (
    SELECT sponsor_name, sponsor_class, COUNT(*) AS trial_count,
           RANK() OVER (PARTITION BY sponsor_class ORDER BY COUNT(*) DESC) AS rank_in_class
    FROM trials
    GROUP BY sponsor_name, sponsor_class
    HAVING trial_count >= 10
) AS ranked_sponsors
WHERE rank_in_class <= 3
ORDER BY sponsor_class, rank_in_class
"""

result6 = pd.read_sql(query6, conn)
print("\nTop 3 sponsors per class:")
print(result6)

# Trial mix: does sponsor class or phase explain Turkey and Egypt's low termination rates?
query7 = """
SELECT sponsor_class,
       COUNT(*) AS total_trials,
       SUM(CASE WHEN status = 'TERMINATED' THEN 1 ELSE 0 END) AS terminated_trials
FROM trials
GROUP BY sponsor_class
ORDER BY total_trials DESC
"""

result7 = pd.read_sql(query7, conn)
result7["termination_rate"] = (result7["terminated_trials"] / result7["total_trials"] * 100).round(1)
result7["share_of_all_trials"] = (result7["total_trials"] / result7["total_trials"].sum() * 100).round(1)
print("\nTermination rate and share of trials by sponsor class (all countries):")
print(result7)

query8 = """
SELECT country, sponsor_class,
       COUNT(*) AS total_trials,
       SUM(CASE WHEN status = 'TERMINATED' THEN 1 ELSE 0 END) AS terminated_trials
FROM (
    SELECT DISTINCT locations.country, trials.nct_id, trials.sponsor_class, trials.status
    FROM locations
    JOIN trials ON locations.nct_id = trials.nct_id
    WHERE locations.country IN ('Turkey (Türkiye)', 'Egypt')
)
GROUP BY country, sponsor_class
ORDER BY country, total_trials DESC
"""

result8 = pd.read_sql(query8, conn)
print("\nSponsor class mix for Turkey and Egypt:")
print(result8)

query9 = """
SELECT country, COALESCE(phase, 'MISSING') AS phase, COUNT(*) AS total_trials
FROM (
    SELECT DISTINCT locations.country, trials.nct_id, trials.phase
    FROM locations
    JOIN trials ON locations.nct_id = trials.nct_id
    WHERE locations.country IN ('Turkey (Türkiye)', 'Egypt')
)
GROUP BY country, COALESCE(phase, 'MISSING')
ORDER BY country, total_trials DESC
"""

result9 = pd.read_sql(query9, conn)
print("\nPhase mix for Turkey and Egypt:")
print(result9)

query10 = """
SELECT COALESCE(phase, 'MISSING') AS phase,
       COUNT(*) AS total_trials,
       SUM(CASE WHEN status = 'TERMINATED' THEN 1 ELSE 0 END) AS terminated_trials
FROM trials
GROUP BY COALESCE(phase, 'MISSING')
ORDER BY total_trials DESC
"""

result10 = pd.read_sql(query10, conn)
result10["termination_rate"] = (result10["terminated_trials"] / result10["total_trials"] * 100).round(1)
print("\nTermination rate by phase (all countries):")
print(result10)

# Expected terminations in Turkey and Egypt if each phase had the overall termination rate for that phase
phase_rates = result10[["phase", "termination_rate"]].copy()
phase_rates["rate"] = phase_rates["termination_rate"] / 100
mix = result9.merge(phase_rates[["phase", "rate"]], on="phase")
mix["expected_terminated"] = mix["total_trials"] * mix["rate"]
expected = mix.groupby("country")["expected_terminated"].sum().round(1)
observed = result2.set_index("country").loc[["Egypt", "Turkey (Türkiye)"], "terminated_trials"]
print("\nExpected vs observed terminations, given each country's phase mix:")
print(pd.DataFrame({"expected_given_phase_mix": expected, "observed": observed}))

query_sponsors = """
SELECT sponsor_name,
       sponsor_class,
       COUNT(*) AS total_trials,
       SUM(CASE WHEN status = 'TERMINATED' THEN 1 ELSE 0 END) AS terminated_trials
FROM trials
GROUP BY sponsor_name, sponsor_class
HAVING total_trials >= 20
ORDER BY total_trials DESC
"""

sponsor_summary = pd.read_sql(query_sponsors, conn)
sponsor_summary["termination_rate"] = (sponsor_summary["terminated_trials"] / sponsor_summary["total_trials"] * 100).round(1)

class_labels = {
    "INDUSTRY": "Industry",
    "OTHER": "Academic / hospital / other",
    "NIH": "NIH",
    "NETWORK": "Research network",
    "OTHER_GOV": "Other government",
    "FED": "Federal",
    "INDIV": "Individual",
    "UNKNOWN": "Unknown",
}
sponsor_summary["sponsor_type"] = sponsor_summary["sponsor_class"].map(class_labels).fillna(sponsor_summary["sponsor_class"])

print("\nSponsor summary (20+ trials):")
print(sponsor_summary)

sponsor_summary.to_csv("data/processed/sponsor_trial_summary.csv", index=False)
print("\nSaved sponsor summary for Power BI: data/processed/sponsor_trial_summary.csv")

# Export 1: termination rate by phase
phase_summary = result10.copy()
phase_labels = {
    "EARLY_PHASE1": "Early Phase 1",
    "PHASE1": "Phase 1",
    "PHASE2": "Phase 2",
    "PHASE3": "Phase 3",
    "PHASE4": "Phase 4",
    "NA": "Not applicable (non-drug)",
    "MISSING": "Phase not reported",
}
phase_summary["phase_label"] = phase_summary["phase"].map(phase_labels).fillna(phase_summary["phase"])
phase_summary.to_csv("data/processed/phase_trial_summary.csv", index=False)
print("\nSaved phase summary: data/processed/phase_trial_summary.csv")

# Export 2: average trial duration against termination rate, by country
query_duration = """
SELECT country, AVG(duration) AS avg_duration_days
FROM (
    SELECT DISTINCT locations.country, trials.nct_id,
           julianday(trials.completion_date) - julianday(trials.start_date) AS duration
    FROM locations
    JOIN trials ON locations.nct_id = trials.nct_id
    WHERE trials.completion_date IS NOT NULL AND trials.start_date IS NOT NULL
)
GROUP BY country
"""
duration_df = pd.read_sql(query_duration, conn)
country_detail = result2.merge(duration_df, on="country")
country_detail["avg_duration_years"] = (country_detail["avg_duration_days"] / 365.25).round(1)
country_detail.to_csv("data/processed/country_duration_vs_termination.csv", index=False)
print("Saved country duration summary: data/processed/country_duration_vs_termination.csv")

duration_corr = country_detail["avg_duration_years"].corr(country_detail["termination_rate"])
print(f"\nCorrelation between average trial duration and termination rate across countries: {duration_corr:.2f}")

conn.close()