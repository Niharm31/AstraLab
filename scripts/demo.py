import json
from app.core.logging import configure_logging
from app.research import run_research

def main():
    configure_logging()
    question = "How can machine learning improve battery performance?"
    print("=" * 60)
    print("ASTRALAB SCIENTIFIC DISCOVERY ENGINE")
    print("=" * 60)
    print("Research Question:", question)
    print("[1/6] Searching literature...")
    result = run_research(question)
    print("[2/6] Evidence extracted")
    print("[3/6] Hypothesis generated")
    print("[4/6] Experiment created")
    print("[5/6] Experiment executed")
    print("[6/6] Report generated")
    print()
    print("RESULT")
    print(f"Research ID: {result.research_id}")
    print(f"Baseline MAE: {result.result.baseline:.6f}")
    print(f"Experimental MAE: {result.result.experimental:.6f}")
    print(f"Difference: {result.result.difference:.6f}")
    if result.result.relative_improvement is not None:
        print(f"Relative improvement: {result.result.relative_improvement * 100:.2f}%")
    print(f"Report: {result.report_path}")
    print("DONE")

if __name__ == "__main__":
    main()
