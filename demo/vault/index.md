# Index

_Derived by `./kb build`. Do not edit; edit the pages._

## Maps

- [[start-here-how-this-system-works]] — A short path through the sample vault, from storage to safety to retrieval. (stub, low) · programming

## Concepts

- [[files-as-the-source-of-truth-databases-as-disposable-caches]] — Keep the canonical data in plain files under version control and treat every index or database as something that can be deleted and rebuilt. (reviewed, medium) · programming
- [[human-approval-gate]] — AI-written knowledge lands in a proposals area and becomes part of the knowledge base only when a person approves it. (reviewed, medium) · ai, programming
- [[hybrid-retrieval-with-reciprocal-rank-fusion]] — Search the same passages with a keyword index and with embeddings, then merge the two ranked lists by rank position. (reviewed, medium) · ai
- [[least-privilege-for-llm-agents]] — Give a model only the tools and write access its task needs, so that a hijacked model has nothing dangerous to do. (reviewed, medium) · ai
- [[prompt-injection-through-sources]] — Text inside a document, web page or transcript that tries to give the model instructions, such as "ignore previous instructions". (reviewed, medium) · ai

## Claims

- [[hybrid-retrieval-ranks-the-right-source-first-more-often-than-keyword]] — On this project's 20-question set, hybrid search placed the expected source first in 75% of cases against 50% for keyword search. (reviewed, low) · ai
- [[structural-controls-protect-against-prompt-injection-better-than-promp]] — The project's security document holds that removing tools, confining writes and requiring human approval matter more than how the prompt is phrased. (reviewed, low) · ai

## Open questions

- [[at-what-corpus-size-does-brute-force-cosine-search-stop-being-enough]] — The design uses a NumPy matrix multiply over all passage embeddings and expects that to change at around a million passages; the real threshold is unmeasured. (reviewed, low) · ai, programming

## Entities

- [[bge-small-en-v1-5]] — A small English text-embedding model from BAAI, used here through ONNX for semantic search. (reviewed, medium) · ai

## Sources

- [[architecture-and-design-decisions-this-project]] — The project's own design document: the problem, the components, and each key decision with its cost and gain. (reviewed, high) · programming
- [[ask-evaluation-20-cases-this-project]] — Retrieval results for keyword, semantic and hybrid search on 20 hand-written questions, with the limits of the measurement stated. (reviewed, high) · programming
- [[security-model-this-project]] — The project's threat model: a web page attacking the local server and text in a source attacking the model, with a control and a test for each threat. (reviewed, high) · programming
