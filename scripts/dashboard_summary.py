import pandas as pd
from pathlib import Path

report = Path("reports/final_seo_report.csv")
out = Path("reports/dashboard_summary.csv")

df = pd.read_csv(report)

summary = [
    ["Total report rows", len(df)],
    ["AI Reviewed", int((df["Status"] == "AI Reviewed").sum())],
    ["Pending", int((df["Status"] == "Pending").sum())],
    ["High priority", int((df["Priority"].astype(str).str.upper() == "HIGH").sum())],
    ["Medium priority", int((df["Priority"].astype(str).str.upper() == "MEDIUM").sum())],
]

if Path("reports/data_quality.csv").exists():
    dq = pd.read_csv("reports/data_quality.csv")
    summary.append(["Data quality issues", len(dq)])

pd.DataFrame(summary, columns=["Metric", "Value"]).to_csv(
    out, index=False, encoding="utf-8-sig"
)

print("Dashboard summary:", out)
