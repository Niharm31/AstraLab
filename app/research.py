import uuid
from .core.config import settings
from .literature import get_literature_provider
from .models import Evidence, ResearchResponse
from .hypothesis import generate_hypotheses
from .experiment import run_demo_experiment
from .report import generate_report

def run_research(question: str) -> ResearchResponse:
    research_id = f"R-{uuid.uuid4().hex[:10]}"
    provider = get_literature_provider(settings.literature_provider)
    papers = provider.search(question, limit=3)

    evidence = []
    for p in papers:
        evidence.append(Evidence(
            claim=f"Literature record {p.id} discusses machine-learning methods relevant to the research question.",
            evidence=p.abstract,
            paper_id=p.id,
            confidence=0.70 if p.mock else 0.60,
            evidence_type="computational",
            mock=p.mock,
        ))

    hypotheses = generate_hypotheses(question, evidence)
    result = run_demo_experiment(research_id)
    report_path = generate_report(research_id, question, papers, evidence, hypotheses, result)

    return ResearchResponse(
        research_id=research_id,
        question=question,
        papers=papers,
        evidence=evidence,
        hypotheses=hypotheses,
        result=result,
        report_path=report_path,
    )
