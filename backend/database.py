"""
JSON 文件数据库操作层
提供节点、关系、案例、试题的增删改查
"""
import json
import os
import uuid
from typing import List, Optional, Dict, Any
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# 数据文件路径
NODES_FILE = DATA_DIR / "nodes.json"
EDGES_FILE = DATA_DIR / "edges.json"
CASES_FILE = DATA_DIR / "cases.json"
QUESTIONS_FILE = DATA_DIR / "questions.json"


def _ensure_files():
    """确保数据文件存在"""
    DATA_DIR.mkdir(exist_ok=True)
    for file in [NODES_FILE, EDGES_FILE, CASES_FILE, QUESTIONS_FILE]:
        if not file.exists():
            with open(file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False)


def _read_json(filepath: Path) -> List[Dict]:
    """读取 JSON 文件"""
    _ensure_files()
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(filepath: Path, data: List[Dict]):
    """写入 JSON 文件"""
    _ensure_files()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _generate_id() -> str:
    return str(uuid.uuid4())[:8]


# 节点操作

def get_all_nodes() -> List[Dict]:
    return _read_json(NODES_FILE)


def get_node_by_id(node_id: str) -> Optional[Dict]:
    nodes = _read_json(NODES_FILE)
    for node in nodes:
        if node["id"] == node_id:
            return node
    return None


def search_nodes(keyword: str = None, chapter: str = None, 
                 node_type: str = None, layer: str = None) -> List[Dict]:
    nodes = _read_json(NODES_FILE)
    result = nodes
    
    if keyword:
        keyword_lower = keyword.lower()
        result = [
            n for n in result
            if keyword_lower in n.get("name", "").lower()
            or any(keyword_lower in kw.lower() for kw in n.get("keywords", []))
            or keyword_lower in n.get("description", "").lower()
        ]
    
    if chapter:
        result = [n for n in result if n.get("chapter") == chapter]
    
    if node_type:
        result = [n for n in result if n.get("type") == node_type]
    
    if layer:
        result = [n for n in result if n.get("layer") == layer]
    
    return result


def create_node(node_data: Dict) -> Dict:
    nodes = _read_json(NODES_FILE)
    node_data["id"] = _generate_id()
    nodes.append(node_data)
    _write_json(NODES_FILE, nodes)
    return node_data


def update_node(node_id: str, update_data: Dict) -> Optional[Dict]:
    nodes = _read_json(NODES_FILE)
    for i, node in enumerate(nodes):
        if node["id"] == node_id:
            for key, value in update_data.items():
                if value is not None:
                    nodes[i][key] = value
            _write_json(NODES_FILE, nodes)
            return nodes[i]
    return None


def delete_node(node_id: str) -> bool:
    nodes = _read_json(NODES_FILE)
    edges = _read_json(EDGES_FILE)
    new_nodes = [n for n in nodes if n["id"] != node_id]
    if len(new_nodes) == len(nodes):
        return False
    # 同时删除与该节点相关的所有关系
    new_edges = [e for e in edges if e["source"] != node_id and e["target"] != node_id]
    _write_json(NODES_FILE, new_nodes)
    _write_json(EDGES_FILE, new_edges)
    return True


def get_node_neighbors(node_id: str) -> Dict:
    """获取节点的相邻节点和关系"""
    nodes = _read_json(NODES_FILE)
    edges = _read_json(EDGES_FILE)
    
    neighbor_ids = set()
    related_edges = []
    for edge in edges:
        if edge["source"] == node_id:
            neighbor_ids.add(edge["target"])
            related_edges.append(edge)
        elif edge["target"] == node_id:
            neighbor_ids.add(edge["source"])
            related_edges.append(edge)
    
    neighbors = [n for n in nodes if n["id"] in neighbor_ids]
    return {
        "node": next((n for n in nodes if n["id"] == node_id), None),
        "neighbors": neighbors,
        "edges": related_edges
    }


# 关系操作

def get_all_edges() -> List[Dict]:
    return _read_json(EDGES_FILE)


def create_edge(edge_data: Dict) -> Dict:
    edges = _read_json(EDGES_FILE)
    edge_data["id"] = f"edge_{_generate_id()}"
    edges.append(edge_data)
    _write_json(EDGES_FILE, edges)
    return edge_data


