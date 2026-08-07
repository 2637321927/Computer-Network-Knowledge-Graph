"""执行课程知识图谱最终交付的数据与文件验收。"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DATA = ROOT / "backend" / "data"
CORE_DATA = ROOT / "data" / "core"


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


nodes = load(BACKEND_DATA / "nodes.json")
edges = load(BACKEND_DATA / "edges.json")
questions = load(BACKEND_DATA / "questions.json")
cases = load(BACKEND_DATA / "cases.json")

node_ids = {node["id"] for node in nodes}
edge_ids = {edge["id"] for edge in edges}
question_ids = {question["id"] for question in questions}
case_ids = {case["id"] for case in cases}
concepts = [node for node in nodes if node.get("layer") == "概念层"]
concept_ids = {node["id"] for node in concepts}

assert len(node_ids) == len(nodes), "节点ID不唯一"
assert len(edge_ids) == len(edges), "关系ID不唯一"
assert len(question_ids) == len(questions), "试题ID不唯一"
assert len(case_ids) == len(cases), "案例ID不唯一"

required_relations = {
    "包含",
    "前置知识",
    "属于层",
    "相关案例",
    "关联试题",
    "应用于",
    "对比",
    "依赖",
}
assert set(edge["relation"] for edge in edges) == required_relations, "关系类型不完整"
assert all(
    edge["source"] in node_ids and edge["target"] in node_ids for edge in edges
), "存在悬空关系"

required_question_fields = {
    "id",
    "question",
    "answer",
    "analysis",
    "knowledge_point_id",
    "difficulty",
}
assert all(required_question_fields <= question.keys() for question in questions)
assert all(question["knowledge_point_id"] in concept_ids for question in questions)
assert all(
    related in concept_ids
    for question in questions
    for related in question.get("related_nodes", [])
)
assert all(
    bool(question.get("options"))
    for question in questions
    if question.get("type") in {"单选题", "多选题"}
)

required_case_fields = {
    "id",
    "title",
    "description",
    "background",
    "steps",
    "related_nodes",
    "analysis",
}
assert all(required_case_fields <= case.keys() for case in cases)
assert all(
    related in concept_ids for case in cases for related in case.get("related_nodes", [])
)

associated: dict[str, set[str]] = defaultdict(set)
for question in questions:
    associated[question["knowledge_point_id"]].add(question["id"])
    for related in question.get("related_nodes", []):
        associated[related].add(question["id"])
for edge in edges:
    if edge["relation"] == "关联试题" and edge["target"] in question_ids:
        associated[edge["source"]].add(edge["target"])

assert len(concepts) >= 200
assert len(questions) >= 600
assert len(cases) >= 20
assert all(len(associated[node_id]) >= 3 for node_id in concept_ids)

core_node_files = (
    "network_layer_nodes.json",
    "transport_layer_nodes.json",
    "application_layer_nodes.json",
)
core_nodes = sum((load(CORE_DATA / filename) for filename in core_node_files), [])
core_edges = load(CORE_DATA / "core_layer_edges.json")
core_questions = load(CORE_DATA / "core_questions.json")
core_cases = load(CORE_DATA / "core_cases.json")
assert len(core_nodes) == 81
assert Counter(node["chapter"] for node in core_nodes) == {
    "网络层": 27,
    "传输层": 27,
    "应用层": 27,
}
assert len(core_edges) == 437
assert len(core_questions) == 243
assert len(core_cases) == 8

required_files = (
    "README.md",
    "docs/project-report.md",
    "docs/acceptance-checklist.md",
    "docs/courseware/core-courseware.md",
    "docs/experiments/core-experiment-guide.md",
    "docs/resources/core-resource-catalog.md",
    "docs/progress/weekly-report-01.md",
    "docs/progress/weekly-report-02.md",
    "docs/demo/screenshots/01-graph-overview.png",
    "docs/demo/screenshots/02-core-layer-filter.png",
    "docs/demo/screenshots/03-node-detail.png",
    "docs/demo/screenshots/04-management.png",
    "docs/demo/screenshots/05-node-cases.png",
)
assert all((ROOT / path).is_file() and (ROOT / path).stat().st_size > 0 for path in required_files)

print(
    json.dumps(
        {
            "concept_nodes": len(concepts),
            "questions": len(questions),
            "cases": len(cases),
            "edges": len(edges),
            "minimum_questions_per_concept": min(
                len(associated[node_id]) for node_id in concept_ids
            ),
            "core": {
                "nodes": len(core_nodes),
                "questions": len(core_questions),
                "cases": len(core_cases),
                "edges": len(core_edges),
            },
            "delivery_files": len(required_files),
        },
        ensure_ascii=False,
        indent=2,
    )
)
