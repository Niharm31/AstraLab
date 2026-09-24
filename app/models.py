from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class Paper(BaseModel):
    id: str
    title: str
    authors: list[str]
    abstract: str
    url: str
    source: str
    mock: bool = False

class Evidence(BaseModel):
    claim: str
    evidence: str
    paper_id: str
    confidence: float = Field(ge=0, le=1)
    evidence_type: str = "computational"
    mock: bool = False

class Hypothesis(BaseModel):
    id: str
    statement: str
    rationale: str
    supporting_evidence: list[str]
    expected_outcome: str
    assumptions: list[str]
    testability: str
    mock: bool = False

class ExperimentResult(BaseModel):
    metric: str
    baseline: float
    experimental: float
    difference: float
    relative_improvement: float | None
    seed: int

class ResearchRequest(BaseModel):
    question: str = Field(min_length=8, max_length=2000)

class ResearchResponse(BaseModel):
    research_id: str
    question: str
    papers: list[Paper]
    evidence: list[Evidence]
    hypotheses: list[Hypothesis]
    result: ExperimentResult
    report_path: str

class HealthResponse(BaseModel):
    status: str
    mock_mode: bool
    llm_provider: str
    literature_provider: str
