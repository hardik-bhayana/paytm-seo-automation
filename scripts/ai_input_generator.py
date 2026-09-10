import pandas as pd
import os

# ==========================================
# Load SEO opportunity reports
# ==========================================

gsc_file = "reports/gsc_opportunities.csv"
technical_file = "reports/technical_seo_issues.csv"

gsc_df = pd.read_csv(gsc_file)
technical_df = pd.read_csv(technical_file)

# ==========================================
# Create AI input records
# ==========================================

ai_records = []

# GSC opportunities
for _, row in gsc_df.head(30).iterrows():

    ai_records.append({
        "URL": row.get("URL", ""),
        "Keyword": row.get("Keyword", ""),
        "Issue": row.get("Opportunity", ""),
        "Priority": row.get("Priority", ""),
        "Clicks": row.get("Clicks", ""),
        "Impressions": row.get("Impressions", ""),
        "CTR": row.get("CTR", ""),
        "Position": row.get("Current Position", ""),
        "Current Value": "",
        "AI Task": "Analyse this SEO opportunity and provide an actionable recommendation."
    })


# Technical SEO issues
for _, row in technical_df.head(30).iterrows():

    ai_records.append({
        "URL": row.get("URL", ""),
        "Keyword": "",
        "Issue": row.get("Issue", ""),
        "Priority": row.get("Priority", ""),
        "Clicks": "",
        "Impressions": "",
        "CTR": "",
        "Position": "",
        "Current Value": row.get("Current Value", ""),
        "AI Task": "Analyse this technical SEO issue and provide an actionable recommendation."
    })


# ==========================================
# Create AI input CSV
# ==========================================

os.makedirs("reports", exist_ok=True)

ai_df = pd.DataFrame(ai_records)

output_file = "reports/ai_input.csv"

ai_df.to_csv(output_file, index=False)

print("\n====================================")
print("AI INPUT GENERATION COMPLETE")
print("====================================")

print(f"GSC opportunities used: {min(30, len(gsc_df))}")
print(f"Technical issues used: {min(30, len(technical_df))}")
print(f"Total AI records: {len(ai_df)}")
print(f"AI input file: {output_file}")

print("\nFirst 10 AI records:")
print(ai_df.head(10).to_string(index=False))

print("\nCompleted successfully.")