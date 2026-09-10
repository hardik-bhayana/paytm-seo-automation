import pandas as pd
import re
from pathlib import Path

FINAL_REPORT = Path("reports/final_seo_report.csv")
CLAUDE_FILE = Path("reports/claude_response.txt")

df = pd.read_csv(FINAL_REPORT)
df["URL"] = df["URL"].fillna("").astype(str).str.strip()
df["Issue"] = df["Issue"].fillna("").astype(str).str.strip()

if "Risk Level" not in df.columns:
    df["Risk Level"] = ""

text = CLAUDE_FILE.read_text(encoding="utf-8")
text = text.replace("\\n", "\n")

# Stop before Cross-Case Observations so it cannot leak into Case 10.
text = re.split(r"(?i)(?:---\s*)?#{2,3}\s*Cross-Case Observations", text)[0]

cases = re.split(r"(?=##\s*Case\s+\d+)", text)
updated = 0

for case in cases:
    if not case.strip():
        continue

    url_match = re.search(
        r"\*\*URL:\*\*\s*(?:\[[^\]]+\]\()?([^\s\)]+)", case
    )
    issue_match = re.search(
        r"\*\*SEO Issue:\*\*\s*([^\n]+)", case
    )

    if not url_match or not issue_match:
        continue

    url = url_match.group(1).strip().rstrip(")")
    issue = issue_match.group(1).strip()

    recommendation_match = re.search(
        r"\*\*AI Recommendation:\*\*\s*(.*?)(?=\s*\*\*Human Review:\*\*)",
        case, re.S
    )
    human_match = re.search(
        r"\*\*Human Review:\*\*\s*(.*?)(?=\s*\*\*Risk Level:\*\*)",
        case, re.S
    )
    risk_match = re.search(
        r"\*\*Risk Level:\*\*\s*(.*?)(?=\s*(?:---|##\s*Case|\Z))",
        case, re.S
    )

    recommendation = recommendation_match.group(1).strip() if recommendation_match else "Not provided"
    human_review = human_match.group(1).strip() if human_match else "Required"
    risk_level = risk_match.group(1).strip() if risk_match else "Not provided"

    recommendation = re.sub(r"\*\*", "", recommendation)
    human_review = re.sub(r"\*\*", "", human_review)
    risk_level = re.sub(r"\*\*", "", risk_level)

    recommendation = re.sub(r"\s+", " ", recommendation).strip()
    human_review = re.sub(r"\s+", " ", human_review).strip()
    risk_level = re.sub(r"\s+", " ", risk_level).strip()

    # Never allow a new section to remain inside Risk Level.
    risk_level = re.split(
        r"(?i)(?:---\s*)?(?:#{2,3}\s*)?(?:Cross-Case Observations|Case\s+\d+)",
        risk_level
    )[0].strip()

    mask = (
        (df["URL"] == url) &
        (df["Issue"].str.lower() == issue.lower())
    )

    if mask.any():
        df.loc[mask, "AI Recommendation"] = recommendation
        df.loc[mask, "Human Review"] = human_review
        df.loc[mask, "Risk Level"] = risk_level
        df.loc[mask, "Status"] = "AI Reviewed"
        updated += int(mask.sum())

df.to_csv(FINAL_REPORT, index=False, encoding="utf-8-sig")

print("\n====================================")
print("CLAUDE OUTPUT MERGED SUCCESSFULLY")
print("====================================")
print("Rows updated:", updated)
print("Final report:", FINAL_REPORT)
print("\nRisk Level Summary:")
print(df["Risk Level"].value_counts(dropna=False))
print("\nAI Review Status:")
print(df["Status"].value_counts(dropna=False))
