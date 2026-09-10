import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

class SEOAutomationTests(unittest.TestCase):
    def test_source_data_exists(self):
        self.assertTrue((ROOT / "data" / "gsc_data.csv").exists())

    def test_final_report_exists(self):
        self.assertTrue((REPORTS / "final_seo_report.csv").exists())
        df = pd.read_csv(REPORTS / "final_seo_report.csv")
        self.assertIn("URL", df.columns)
        self.assertGreater(len(df), 0)

    def test_dashboard_exists(self):
        self.assertTrue((REPORTS / "dashboard_summary.csv").exists())

if __name__ == "__main__":
    unittest.main()
