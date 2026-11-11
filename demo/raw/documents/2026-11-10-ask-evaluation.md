# Ask evaluation (20 cases, 2026-11-10)

Retrieval: did a passage from the expected source appear in the top results? `hit@k` = share of questions answered within the top k passages; `MRR` = mean reciprocal rank of the first correct passage.

| mode | hit@1 | hit@5 | hit@12 | MRR |
|---|---|---|---|---|
| keyword | 50% | 95% | 100% | 0.69 |
| semantic | 65% | 95% | 100% | 0.76 |
| hybrid | 75% | 95% | 100% | 0.82 |

## How to read this

- **Corpus:** about 7,700 passages from ~700 sources (web, video transcripts, PDFs) plus approved vault pages. Model: `BAAI/bge-small-en-v1.5`; hybrid = reciprocal-rank fusion of BM25 and embeddings.
- **Cases:** 20 questions written by hand from the documents' content (not their titles), each with one known answering file. 17 target raw sources and 3 target vault concept pages.
- **Limits:** 20 cases is a small sample, so differences of one question (5 points) are noise. The result to trust is the direction: hybrid placed the right source first more often (75% vs 50% keyword-only) at no cost to recall. Questions were written by the project author, who also built the retriever, which risks optimistic bias; extending the set with questions from real use is the next step.
- **Reproduce:** `.venv/bin/python -m tools.kb.evals --write docs/eval-results.md` (add `--answers 5` to also score groundedness with Claude).
