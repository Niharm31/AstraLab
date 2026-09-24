from app.literature import MockLiteratureProvider
from app.hypothesis import generate_hypotheses
from app.experiment import run_demo_experiment
from app.research import run_research

def test_mock_literature():
    papers = MockLiteratureProvider().search("battery", 3)
    assert len(papers) == 3
    assert all(p.mock for p in papers)

def test_hypothesis_generation():
    papers = MockLiteratureProvider().search("battery", 3)
    from app.models import Evidence
    evidence = [Evidence(
        claim="demo",
        evidence=p.abstract,
        paper_id=p.id,
        confidence=0.7,
        mock=True,
    ) for p in papers]
    hypotheses = generate_hypotheses("battery ML", evidence)
    assert hypotheses
    assert hypotheses[0].statement

def test_experiment():
    result = run_demo_experiment("TEST-001")
    assert result.baseline >= 0
    assert result.experimental >= 0
    assert result.metric == "MAE"

def test_full_pipeline():
    result = run_research("How can machine learning improve battery performance?")
    assert result.research_id.startswith("R-")
    assert result.papers
    assert result.evidence
    assert result.hypotheses
    assert result.report_path.endswith(".md")
