import pandas as pd

# ==============================
# 1. Load GSC Data
# ==============================

input_file = "data/gsc_data.csv"
output_file = "reports/gsc_opportunities.csv"

df = pd.read_csv(input_file)

# Convert numeric columns
df["Clicks"] = pd.to_numeric(df["Clicks"], errors="coerce").fillna(0)
df["Impressions"] = pd.to_numeric(df["Impressions"], errors="coerce").fillna(0)
df["CTR"] = pd.to_numeric(df["CTR"], errors="coerce").fillna(0)
df["Position"] = pd.to_numeric(df["Position"], errors="coerce")

# ==============================
# 2. Detect SEO Opportunities
# ==============================

opportunities = []

for _, row in df.iterrows():

    url = row["URL"]
    keyword = row["Keyword"]
    impressions = row["Impressions"]
    ctr = row["CTR"]
    position = row["Position"]

    # --------------------------------
    # Opportunity 1:
    # High impressions + low CTR
    # --------------------------------

    if impressions >= 1000 and ctr < 3:
        opportunities.append({
            "URL": url,
            "Keyword": keyword,
            "Opportunity": "Low CTR Opportunity",
            "Priority": "High",
            "Current Position": position,
            "Impressions": impressions,
            "CTR": ctr,
            "Recommendation": "Improve title tag and meta description to increase CTR."
        })

    # --------------------------------
    # Opportunity 2:
    # Position 11-20
    # --------------------------------

    if 11 <= position <= 20 and impressions >= 500:
        opportunities.append({
            "URL": url,
            "Keyword": keyword,
            "Opportunity": "Page 2 Ranking Opportunity",
            "Priority": "High",
            "Current Position": position,
            "Impressions": impressions,
            "CTR": ctr,
            "Recommendation": "Improve content depth, internal links and search intent alignment."
        })

    # --------------------------------
    # Opportunity 3:
    # Position 4-10
    # --------------------------------

    if 4 <= position <= 10 and impressions >= 1000:
        opportunities.append({
            "URL": url,
            "Keyword": keyword,
            "Opportunity": "Top 3 Opportunity",
            "Priority": "Medium",
            "Current Position": position,
            "Impressions": impressions,
            "CTR": ctr,
            "Recommendation": "Strengthen on-page SEO, internal linking and content relevance to push into Top 3."
        })


# ==============================
# 3. Detect Keyword Cannibalization
# ==============================

keyword_url_counts = df.groupby("Keyword")["URL"].nunique()

cannibalization_keywords = keyword_url_counts[
    keyword_url_counts > 1
].index

for keyword in cannibalization_keywords:

    keyword_rows = df[df["Keyword"] == keyword]

    for _, row in keyword_rows.iterrows():

        opportunities.append({
            "URL": row["URL"],
            "Keyword": keyword,
            "Opportunity": "Keyword Cannibalization",
            "Priority": "High",
            "Current Position": row["Position"],
            "Impressions": row["Impressions"],
            "CTR": row["CTR"],
            "Recommendation": "Review competing URLs and decide which page should be the primary ranking page."
        })


# ==============================
# 4. Create Opportunity Report
# ==============================

opportunity_df = pd.DataFrame(opportunities)

# Create reports folder if required
import os

os.makedirs("reports", exist_ok=True)

if not opportunity_df.empty:

    # Remove duplicate opportunities
    opportunity_df = opportunity_df.drop_duplicates()

    # Sort by priority and impressions
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    opportunity_df["Priority_Order"] = opportunity_df["Priority"].map(
        priority_order
    )

    opportunity_df = opportunity_df.sort_values(
        by=["Priority_Order", "Impressions"],
        ascending=[True, False]
    )

    opportunity_df = opportunity_df.drop(
        columns=["Priority_Order"]
    )

    opportunity_df.to_csv(
        output_file,
        index=False
    )

    print("\n====================================")
    print("SEO OPPORTUNITY ANALYSIS COMPLETE")
    print("====================================")

    print(f"Total URLs analysed: {len(df)}")
    print(f"SEO opportunities found: {len(opportunity_df)}")
    print(f"Report created: {output_file}")

    print("\nOpportunity Summary:")
    print(
        opportunity_df["Opportunity"]
        .value_counts()
        .to_string()
    )

else:

    print("\nNo SEO opportunities found.")

print("\nAnalysis completed successfully.")