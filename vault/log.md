# Log

Append-only. Each entry starts with `## [YYYY-MM-DD] <operation> | <title>` so it can be searched with:
`grep "^## \[" wiki/log.md | tail -5`

## [2026-11-06] init | Wiki created
Topic: AI. Empty skeleton: raw/, wiki/index.md, wiki/log.md.

## [2026-11-06] schema | CLAUDE.md v1
Defined core types, frontmatter, relations, body sections, tagging, validation rules.

## [2026-11-08] schema | CLAUDE.md v2 (section 14 Intake)
Added intake workflow. Created tools/ingest.py, raw/{chats,documents,web,videos}.

## [2026-11-08] schema | Schema v2: multidisciplinary knowledge system
wiki/ renamed to vault/. Eight entity types (source, concept, claim, entity, question, insight, project, map), opaque ids, domains, proposals/ workflow with human approval, derived indexes (build/), SQLite learning layer (data/learning.db), tools/kb CLI + tests. See docs/knowledge-schema.md. Old six-type AI-only schema replaced; vault was empty so no migration needed.

## [2026-11-08] approve | ai-curriculum
- added vault/concepts/adam-and-modern-optimizers.md (cpt_0zqyyvm3)
- added vault/concepts/ai-alignment.md (cpt_rxnywosi)
- added vault/concepts/backpropagation.md (cpt_sawcp9g6)
- added vault/concepts/benchmark-contamination.md (cpt_moohgz03)
- added vault/concepts/convolutional-neural-networks.md (cpt_cjd65ji2)
- added vault/concepts/decoding-and-sampling.md (cpt_l3s5o9i7)
- added vault/concepts/derivatives-and-gradients.md (cpt_j1pzsz1z)
- added vault/concepts/diffusion-models.md (cpt_la33hi6u)
- added vault/concepts/direct-preference-optimization.md (cpt_yxdd8lvt)
- added vault/concepts/embeddings.md (cpt_d10rzi67)
- added vault/concepts/entropy-and-cross-entropy.md (cpt_gbtmoc62)
- added vault/concepts/evaluating-llms.md (cpt_1dk2t19q)
- added vault/concepts/gradient-descent.md (cpt_b4estw58)
- added vault/concepts/hallucination.md (cpt_a602ati7)
- added vault/concepts/in-context-learning.md (cpt_02ceyiw3)
- added vault/concepts/kv-cache.md (cpt_aj415iv5)
- added vault/concepts/language-modeling.md (cpt_fsyf2ys2)
- added vault/concepts/linear-algebra-for-ml.md (cpt_vb2rdsqz)
- added vault/concepts/llm-agents.md (cpt_9ug6lxd3)
- added vault/concepts/loss-functions.md (cpt_rez0ra3h)
- added vault/concepts/low-rank-adaptation-lora.md (cpt_7yi39z1u)
- added vault/concepts/mechanistic-interpretability.md (cpt_hrzo5jmc)
- added vault/concepts/mixture-of-experts.md (cpt_3o0xla6w)
- added vault/concepts/neural-networks.md (cpt_s92mncas)
- added vault/concepts/overfitting-and-generalization.md (cpt_ob6w2kq2)
- added vault/concepts/positional-encoding.md (cpt_g0clar9v)
- added vault/concepts/probability-and-statistics-basics.md (cpt_ewby2b74)
- added vault/concepts/prompt-engineering.md (cpt_be51ajjr)
- added vault/concepts/prompt-injection.md (cpt_svq1gwub)
- added vault/concepts/quantization.md (cpt_xi24x0ku)
- added vault/concepts/regularization.md (cpt_vau7nfp4)
- added vault/concepts/reinforcement-learning-basics.md (cpt_nc6s1zdy)
- added vault/concepts/reinforcement-learning-from-human-feedback.md (cpt_tqbd5i2f)
- added vault/concepts/retrieval-augmented-generation.md (cpt_b99cr5t8)
- added vault/concepts/scaling-laws.md (cpt_8cceawd5)
- added vault/concepts/self-attention.md (cpt_0ryfzibo)
- added vault/concepts/supervised-fine-tuning.md (cpt_miqp75kg)
- added vault/concepts/supervised-learning.md (cpt_c0pgntxg)
- added vault/concepts/tokenization.md (cpt_92s0kwnu)
- added vault/concepts/tool-use-and-function-calling.md (cpt_eripv7vv)
- added vault/concepts/train-validation-and-test-splits.md (cpt_kw8vqr82)
- added vault/concepts/transformer-architecture.md (cpt_tp1bkybc)
- added vault/concepts/vector-search.md (cpt_ghltp2gf)
- added vault/questions/can-hallucination-be-eliminated-or-only-reduced.md (qst_fwb03lfq)
- added vault/questions/do-language-models-build-internal-world-models.md (qst_mdkp8ma5)
- added vault/questions/do-scaling-laws-keep-holding-as-models-and-data-grow.md (qst_xos1ypjo)
- added vault/questions/how-reliable-is-llm-as-a-judge-evaluation.md (qst_2wilgfwk)
- added vault/maps/ai-curriculum.md (map_wt9hf4tp)
