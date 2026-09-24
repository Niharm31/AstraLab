from pathlib import Path
from datetime import datetime, timezone
from .models import Paper, Evidence, Hypothesis, ExperimentResult

def generate_report(research_id, question, papers, evidence, hypotheses, result):
    Path("reports").mkdir(exist_ok=True)
    path = Path("reports") / f"{research_id}.md"
    improvement = "N/A" if result.relative_improvement is None else f"{result.relative_improvement*100:.2f}%"
    lines = [
        f"# AstraLab Research Report — {research_id}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Research Question",
        question,
        "",
        "## Literature",
    ]
    for p in papers:
        lines += [f"- **{p.title}** — {', '.join(p.authors)} — {p.source} — {p.url}"]
    lines += ["", "## Evidence"]
    for e in evidence:
        lines += [f"- **Claim:** {e.claim}", f"  - Evidence: {e.evidence}", f"  - Confidence: {e.confidence:.2f}", f"  - Source: {e.paper_id}"]
    lines += ["", "## Generated Hypotheses"]
    for h in hypotheses:
        lines += [f"### {h.id}", h.statement, "", f"**Rationale:** {h.rationale}", f"**Expected outcome:** {h.expected_outcome}", f"**Testability:** {h.testability}"]
    lines += [
        "",
        "## Computational Experiment",
        "A fixed-seed synthetic regression benchmark compared a linear regression baseline with a random forest model.",
        "",
        "## Results",
        f"- Metric: **{result.metric}**",
        f"- Baseline: **{result.baseline:.6f}**",
        f"- Experimental: **{result.experimental:.6f}**",
        f"- Difference (experimental - baseline): **{result.difference:.6f}**",
        f"- Relative improvement in lower-is-better MAE: **{improvement}**",
        "",
        "## Limitations",
        "- Literature is synthetic in mock mode and must not be treated as real scientific evidence.",
        "- The experiment uses synthetic data and demonstrates engineering workflow rather than a scientific claim about real battery systems.",
        "- A computational result does not establish scientific significance or real-world validity.",
        "",
        "## Reproducibility",
        f"- Experiment seed: `{result.seed}`",
        f"- Result artifact: `experiments/{research_id}/results.json`",
        f"- Manifest: `experiments/{research_id}/manifest.json`",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)
