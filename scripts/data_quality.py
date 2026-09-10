import pandas as pd
from pathlib import Path

src = Path("data/gsc_data.csv")
out = Path("reports/data_quality.csv")

df = pd.read_csv(src)

for col in ["Clicks", "Impressions", "CTR", "Position"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

issues = []

for _, row in df.iterrows():
    url = str(row.get("URL", "")).strip()
    if not url or url.lower() == "nan":
        continue

    clicks = row.get("Clicks", 0)
    impressions = row.get("Impressions", 0)
    ctr = row.get("CTR", 0)

    if pd.notna(clicks) and pd.notna(impressions) and impressions > 0:
        derived_ctr = clicks / impressions * 100

        if pd.notna(ctr) and ctr == 0 and clicks > 0:
            issues.append({
                "URL": url,
                "Issue": "CTR Data Integrity Issue",
                "Priority": "High",
                "Current Value": f"CTR={ctr}%, Clicks={clicks}, Impressions={impressions}",
                "Recommendation": f"Validate GSC export/tracking. Derived CTR is {derived_ctr:.2f}%."
            })
        elif pd.notna(ctr) and abs(float(ctr) - derived_ctr) > 0.5:
            issues.append({
                "URL": url,
                "Issue": "CTR Data Mismatch",
                "Priority": "Medium",
                "Current Value": f"Reported CTR={ctr}%, Derived CTR={derived_ctr:.2f}%",
                "Recommendation": "Validate the GSC export before using CTR for automated prioritisation."
            })

pd.DataFrame(issues).to_csv(out, index=False, encoding="utf-8-sig")
print("Data quality report:", out)
print("Issues found:", len(issues))
