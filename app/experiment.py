
from pathlib import Path
import json, time, platform
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from .models import ExperimentResult

def run_demo_experiment(experiment_id: str, seed: int = 42) -> ExperimentResult:
    out = Path("experiments") / experiment_id
    out.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)
    X = rng.normal(size=(1200, 6))
    y = (
        2.8 * X[:, 0]**2
        + 1.7 * np.sin(X[:, 1] * 2.0)
        + 1.2 * X[:, 2] * X[:, 3]
        + 0.8 * X[:, 4]
        + rng.normal(0, 0.35, 1200)
    )

    split = 900
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    baseline = LinearRegression()
    experimental = RandomForestRegressor(
        n_estimators=120, max_depth=12, random_state=seed, n_jobs=1
    )

    started = time.time()
    baseline.fit(X_train, y_train)
    experimental.fit(X_train, y_train)

    b = float(mean_absolute_error(y_test, baseline.predict(X_test)))
    e = float(mean_absolute_error(y_test, experimental.predict(X_test)))
    diff = e - b
    rel = ((b - e) / abs(b)) if b else None

    result = ExperimentResult(
        metric="MAE",
        baseline=b,
        experimental=e,
        difference=diff,
        relative_improvement=rel,
        seed=seed,
    )

    (out / "results.json").write_text(result.model_dump_json(indent=2), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({
        "seed": seed,
        "python": platform.python_version(),
        "experiment": "nonlinear_synthetic_regression_baseline_vs_random_forest",
        "duration_seconds": round(time.time() - started, 4),
    }, indent=2), encoding="utf-8")
    return result
