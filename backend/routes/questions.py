"""试题相关API路由"""
from fastapi import APIRouter, HTTPException
from typing import List
from models import Question, QuestionCreate, QuestionUpdate
from database import get_all_questions, get_question_by_id, create_question, update_question, delete_question
from database import create_node, update_node, delete_node

router = APIRouter(prefix="/api/questions", tags=["试题管理"])


@router.get("", response_model=List[Question])
async def list_questions():
    """查询试题列表"""
    return get_all_questions()


@router.get("/{question_id}", response_model=Question)
async def get_question(question_id: str):
    """查询试题详情"""
    question = get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="试题不存在")
    return question


@router.post("", response_model=Question, status_code=201)
async def add_question(question: QuestionCreate):
    """新增试题（同时创建图谱节点）"""
    data = question.model_dump()
    result = create_question(data)
    create_node({
        "id": result["id"],
        "name": data.get("name", data["title"]),
        "type": "问题",
        "layer": "问题层",
        "chapter": data.get("chapter", "传输层"),
        "description": data.get("description", ""),
        "keywords": data.get("keywords", []),
        "difficulty": data.get("difficulty", 1),
    })
    return result


@router.put("/{question_id}", response_model=Question)
async def edit_question(question_id: str, question: QuestionUpdate):
    """修改试题（同步更新图谱节点）"""
    updated = update_question(question_id, question.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="试题不存在")
    update_node(question_id, {
        "name": updated.get("name"),
        "chapter": updated.get("chapter"),
        "description": updated.get("description"),
        "keywords": updated.get("keywords", []),
        "difficulty": updated.get("difficulty"),
    })
    return updated


@router.delete("/{question_id}")
async def remove_question(question_id: str):
    """删除试题（同时删除图谱节点）"""
    if not delete_question(question_id):
        raise HTTPException(status_code=404, detail="试题不存在")
    delete_node(question_id)
    return {"message": "删除成功"}
