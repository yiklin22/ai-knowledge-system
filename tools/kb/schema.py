"""Schema constants (docs/knowledge-schema.md v2). No I/O."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 2

# type -> (folder, id prefix)
TYPES = {
    "source": ("sources", "src"), "concept": ("concepts", "cpt"), "claim": ("claims", "clm"),
    "entity": ("entities", "ent"), "question": ("questions", "qst"), "insight": ("insights", "ins"),
    "project": ("projects", "prj"), "map": ("maps", "map"),
}
COMMON_FIELDS = ["id", "schema", "type", "title", "aliases", "domains", "summary", "tags", "status",
                 "confidence", "created", "updated", "sources", "relations"]
ENUMS = {
    "status": {"stub", "draft", "reviewed", "outdated", "deprecated"},
    "confidence": {"low", "medium", "high"},
}
TYPE_ENUMS = {
    "source": {"kind": {"chat", "document", "web", "video", "paper", "book", "note"},
               "reliability": {"primary", "secondary", "vendor", "ai-chat", "opinion"}},
    "entity": {"kind": {"person", "organization", "paper", "book", "model", "product", "benchmark", "tool", "dataset"}},
    "claim": {"verdict": {"unverified", "supported", "contested", "refuted"}},
    "question": {"state": {"open", "answered", "parked"}},
    "insight": {"kind": {"lesson", "decision", "preference", "principle"}},
    "project": {"state": {"idea", "active", "paused", "done"}},
}
SOURCES_OPTIONAL = {"insight", "question", "project", "map", "source", "entity"}
RELS = {  # rel -> inverse
    "related": "related", "broader": "narrower", "part_of": "has_part", "prerequisite_for": "requires",
    "supports": "supported_by", "contradicts": "contradicts", "qualifies": "qualified_by",
    "derived_from": "gave_rise_to", "answers": "answered_by", "about": "discussed_in",
    "introduced_in": "introduces", "authored_by": "authored", "affiliated_with": "has_affiliate",
    "supersedes": "superseded_by", "applies_to": "applied_by", "contains": "contained_in",
}
CONCEPT_SECTIONS = ["Knowledge", "Evidence", "Understanding", "Application", "Uncertainty", "Related"]
STALE_DAYS = 90
