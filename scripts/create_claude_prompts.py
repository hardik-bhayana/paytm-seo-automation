import pandas as pd
import os

input_file = "reports/ai_input.csv"
output_file = "reports/claude_prompts.txt"

df = pd.read_csv(input_file)

# Top 10 high-priority records for AI review
df = df.head(10)

prompts = []

for _, row in df.iterrows():

    prompt = f"""
You are an expert SEO analyst working on a high-scale fintech website.

Analyse the following SEO case.

URL:
{row['URL']}

Keyword:
{row['Keyword']}

SEO Issue:
{row['Issue']}

Priority:
{row['Priority']}

Clicks:
{row['Clicks']}

Impressions:
{row['Impressions']}

CTR:
{row['CTR']}

Current Position:
{row['Position']}

Current Value:
{row['Current Value']}

Provide:

1. SEO Problem
2. Why this matters
3. Recommended Action
4. Suggested SEO improvement
5. Human Review Required
6. Risk Level

Important:
- Do not recommend automatic production changes.
- A human SEO must approve important changes.
- Keep the recommendation practical and specific.
"""

    prompts.append(prompt)


os.makedirs("reports", exist_ok=True)

with open(output_file, "w", encoding="utf-8") as file:

    file.write(
        "\n\n"
        + "=" * 80
        + "\n\n".join(prompts)
    )

print("\n====================================")
print("CLAUDE PROMPTS CREATED")
print("====================================")

print(f"Records sent for AI analysis: {len(df)}")
print(f"Output file: {output_file}")

print("\nCompleted successfully.")