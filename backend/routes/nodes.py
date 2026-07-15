"""节点相关API路由"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models import Node, NodeCreate, NodeUpdate
from database import (
    get_all_nodes, get_node_by_id, search_nodes,
    create_node, update_node, delete_node, get_node_neighbors
)

router = APIRouter(prefix="/api/nodes", tags=["节点管理"])


@router.get("", response_model=List[Node])
async def list_nodes(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    chapter: Optional[str] = Query(None, description="按章节筛选"),
    node_type: Optional[str] = Query(None, description="按节点类型筛选"),
    layer: Optional[str] = Query(None, description="按层次筛选（概念层/案例层/问题层）")
):
    """查询知识点列表，支持搜索和筛选"""
    return search_nodes(keyword=keyword, chapter=chapter, node_type=node_type, layer=layer)


@router.get("/{node_id}", response_model=Node)
async def get_node(node_id: str):
    """查询知识点详情"""
    node = get_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return node


@router.post("", response_model=Node, status_code=201)
async def add_node(node: NodeCreate):
    """新增知识点"""
    return create_node(node.model_dump())


@router.put("/{node_id}", response_model=Node)
async def edit_node(node_id: str, node: NodeUpdate):
    """修改知识点"""
    updated = update_node(node_id, node.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return updated


@router.delete("/{node_id}")
async def remove_node(node_id: str):
    """删除知识点（同时删除关联关系）"""
    if not delete_node(node_id):
        raise HTTPException(status_code=404, detail="知识点不存在")
    return {"message": "删除成功"}


@router.get("/{node_id}/neighbors")
async def get_neighbors(node_id: str):
    """查询某个知识点的相邻节点"""
    result = get_node_neighbors(node_id)
    if not result["node"]:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return result
