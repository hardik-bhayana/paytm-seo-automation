from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parent.parent

steps = [
    ["python", str(ROOT / "scripts" / "gsc_analysis.py")],
    ["python", str(ROOT / "scripts" / "technical_audit.py")],
    ["python", str(ROOT / "scripts" / "ai_input_generator.py")],
    ["python", str(ROOT / "scripts" / "create_claude_prompts.py")],
    ["python", str(ROOT / "scripts" / "create_final_report.py")],
]

for cmd in steps:
    print("\n>>>", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print("Step failed; continuing with repaired pipeline.")
print("\nPIPELINE FINISHED")
