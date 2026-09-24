from typing import Protocol
from .models import Paper

class LiteratureProvider(Protocol):
    def search(self, query: str, limit: int = 5) -> list[Paper]: ...

class MockLiteratureProvider:
    def search(self, query: str, limit: int = 5) -> list[Paper]:
        base = [
            Paper(
                id="MOCK-001",
                title="Machine Learning Approaches for Battery Performance Prediction",
                authors=["AstraLab Demo"],
                abstract="Synthetic demonstration record describing machine-learning models for battery state prediction.",
                url="https://example.invalid/astralab/mock-001",
                source="mock",
                mock=True,
            ),
            Paper(
                id="MOCK-002",
                title="Data-Driven Optimization of Battery Materials",
                authors=["AstraLab Demo"],
                abstract="Synthetic demonstration record describing data-driven optimization of material properties.",
                url="https://example.invalid/astralab/mock-002",
                source="mock",
                mock=True,
            ),
            Paper(
                id="MOCK-003",
                title="Benchmarking Regression Models for Energy-System Forecasting",
                authors=["AstraLab Demo"],
                abstract="Synthetic demonstration record describing baseline and nonlinear regression comparisons.",
                url="https://example.invalid/astralab/mock-003",
                source="mock",
                mock=True,
            ),
        ]
        return base[:max(1, min(limit, len(base)))]

class ArxivProvider:
    def search(self, query: str, limit: int = 5) -> list[Paper]:
        import urllib.parse, urllib.request, xml.etree.ElementTree as ET
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
        })
        try:
            with urllib.request.urlopen(url, timeout=12) as response:
                xml = response.read()
            ns = {"a": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(xml)
            papers = []
            for entry in root.findall("a:entry", ns):
                pid = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
                title = " ".join((entry.findtext("a:title", default="", namespaces=ns) or "").split())
                abstract = " ".join((entry.findtext("a:summary", default="", namespaces=ns) or "").split())
                authors = [
                    (a.findtext("a:name", default="", namespaces=ns) or "").strip()
                    for a in entry.findall("a:author", ns)
                ]
                papers.append(Paper(
                    id=pid or title,
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    url=pid,
                    source="arxiv",
                    mock=False,
                ))
            return papers
        except Exception as exc:
            raise RuntimeError(f"arXiv provider failed: {exc}") from exc

def get_literature_provider(name: str):
    if name.lower() == "arxiv":
        return ArxivProvider()
    return MockLiteratureProvider()
