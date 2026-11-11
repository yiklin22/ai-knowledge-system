"""Evaluation for Ask: retrieval quality (hit rate, MRR) and groundedness of answers.

    .venv/bin/python -m tools.kb.evals                      # retrieval: keyword vs semantic vs hybrid
    .venv/bin/python -m tools.kb.evals --answers 5          # also answer 5 cases with Claude and check groundedness
    .venv/bin/python -m tools.kb.evals --write docs/eval-results.md

Cases are JSON lines in evals/ask_cases.jsonl: {"q": question, "expect": [paths that answer it]}.
The groundedness checks are deterministic (no LLM judge): valid citation numbers, and verbatim quotes.
"""
import argparse
import json
import re
import time
from pathlib import Path

from tools.kb import ask

ROOT = Path(__file__).resolve().parents[2]
KS = (1, 5, 12)


def load_cases(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_retrieval(root: Path, cases, mode="auto", k=12):
    """Per case: rank (1-based) of the first retrieved passage whose file is expected, or None."""
    ranks = []
    for c in cases:
        found = ask.retrieve(root, c["q"], mode=mode, k=k, **c.get("scope", {}))
        rank = next((i + 1 for i, p in enumerate(found) if p["path"] in c["expect"]), None)
        ranks.append(rank)
    return ranks


def summarise(ranks):
    n = len(ranks)
    out = {f"hit@{k}": sum(1 for r in ranks if r and r <= k) / n for k in KS}
    out["mrr"] = sum(1 / r for r in ranks if r) / n
    return out


def _norm(t):
    return re.sub(r"\s+", " ", t.lower().replace("’", "'").replace("“", '"').replace("”", '"').replace("‘", "'")).strip()


def check_answer(answer: str, passages):
    """Deterministic groundedness problems: citations to passages that were not provided, an uncited answer, and
    quotations (>= 25 characters) that do not appear verbatim in any provided passage."""
    problems = []
    cited = {int(n) for n in re.findall(r"\[(\d{1,2})\]", answer)}
    valid = {p["n"] for p in passages}
    if passages and not cited:
        problems.append("no citations")
    problems += [f"cites [{n}] which was not provided" for n in sorted(cited - valid)]
    haystack = _norm(" ".join(p["text"] for p in passages))
    for q in re.findall(r'"([^"\n]{25,})"|“([^”\n]{25,})”', answer):
        quote = _norm(next(x for x in q if x)).rstrip(".,;:")
        if quote not in haystack:
            problems.append(f"quote not found in passages: “{quote[:60]}…”")
    return problems


def run_answers(root: Path, cases, n):
    """Answer the first n cases with Claude and check groundedness. Costs one Claude call per case."""
    results = []
    for c in cases[:n]:
        found = ask.retrieve(root, c["q"], **c.get("scope", {}))
        text = ask.run_claude(ask.build_prompt(c["q"], found), root / "data" / "ask")
        results.append({"q": c["q"], "problems": check_answer(text, found), "cited": sorted(set(re.findall(r"\[(\d{1,2})\]", text)))})
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", default=str(ROOT / "evals" / "ask_cases.jsonl"))
    ap.add_argument("--answers", type=int, default=0, help="also answer this many cases with Claude")
    ap.add_argument("--write", help="write a Markdown report to this path")
    a = ap.parse_args()
    cases = load_cases(Path(a.cases))
    modes = ["keyword"] + (["semantic", "hybrid"] if ask.embeddings_available() and ask.embedding_status(ROOT)[0] else [])
    lines = [f"# Ask evaluation ({len(cases)} cases, {time.strftime('%Y-%m-%d')})", "",
             "Retrieval: did a passage from the expected source appear in the top results? "
             "`hit@k` = share of questions answered within the top k passages; `MRR` = mean reciprocal rank of the first correct passage.", "",
             "| mode | hit@1 | hit@5 | hit@12 | MRR |", "|---|---|---|---|---|"]
    misses = {}
    for m in modes:
        r = run_retrieval(ROOT, cases, mode=m)
        s = summarise(r)
        lines.append(f"| {m} | {s['hit@1']:.0%} | {s['hit@5']:.0%} | {s['hit@12']:.0%} | {s['mrr']:.2f} |")
        misses[m] = [c["q"] for c, x in zip(cases, r) if not x]
    for m, qs in misses.items():
        if qs:
            lines += ["", f"Missed in **{m}** mode (not in top 12):"] + [f"- {q}" for q in qs]
    if a.answers:
        res = run_answers(ROOT, cases, a.answers)
        ok = sum(1 for r in res if not r["problems"])
        lines += ["", f"## Groundedness ({len(res)} answers)", "", f"{ok}/{len(res)} answers had valid citations and only verbatim quotes."]
        lines += [f"- {r['q']}: {'; '.join(r['problems'])}" for r in res if r["problems"]]
    report = "\n".join(lines) + "\n"
    print(report)
    if a.write:
        Path(a.write).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
