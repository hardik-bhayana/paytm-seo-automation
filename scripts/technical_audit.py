import pandas as pd
import os

# =====================================
# 1. Load SEO Data
# =====================================

input_file = "data/gsc_data.csv"
output_file = "reports/technical_seo_issues.csv"

df = pd.read_csv(input_file)

issues = []


# =====================================
# 2. Missing Title Check
# =====================================

for _, row in df.iterrows():

    url = row["URL"]

    title = str(row["Title"]).strip()

    if pd.isna(row["Title"]) or title == "" or title.lower() == "nan":

        issues.append({
            "URL": url,
            "Issue": "Missing Title",
            "Priority": "High",
            "Current Value": "Missing",
            "Recommendation": "Add a unique and descriptive title tag."
        })


# =====================================
# 3. Missing Meta Description Check
# =====================================

for _, row in df.iterrows():

    url = row["URL"]

    meta = str(row["Meta Description"]).strip()

    if pd.isna(row["Meta Description"]) or meta == "" or meta.lower() == "nan":

        issues.append({
            "URL": url,
            "Issue": "Missing Meta Description",
            "Priority": "Medium",
            "Current Value": "Missing",
            "Recommendation": "Add a relevant meta description."
        })


# =====================================
# 4. Missing H1 Check
# =====================================

for _, row in df.iterrows():

    url = row["URL"]

    h1 = str(row["H1"]).strip()

    if pd.isna(row["H1"]) or h1 == "" or h1.lower() == "nan":

        issues.append({
            "URL": url,
            "Issue": "Missing H1",
            "Priority": "High",
            "Current Value": "Missing",
            "Recommendation": "Add one clear and relevant H1."
        })


# =====================================
# 5. Status Code Check
# =====================================

for _, row in df.iterrows():

    url = row["URL"]

    status = str(row["Status"]).strip()

    if status not in ["200", "200.0"]:

        issues.append({
            "URL": url,
            "Issue": "HTTP Status Issue",
            "Priority": "High",
            "Current Value": status,
            "Recommendation": "Investigate the page status and fix important non-200 URLs."
        })


# =====================================
# 6. Indexability Check
# =====================================

for _, row in df.iterrows():

    url = row["URL"]

    indexability = str(row["Indexability"]).strip().lower()

    if indexability != "indexable":

        issues.append({
            "URL": url,
            "Issue": "Indexability Issue",
            "Priority": "High",
            "Current Value": row["Indexability"],
            "Recommendation": "Review robots, meta robots and indexation settings."
        })


# =====================================
# 7. Canonical Check
# =====================================

for _, row in df.iterrows():

    url = row["URL"]

    canonical = str(row["Canonical"]).strip()

    if pd.isna(row["Canonical"]) or canonical == "" or canonical.lower() == "nan":

        issues.append({
            "URL": url,
            "Issue": "Missing Canonical",
            "Priority": "High",
            "Current Value": "Missing",
            "Recommendation": "Add a self-referencing or appropriate canonical URL."
        })


# =====================================
# 8. Duplicate Title Check
# =====================================

duplicate_titles = df[
    df["Title"].duplicated(keep=False) &
    df["Title"].notna()
]

for _, row in duplicate_titles.iterrows():

    issues.append({
        "URL": row["URL"],
        "Issue": "Duplicate Title",
        "Priority": "Medium",
        "Current Value": row["Title"],
        "Recommendation": "Create a unique title based on page intent and target keyword."
    })


# =====================================
# 9. Create Final Report
# =====================================

os.makedirs("reports", exist_ok=True)

issues_df = pd.DataFrame(issues)

if not issues_df.empty:

    issues_df = issues_df.drop_duplicates()

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    issues_df["Priority_Order"] = issues_df["Priority"].map(
        priority_order
    )

    issues_df = issues_df.sort_values(
        by="Priority_Order"
    )

    issues_df = issues_df.drop(
        columns=["Priority_Order"]
    )

    issues_df.to_csv(
        output_file,
        index=False
    )

    print("\n===================================")
    print("TECHNICAL SEO AUDIT COMPLETE")
    print("===================================")

    print(f"Total URLs analysed: {len(df)}")
    print(f"Technical issues found: {len(issues_df)}")
    print(f"Report created: {output_file}")

    print("\nIssue Summary:")

    print(
        issues_df["Issue"]
        .value_counts()
        .to_string()
    )

else:

    print("\nNo technical SEO issues found.")


print("\nTechnical audit completed successfully.")