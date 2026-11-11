"""Operational metrics: what each model call cost and how often the human accepted the result.

Events are appended to data/metrics.jsonl (private, not committed), one JSON object per line. Recording never
raises: a full disk or a read-only folder must not break a digest or an approval.

    ./kb metrics                       # summary table
    ./kb metrics --write docs/metrics.md
"""
import json
import time
from pathlib import Path

from .schema import ROOT

FILE = "data/metrics.jsonl"


def record(root: Path, kind: str, **fields) -> None:
    try:
        f = root / FILE
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": round(time.time()), "kind": kind, **fields}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def load(root: Path = ROOT) -> list[dict]:
    try:
        lines = (root / FILE).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except ValueError:
            continue  # a half-written last line must not hide the rest
    return out


def from_result_event(ev: dict) -> dict:
    """Pick cost, time and token counts out of a Claude Code `result` event (json or stream-json output)."""
    u = ev.get("usage") or {}
    return {"cost_usd": ev.get("total_cost_usd"), "seconds": round((ev.get("duration_ms") or 0) / 1000, 1),
            "turns": ev.get("num_turns"), "input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens"),
            "cache_read_tokens": u.get("cache_read_input_tokens"), "cache_write_tokens": u.get("cache_creation_input_tokens"),
            "ok": not ev.get("is_error", False)}


def _median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def _calls(events, kind):
    ev = [e for e in events if e["kind"] == kind]
    costs = [e["cost_usd"] for e in ev if e.get("cost_usd") is not None]
    secs = [e["seconds"] for e in ev if e.get("seconds")]
    return {"runs": len(ev), "failed": sum(1 for e in ev if e.get("ok") is False), "cost_total": sum(costs) if costs else None,
            "cost_median": _median(costs), "seconds_median": _median(secs), "seconds_max": max(secs) if secs else None}


def summary(events: list[dict]) -> dict:
    """Aggregate events. Every rate is None when there is nothing to divide by, so callers print 'no data'."""
    digest = _calls(events, "digest")
    d_ev = [e for e in events if e["kind"] == "digest"]
    sources = sum(e.get("sources") or 0 for e in d_ev if e.get("cost_usd") is not None)
    pages = sum(e.get("pages") or 0 for e in d_ev if e.get("cost_usd") is not None)
    digest["cost_per_source"] = digest["cost_total"] / sources if digest["cost_total"] is not None and sources else None
    digest["cost_per_page"] = digest["cost_total"] / pages if digest["cost_total"] is not None and pages else None
    digest["first_pass_valid"] = (sum(1 for e in d_ev if e.get("valid")) / len(d_ev)) if d_ev else None

    reviews = [e for e in events if e["kind"] == "review"]
    approved = [e for e in reviews if e.get("decision") == "approved"]
    discarded = [e for e in reviews if e.get("decision") == "discarded"]
    pa, pd = sum(e.get("pages") or 0 for e in approved), sum(e.get("pages") or 0 for e in discarded)
    review = {"batches_approved": len(approved), "batches_discarded": len(discarded), "pages_approved": pa, "pages_discarded": pd,
              "batch_approval_rate": len(approved) / len(reviews) if reviews else None,
              "page_approval_rate": pa / (pa + pd) if pa + pd else None,
              "amendments": sum(e.get("amended") or 0 for e in approved)}
    return {"digest": digest, "ask": _calls(events, "ask"), "review": review, "events": len(events)}


def _money(v):
    return "no data" if v is None else f"${v:.2f}" if v >= 0.1 else f"${v:.3f}"


def _pct(v):
    return "no data" if v is None else f"{v:.0%}"


def _secs(v):
    return "no data" if v is None else f"{v:.0f} s"


def render(s: dict) -> str:
    d, a, r = s["digest"], s["ask"], s["review"]
    lines = [f"# Operational metrics ({time.strftime('%Y-%m-%d')})", "",
             "Recorded automatically from real use (`data/metrics.jsonl`): one event per model call and per review decision.", "",
             "## Cost and latency", "",
             "| call | runs | failed | median cost | total cost | median time | slowest |", "|---|---|---|---|---|---|---|",
             f"| digest (agent, per batch) | {d['runs']} | {d['failed']} | {_money(d['cost_median'])} | {_money(d['cost_total'])} | {_secs(d['seconds_median'])} | {_secs(d['seconds_max'])} |",
             f"| ask (one tool-less call) | {a['runs']} | {a['failed']} | {_money(a['cost_median'])} | {_money(a['cost_total'])} | {_secs(a['seconds_median'])} | {_secs(a['seconds_max'])} |",
             "", f"- Digest cost per source: **{_money(d['cost_per_source'])}**; per proposed page: **{_money(d['cost_per_page'])}**.",
             f"- Batches that passed validation without a human fixing anything: **{_pct(d['first_pass_valid'])}**.",
             "", "## Human review", "",
             f"- Batches approved: **{r['batches_approved']}**, discarded: **{r['batches_discarded']}** (approval rate {_pct(r['batch_approval_rate'])}).",
             f"- Pages approved: **{r['pages_approved']}**, discarded: **{r['pages_discarded']}** (approval rate {_pct(r['page_approval_rate'])}); {r['amendments']} were amendments to existing pages.",
             "", "Costs are what Claude Code reports for the call (`total_cost_usd`); on a subscription plan they are the API-equivalent price, not a bill."]
    return "\n".join(lines) + "\n"
