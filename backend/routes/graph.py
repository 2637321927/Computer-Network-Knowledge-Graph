"""图谱相关API路由"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import (
    get_all_nodes, get_all_edges, get_graph_stats, search_nodes
)

router = APIRouter(prefix="/api/graph", tags=["图谱展示"])


@router.get("")
async def get_full_graph(
    chapter: Optional[str] = Query(None, description="按章节筛选"),
    layer: Optional[str] = Query(None, description="按层次筛选")
):
    """获取完整图谱数据（节点 + 关系），支持筛选"""
    nodes = search_nodes(chapter=chapter, layer=layer)
    all_edges = get_all_edges()
    
    # 筛选相关关系
    node_ids = {n["id"] for n in nodes}
    edges = [e for e in all_edges if e["source"] in node_ids and e["target"] in node_ids]
    
    return {"nodes": nodes, "edges": edges}


@router.get("/stats")
async def get_stats():
    """获取图谱统计信息"""
    return get_graph_stats()


@router.get("/layer/{layer_number}")
async def get_layer_graph(layer_number: int):
    """按课程章号返回第5、6、7章的完整节点与内部关系子图。"""
    chapter_by_layer = {5: "网络层", 6: "传输层", 7: "应用层"}
    chapter = chapter_by_layer.get(layer_number)
    if chapter is None:
        raise HTTPException(status_code=404, detail="核心篇仅包含第5、6、7章")
    nodes = search_nodes(chapter=chapter)
    node_ids = {node["id"] for node in nodes}
    edges = [
        edge for edge in get_all_edges()
        if edge["source"] in node_ids and edge["target"] in node_ids
    ]
    return {"chapter": chapter, "layer_number": layer_number, "nodes": nodes, "edges": edges}
