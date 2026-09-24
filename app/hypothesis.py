import uuid
from .models import Evidence, Hypothesis
from .ai import get_llm

def generate_hypotheses(question: str, evidence: list[Evidence]) -> list[Hypothesis]:
    raw = get_llm().generate_hypotheses(question, evidence)
    return [
        Hypothesis(
            id=f"H-{uuid.uuid4().hex[:8]}",
            statement=item["statement"],
            rationale=item["rationale"],
            supporting_evidence=item.get("supporting_evidence", []),
            expected_outcome=item["expected_outcome"],
            assumptions=item.get("assumptions", []),
            testability=item["testability"],
            mock=all(e.mock for e in evidence),
        )
        for item in raw
    ]
