# Paytm SEO Automation Demo

> Assignment demo for a high-scale fintech SEO automation workflow.

## Important disclaimer
Paytm is used only as a representative high-scale website. Where proprietary/internal data is unavailable, synthetic/sample SEO data is used to demonstrate the workflow.

## Workflow
SEO data → Python rules → issue detection → prioritisation → Claude AI recommendation → human review → GitHub → implementation → QA → monitoring.

## Run
```bash
python scripts/run_all.py
```

## Outputs
- `reports/gsc_opportunities.csv`
- `reports/technical_seo_issues.csv`
- `reports/data_quality.csv`
- `reports/ai_input.csv`
- `reports/final_seo_report.csv`
- `reports/dashboard_summary.csv`

## AI safety
Claude is a recommendation layer. Production changes such as redirects, canonical changes, noindex, consolidation and major financial-content edits require human SEO/compliance approval.

## Scale example
For 1M URLs, automation processes and groups issues first. Humans review prioritised high-impact cases instead of manually checking every URL.
