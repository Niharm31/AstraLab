
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from .core.logging import configure_logging
from .core.config import settings
from .models import ResearchRequest, HealthResponse
from .research import run_research

configure_logging()

app = FastAPI(
    title="AstraLab",
    version="0.2.0",
    description="AI-assisted scientific research and computational experimentation platform.",
)

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AstraLab — Scientific Discovery Engine</title>
<style>
:root{--bg:#070b18;--panel:#0e1528;--panel2:#121b31;--line:#24314d;--text:#edf3ff;--muted:#94a3bd;--accent:#6ea8ff;--good:#4ade80;--warn:#fbbf24}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 15% 0%,#15234a 0,#070b18 42%);color:var(--text);font:15px/1.55 Inter,Segoe UI,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:44px 22px 70px}.brand{display:flex;gap:14px;align-items:center}.logo{font-size:36px}.brand h1{margin:0;font-size:31px}.sub{color:var(--muted);margin:4px 0 28px}
.search{display:flex;gap:10px;background:rgba(14,21,40,.9);padding:10px;border:1px solid var(--line);border-radius:16px;box-shadow:0 12px 40px #0004}
input{flex:1;min-width:0;background:#fff;color:#111827;border:0;border-radius:10px;padding:14px 16px;font-size:15px;outline:none}
button{border:1px solid #7897c9;background:#eaf2ff;color:#0b1220;border-radius:10px;padding:0 20px;font-weight:700;cursor:pointer}button:disabled{opacity:.55;cursor:wait}
#status{margin:16px 0;color:var(--muted);min-height:24px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:0 10px 30px #0003}.wide{grid-column:1/-1}
h2{font-size:18px;margin:0 0 14px}h3{font-size:16px;margin:0 0 7px}.muted{color:var(--muted)}.pill{display:inline-block;padding:3px 8px;border-radius:99px;background:#19305b;color:#aecdff;font-size:12px;margin-left:7px}.mock{background:#4b3410;color:#ffd978}
.paper{padding:14px 0;border-top:1px solid var(--line)}.paper:first-child{border-top:0}.paper a{color:#8dbbff;text-decoration:none}.paper a:hover{text-decoration:underline}
.ev{padding:12px;border:1px solid var(--line);border-radius:10px;margin:9px 0}.confidence{color:var(--good);font-weight:700}
.result{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.metric{background:#0a1122;border:1px solid var(--line);padding:14px;border-radius:12px}.metric b{display:block;font-size:21px;margin-top:3px}
pre{background:#070c18;border:1px solid var(--line);padding:14px;border-radius:10px;overflow:auto}.report{display:inline-block;margin-top:10px;color:#9ec5ff}
.empty{color:var(--muted);padding:28px 0;text-align:center}.error{color:#fecaca;background:#3a1418;border:1px solid #7f3038;padding:13px;border-radius:10px}
@media(max-width:760px){.grid{grid-template-columns:1fr}.wide{grid-column:auto}.search{flex-direction:column}button{height:46px}.result{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <div class="brand"><div class="logo">🧬</div><div><h1>AstraLab</h1><div class="sub">AI-assisted scientific discovery workspace</div></div></div>

  <div class="search">
    <input id="q" value="How can machine learning improve battery performance?" aria-label="Research question">
    <button id="run" onclick="runResearch()">Run Research</button>
  </div>
  <div id="status">Ready. Enter a research question to begin.</div>
  <div id="app"><div class="card empty">Your research pipeline results will appear here.</div></div>
</div>

<script>
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
const fmt = n => typeof n === 'number' ? n.toFixed(4) : esc(n);

function render(d){
  const papers = d.papers.map(p => `
    <div class="paper">
      <h3>${esc(p.title)} <span class="pill ${p.mock?'mock':''}">${p.mock?'DEMO DATA':esc(p.source)}</span></h3>
      <div class="muted">${esc(p.authors.join(', '))}</div>
      <p>${esc(p.abstract)}</p>
      <a href="${esc(p.url)}" target="_blank" rel="noopener">Open source ↗</a>
    </div>`).join('');

  const evidence = d.evidence.map(e => `
    <div class="ev">
      <b>${esc(e.claim)}</b>
      <div>${esc(e.evidence)}</div>
      <div class="muted">Source: ${esc(e.paper_id)} · Confidence: <span class="confidence">${fmt(e.confidence)}</span></div>
    </div>`).join('');

  const hypotheses = d.hypotheses.map(h => `
    <div class="ev">
      <h3>${esc(h.statement)}</h3>
      <div><b>Rationale:</b> ${esc(h.rationale)}</div>
      <div><b>Expected outcome:</b> ${esc(h.expected_outcome)}</div>
      <div><b>Testability:</b> ${esc(h.testability)}</div>
      <div class="muted"><b>Assumptions:</b> ${esc(h.assumptions.join('; '))}</div>
    </div>`).join('');

  const r = d.result;
  document.getElementById('app').innerHTML = `
    <div class="grid">
      <section class="card wide"><h2>Research Question</h2><div>${esc(d.question)}</div></section>
      <section class="card wide"><h2>Experiment Results</h2>
        <div class="result">
          <div class="metric">Metric<b>${esc(r.metric)}</b></div>
          <div class="metric">Baseline<b>${fmt(r.baseline)}</b></div>
          <div class="metric">Experimental<b>${fmt(r.experimental)}</b></div>
        </div>
        <div class="muted" style="margin-top:12px">Difference: ${fmt(r.difference)} · Relative improvement: ${r.relative_improvement == null ? 'N/A' : fmt(r.relative_improvement*100)+'%'}</div>
        <a class="report" href="/reports/${encodeURIComponent(d.research_id)}" target="_blank">View generated report ↗</a>
      </section>
      <section class="card wide"><h2>Literature <span class="pill">${d.papers.length} records</span></h2>${papers}</section>
      <section class="card"><h2>Evidence</h2>${evidence || '<div class="empty">No evidence.</div>'}</section>
      <section class="card"><h2>Candidate Hypotheses</h2>${hypotheses || '<div class="empty">No hypotheses.</div>'}</section>
      <section class="card wide"><details><summary>Developer JSON</summary><pre>${esc(JSON.stringify(d,null,2))}</pre></details></section>
    </div>`;
}

async function runResearch(){
  const q=document.getElementById('q').value.trim(), btn=document.getElementById('run'), status=document.getElementById('status');
  if(q.length<8){status.innerHTML='<div class="error">Please enter a more specific research question.</div>';return}
  btn.disabled=true; status.textContent='Running literature search → evidence → hypothesis → experiment → report…';
  try{
    const res=await fetch('/research',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
    const data=await res.json();
    if(!res.ok) throw new Error(data.detail || 'Research pipeline failed');
    render(data); status.textContent=`Completed research run ${data.research_id}.`;
  }catch(e){status.innerHTML='<div class="error">'+esc(e.message)+'</div>'}
  finally{btn.disabled=false}
}
</script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def root():
    return PAGE

@app.get("/reports/{research_id}", response_class=HTMLResponse)
def report(research_id: str):
    from pathlib import Path
    path = Path("reports") / f"{research_id}.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    # Simple Markdown-like presentation without adding a frontend dependency.
    import html
    text = html.escape(path.read_text(encoding="utf-8"))
    return HTMLResponse(f"""<!doctype html><html><head><meta charset="utf-8"><title>AstraLab Report</title>
    <style>body{{max-width:900px;margin:40px auto;padding:20px;background:#080d1b;color:#eaf1ff;font:15px/1.6 system-ui}}pre{{white-space:pre-wrap;background:#111a2e;padding:24px;border-radius:12px}}</style>
    </head><body><h1>🧬 AstraLab Research Report</h1><pre>{text}</pre></body></html>""")

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", mock_mode=settings.mock_mode, llm_provider=settings.llm_provider, literature_provider=settings.literature_provider)

@app.post("/research")
def research(request: ResearchRequest):
    try:
        return run_research(request.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Research pipeline failed: {exc}") from exc