def update_edge(edge_id: str, update_data: Dict) -> Optional[Dict]:
    edges = _read_json(EDGES_FILE)
    for i, edge in enumerate(edges):
        if edge["id"] == edge_id:
            for key, value in update_data.items():
                if value is not None:
                    edges[i][key] = value
            _write_json(EDGES_FILE, edges)
            return edges[i]
    return None


def delete_edge(edge_id: str) -> bool:
    edges = _read_json(EDGES_FILE)
    new_edges = [e for e in edges if e["id"] != edge_id]
    if len(new_edges) == len(edges):
        return False
    _write_json(EDGES_FILE, new_edges)
    return True


# 案例操作

def get_all_cases() -> List[Dict]:
    return _read_json(CASES_FILE)


def get_case_by_id(case_id: str) -> Optional[Dict]:
    cases = _read_json(CASES_FILE)
    for case in cases:
        if case["id"] == case_id:
            return case
    return None


def create_case(case_data: Dict) -> Dict:
    cases = _read_json(CASES_FILE)
    case_data["id"] = f"case_{_generate_id()}"
    cases.append(case_data)
    _write_json(CASES_FILE, cases)
    return case_data


def update_case(case_id: str, update_data: Dict) -> Optional[Dict]:
    cases = _read_json(CASES_FILE)
    for i, case in enumerate(cases):
        if case["id"] == case_id:
            for key, value in update_data.items():
                if value is not None:
                    cases[i][key] = value
            _write_json(CASES_FILE, cases)
            return cases[i]
    return None


def delete_case(case_id: str) -> bool:
    cases = _read_json(CASES_FILE)
    new_cases = [c for c in cases if c["id"] != case_id]
    if len(new_cases) == len(cases):
        return False
    _write_json(CASES_FILE, new_cases)
    return True


# 试题操作

def get_all_questions() -> List[Dict]:
    return _read_json(QUESTIONS_FILE)


def get_question_by_id(question_id: str) -> Optional[Dict]:
    questions = _read_json(QUESTIONS_FILE)
    for q in questions:
        if q["id"] == question_id:
            return q
    return None


def create_question(question_data: Dict) -> Dict:
    questions = _read_json(QUESTIONS_FILE)
    question_data["id"] = f"q_{_generate_id()}"
    questions.append(question_data)
    _write_json(QUESTIONS_FILE, questions)
    return question_data


def update_question(question_id: str, update_data: Dict) -> Optional[Dict]:
    questions = _read_json(QUESTIONS_FILE)
    for i, q in enumerate(questions):
        if q["id"] == question_id:
            for key, value in update_data.items():
                if value is not None:
                    questions[i][key] = value
            _write_json(QUESTIONS_FILE, questions)
            return questions[i]
    return None


def delete_question(question_id: str) -> bool:
    questions = _read_json(QUESTIONS_FILE)
    new_questions = [q for q in questions if q["id"] != question_id]
    if len(new_questions) == len(questions):
        return False
    _write_json(QUESTIONS_FILE, new_questions)
    return True


# 图谱统计

def get_graph_stats() -> Dict:
    nodes = _read_json(NODES_FILE)
    edges = _read_json(EDGES_FILE)
    cases = _read_json(CASES_FILE)
    questions = _read_json(QUESTIONS_FILE)
    
    nodes_by_layer = {}
    for n in nodes:
        layer = n.get("layer", "未知")
        nodes_by_layer[layer] = nodes_by_layer.get(layer, 0) + 1
    
    nodes_by_chapter = {}
    for n in nodes:
        chapter = n.get("chapter", "未知")
        nodes_by_chapter[chapter] = nodes_by_chapter.get(chapter, 0) + 1
    
    edges_by_relation = {}
    for e in edges:
        rel = e.get("relation", "未知")
        edges_by_relation[rel] = edges_by_relation.get(rel, 0) + 1
    
    return {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "total_cases": len(cases),
        "total_questions": len(questions),
        "nodes_by_layer": nodes_by_layer,
        "nodes_by_chapter": nodes_by_chapter,
        "edges_by_relation": edges_by_relation
    }
