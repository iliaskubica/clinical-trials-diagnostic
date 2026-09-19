import requests
import pandas as pd
import time

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "COMPLETED,TERMINATED",
    "filter.advanced": "AREA[CompletionDate]RANGE[2019-01-01,MAX]",
    "pageSize": 100,
}

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

import json
with open("data/raw/trials_raw.json", "w") as f:
    json.dump(all_trials, f)
print("Saved raw trial data to data/raw/trials_raw.json")

print(f"\nTotal trials collected: {len(all_trials)}")
print("\nFirst trial's raw structure (just to see what we're working with):")
print(all_trials[0])

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

print("\nMissing values per column:")
print(trials_df.isnull().sum())

print("\nUnique phase values:")
print(trials_df["phase"].value_counts(dropna=False))