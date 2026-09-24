# AstraLab 🧬

AstraLab is an AI-assisted scientific research prototype that turns a research question into a structured literature/evidence workflow, candidate hypothesis, reproducible computational experiment, metrics, and a research report.

## Current status

**v0.1 — Working end-to-end MVP**

Pipeline:

```text
Research Question
      ↓
Literature
      ↓
Evidence
      ↓
Hypothesis
      ↓
Computational Experiment
      ↓
Evaluation
      ↓
Report
```

## Important scientific limitation

Mock literature is synthetic demonstration data. It is not real scientific evidence. The included experiment uses synthetic data and demonstrates the engineering pipeline; it does not establish a real-world scientific claim.

## Quick start — Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest
python -m scripts.demo
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## API

Health:

```text
GET /health
```

Research:

```text
POST /research
Content-Type: application/json

{
  "question": "How can machine learning improve battery performance?"
}
```

## Local LLM

Set:

```env
LLM_PROVIDER=local
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_MODEL=your-model
```

The MVP keeps mock mode available so the complete pipeline remains runnable without an LLM.

## Roadmap

- Real arXiv/Semantic Scholar retrieval
- RAG and embeddings
- Persistent research database
- Multi-agent orchestration
- Knowledge graph
- Restricted experiment sandbox
- richer dashboard
- reproducibility benchmarking
- domain-specific scientific tools
