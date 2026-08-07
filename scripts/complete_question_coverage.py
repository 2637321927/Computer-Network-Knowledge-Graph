"""补齐全项目试题关联字段，并保证每个概念知识点至少关联三道题。"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "backend" / "data"
NODES_FILE = DATA_DIR / "nodes.json"
EDGES_FILE = DATA_DIR / "edges.json"
QUESTIONS_FILE = DATA_DIR / "questions.json"
CASES_FILE = DATA_DIR / "cases.json"


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, records: list[dict]) -> None:
    path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


nodes = load(NODES_FILE)
edges = load(EDGES_FILE)
questions = load(QUESTIONS_FILE)
cases = load(CASES_FILE)

legacy_id_map = {
    "congestion_control": "core_ch6_congestion",
    "tcp_handshake": "core_ch6_handshake",
    "tcp_wavehand": "core_ch6_connection_release",
    "core_ch6_wavehand": "core_ch6_connection_release",
    "tcp_header": "core_ch6_tcp_header",
    "case_tcp_congestion": "core_case_tcp_congestion",
    "case_tcp_wireshark": "core_case_tcp_lifecycle",
}
for edge in edges:
    edge["source"] = legacy_id_map.get(edge["source"], edge["source"])
    edge["target"] = legacy_id_map.get(edge["target"], edge["target"])

concepts = [node for node in nodes if node.get("layer") == "概念层"]
concept_by_id = {node["id"]: node for node in concepts}
question_by_id = {question["id"]: question for question in questions}

# 旧数据中的问题层节点已经通过“关联试题”边连接概念，但部分题目缺少
# knowledge_point_id/related_nodes。先从图谱边恢复这些字段，使关联 API 可查询。
edge_links: dict[str, list[str]] = defaultdict(list)
for edge in edges:
    if edge.get("relation") != "关联试题":
        continue
    if edge.get("source") in concept_by_id and edge.get("target") in question_by_id:
        edge_links[edge["target"]].append(edge["source"])

for question in questions:
    linked = list(dict.fromkeys(edge_links.get(question["id"], [])))
    existing = question.get("related_nodes") or []
    related = list(dict.fromkeys([*existing, *linked]))
    if related:
        question["related_nodes"] = related
        question.setdefault("knowledge_point_id", related[0])

    question.setdefault("name", question.get("title", "试题"))
    question.setdefault("question", question.get("title", ""))
    question.setdefault("description", question.get("explanation", ""))
    question.setdefault("keywords", [])
    question.setdefault("options", [])
    question.setdefault("explanation", question.get("analysis", ""))
    question.setdefault("analysis", question.get("explanation", ""))
    if not question.get("answer") and question.get("explanation"):
        question["answer"] = question["explanation"]
    difficulty = int(question.get("difficulty", 1))
    question.setdefault(
        "difficulty_label",
        "易" if difficulty <= 1 else "中" if difficulty <= 2 else "难",
    )

for case in cases:
    description = case.get("description") or case.get("content", "")[:240]
    case.setdefault("background", description)
    case.setdefault(
        "steps",
        [
            "阅读案例背景并整理网络拓扑、协议和参数",
            "依据案例条件完成抓包、计算、仿真或配置分析",
            "记录关键结果并解释现象产生的网络原理",
        ],
    )
    case.setdefault("analysis", description)


def associations() -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for question in questions:
        related = set(question.get("related_nodes") or [])
        primary = question.get("knowledge_point_id")
        if primary:
            related.add(primary)
        for node_id in related:
            if node_id in concept_by_id:
                result[node_id].add(question["id"])
    return result


associated = associations()
node_ids = {node["id"] for node in nodes}
edge_ids = {edge["id"] for edge in edges}
question_ids = {question["id"] for question in questions}
new_questions: list[dict] = []

for concept in concepts:
    node_id = concept["id"]
    current = len(associated[node_id])
    if current >= 3:
        continue

    peers = [
        node
        for node in concepts
        if node["chapter"] == concept["chapter"] and node["id"] != node_id
    ]
    for slot in range(current + 1, 4):
        question_id = f"project_q_{node_id}_{slot:02d}"
        if question_id in question_ids or question_id in node_ids:
            continue

        description = concept["description"].strip()
        keywords = list(dict.fromkeys([*concept.get("keywords", []), concept["name"]]))[:6]
        difficulty = slot
        difficulty_label = ("易", "中", "难")[slot - 1]

        if slot == 1:
            distractors = [peer["description"].strip() for peer in peers[:3]]
            while len(distractors) < 3:
                distractors.append("该说法描述的是其他网络机制，与本知识点不符。")
            title = f"下列关于“{concept['name']}”的描述，正确的是哪一项？"
            options = [
                f"A. {description}",
                f"B. {distractors[0]}",
                f"C. {distractors[1]}",
                f"D. {distractors[2]}",
            ]
            answer = "A"
            analysis = f"A项准确说明了{concept['name']}的核心含义：{description}"
            question_type = "单选题"
        elif slot == 2:
            title = f"“{description}”描述的知识点是________。"
            options = []
            answer = concept["name"]
            analysis = f"题干给出的定义对应{concept['name']}。"
            question_type = "填空题"
        else:
            title = f"简述“{concept['name']}”的核心作用或工作机制。"
            options = []
            answer = description
            analysis = (
                f"作答应说明{concept['name']}的目标、关键机制及其在"
                f"{concept['chapter']}中的作用。参考要点：{description}"
            )
            question_type = "简答题"

        question = {
            "id": question_id,
            "name": f"{concept['name']}·{question_type}",
            "title": title,
            "question": title,
            "type": question_type,
            "chapter": concept["chapter"],
            "description": f"{concept['name']}关联{question_type}。",
            "keywords": keywords,
            "knowledge_point_id": node_id,
            "related_nodes": [node_id],
            "options": options,
            "answer": answer,
            "explanation": analysis,
            "analysis": analysis,
            "difficulty": difficulty,
            "difficulty_label": difficulty_label,
        }
        questions.append(question)
        new_questions.append(question)
        question_ids.add(question_id)
        associated[node_id].add(question_id)

        nodes.append(
            {
                "id": question_id,
                "name": question["name"],
                "type": "问题",
                "layer": "问题层",
                "chapter": concept["chapter"],
                "description": title,
                "keywords": keywords,
                "difficulty": difficulty,
                "image_urls": [],
                "video_url": None,
            }
        )
        node_ids.add(question_id)

        edge_id = f"edge_project_{node_id}_{slot:02d}"
        if edge_id not in edge_ids:
            edges.append(
                {
                    "id": edge_id,
                    "source": node_id,
                    "target": question_id,
                    "relation": "关联试题",
                    "description": f"{concept['name']}关联试题：{title}",
                }
            )
            edge_ids.add(edge_id)

coverage = associations()
for question in new_questions:
    coverage[question["knowledge_point_id"]].add(question["id"])

assert len({node["id"] for node in nodes}) == len(nodes), "节点 ID 重复"
assert len({edge["id"] for edge in edges}) == len(edges), "关系 ID 重复"
assert len({question["id"] for question in questions}) == len(questions), "试题 ID 重复"
assert len(questions) >= 600, "试题总量未达到 600"
assert all(len(coverage[node["id"]]) >= 3 for node in concepts), "存在试题不足三道的知识点"

save(NODES_FILE, nodes)
save(EDGES_FILE, edges)
save(QUESTIONS_FILE, questions)
save(CASES_FILE, cases)

print(f"补充试题：{len(new_questions)}")
print(f"试题总数：{len(questions)}")
print(f"概念知识点：{len(concepts)}，每个知识点至少关联 3 道试题")
