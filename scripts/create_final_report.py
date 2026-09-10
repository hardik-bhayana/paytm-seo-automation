import pandas as pd
import os

# ==========================================
# Load reports
# ==========================================

gsc_file = "reports/gsc_opportunities.csv"
technical_file = "reports/technical_seo_issues.csv"

gsc_df = pd.read_csv(gsc_file)
technical_df = pd.read_csv(technical_file)

final_records = []

# ==========================================
# GSC Opportunities
# ==========================================

for _, row in gsc_df.iterrows():

    final_records.append({
        "URL": row.get("URL", ""),
        "Keyword": row.get("Keyword", ""),
        "Issue": row.get("Opportunity", ""),
        "Priority": row.get("Priority", ""),
        "Current Data": (
            f"Position: {row.get('Current Position', '')}; "
            f"Impressions: {row.get('Impressions', '')}; "
            f"CTR: {row.get('CTR', '')}"
        ),
        "AI Recommendation": "Pending Claude AI analysis",
        "Human Review": "Required",
        "Status": "Pending"
    })


# ==========================================
# Technical SEO Issues
# ==========================================

for _, row in technical_df.iterrows():

    final_records.append({
        "URL": row.get("URL", ""),
        "Keyword": "",
        "Issue": row.get("Issue", ""),
        "Priority": row.get("Priority", ""),
        "Current Data": row.get("Current Value", ""),
        "AI Recommendation": "Pending Claude AI analysis",
        "Human Review": "Required",
        "Status": "Pending"
    })


# ==========================================
# Create Final Report
# ==========================================

final_df = pd.DataFrame(final_records)

# Remove completely empty URLs
final_df = final_df[
    final_df["URL"].notna() &
    (final_df["URL"].astype(str).str.strip() != "")
]

# Remove duplicate rows
final_df = final_df.drop_duplicates()

# Priority sorting
priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

final_df["Priority_Order"] = final_df["Priority"].map(priority_order)

final_df = final_df.sort_values(
    by=["Priority_Order"],
    ascending=True
)

final_df = final_df.drop(columns=["Priority_Order"])

# ==========================================
# Save
# ==========================================

os.makedirs("reports", exist_ok=True)

output_file = "reports/final_seo_report.csv"

final_df.to_csv(
    output_file,
    index=False
)

# ==========================================
# Summary
# ==========================================

print("\n======================================")
print("FINAL SEO REPORT CREATED")
print("======================================")

print(f"Total SEO records: {len(final_df)}")

print("\nPriority Summary:")

print(
    final_df["Priority"]
    .value_counts()
    .to_string()
)

print("\nIssue Summary:")

print(
    final_df["Issue"]
    .value_counts()
    .head(15)
    .to_string()
)

print(f"\nReport created: {output_file}")

print("\nCompleted successfully.")