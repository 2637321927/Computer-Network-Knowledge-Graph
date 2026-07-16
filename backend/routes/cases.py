"""案例相关API路由"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models import Case, CaseCreate, CaseUpdate
from database import get_all_cases, get_case_by_id, create_case, update_case, delete_case, search_cases
from database import create_node, update_node, delete_node

router = APIRouter(prefix="/api/cases", tags=["案例管理"])


@router.get("", response_model=List[Case])
async def list_cases(
    chapter: Optional[str] = Query(None, description="按章节筛选")
):
    """查询案例列表，支持按章节筛选"""
    return search_cases(chapter=chapter)


@router.get("/{case_id}", response_model=Case)
async def get_case(case_id: str):
    """查询案例详情"""
    case = get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    return case


@router.post("", response_model=Case, status_code=201)
async def add_case(case: CaseCreate):
    """新增案例（同时创建图谱节点）"""
    data = case.model_dump()
    result = create_case(data)
    # 自动在图谱中创建对应节点
    create_node({
        "id": result["id"],
        "name": data["title"],
        "type": "案例",
        "layer": "案例层",
        "chapter": data.get("chapter", "传输层"),
        "description": data.get("description", ""),
        "keywords": data.get("tags", []),
        "difficulty": data.get("difficulty", 1),
        "image_urls": data.get("image_urls", []),
        "video_url": data.get("video_url"),
    })
    return result


@router.put("/{case_id}", response_model=Case)
async def edit_case(case_id: str, case: CaseUpdate):
    """修改案例（同步更新图谱节点）"""
    updated = update_case(case_id, case.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="案例不存在")
    # 同步更新节点
    update_node(case_id, {
        "name": updated.get("title"),
        "chapter": updated.get("chapter"),
        "description": updated.get("description"),
        "keywords": updated.get("tags", []),
        "difficulty": updated.get("difficulty"),
        "image_urls": updated.get("image_urls"),
        "video_url": updated.get("video_url"),
    })
    return updated


@router.delete("/{case_id}")
async def remove_case(case_id: str):
    """删除案例（同时删除图谱节点）"""
    if not delete_case(case_id):
        raise HTTPException(status_code=404, detail="案例不存在")
    delete_node(case_id)
    return {"message": "删除成功"}
async def remove_case(case_id: str):
    """删除案例"""
    if not delete_case(case_id):
        raise HTTPException(status_code=404, detail="案例不存在")
    return {"message": "删除成功"}
