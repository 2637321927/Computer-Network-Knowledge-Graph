"""关系相关API路由"""
from fastapi import APIRouter, HTTPException
from typing import List
from models import Edge, EdgeCreate, EdgeUpdate
from database import get_all_edges, create_edge, update_edge, delete_edge

router = APIRouter(prefix="/api/edges", tags=["关系管理"])


@router.get("", response_model=List[Edge])
async def list_edges():
    """查询关系列表"""
    return get_all_edges()


@router.post("", response_model=Edge, status_code=201)
async def add_edge(edge: EdgeCreate):
    """新增关系"""
    return create_edge(edge.model_dump())


@router.put("/{edge_id}", response_model=Edge)
async def edit_edge(edge_id: str, edge: EdgeUpdate):
    """修改关系"""
    updated = update_edge(edge_id, edge.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="关系不存在")
    return updated


@router.delete("/{edge_id}")
async def remove_edge(edge_id: str):
    """删除关系"""
    if not delete_edge(edge_id):
        raise HTTPException(status_code=404, detail="关系不存在")
    return {"message": "删除成功"}
