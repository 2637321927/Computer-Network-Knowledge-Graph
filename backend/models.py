"""
数据模型定义 - 知识图谱的三层结构：概念层、案例层、问题层
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# 枚举定义

class NodeType(str, Enum):
    CONCEPT = "概念"       # 概念层
    CASE = "案例"          # 案例层
    PROBLEM = "问题"       # 问题层
    PROTOCOL = "协议"
    ALGORITHM = "算法"
    PRINCIPLE = "原理"
    TECHNOLOGY = "技术"
    DEVICE = "设备"
    SERVICE = "服务"


class RelationType(str, Enum):
    CONTAINS = "包含"
    PREREQUISITE = "前置知识"
    BELONGS_TO = "属于层"
    RELATED_CASE = "相关案例"
    RELATED_QUESTION = "关联试题"
    APPLIED_TO = "应用于"
    COMPARE = "对比"
    DEPENDS = "依赖"


class Chapter(str, Enum):
    CH1 = "计算机网络概述"
    CH2 = "物理层"
    CH3 = "数据链路层"
    CH4 = "局域网原理"
    CH5 = "网络层"
    CH6 = "传输层"
    CH7 = "应用层"
    CH8 = "网络性能优化"
    CH9 = "软件定义网络与边缘计算"
    CH10 = "课程综合项目"


class Layer(str, Enum):
    CONCEPT_LAYER = "概念层"
    CASE_LAYER = "案例层"
    PROBLEM_LAYER = "问题层"


# 节点模型

class NodeBase(BaseModel):
    name: str = Field(..., description="知识点名称")
    type: NodeType = Field(..., description="节点类型")
    layer: Layer = Field(..., description="所属层次（概念层/案例层/问题层）")
    chapter: Chapter = Field(..., description="所属章节")
    description: str = Field("", description="详细描述")
    keywords: List[str] = Field(default_factory=list, description="关键词列表")
    difficulty: int = Field(1, ge=1, le=5, description="难度等级 1-5")
    image_urls: List[str] = Field(default_factory=list, description="配图URL列表（可多张）")
    video_url: Optional[str] = Field(None, description="视频URL（支持B站/YouTube等）")


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[NodeType] = None
    layer: Optional[Layer] = None
    chapter: Optional[Chapter] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    difficulty: Optional[int] = None
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None


class Node(NodeBase):
    id: str = Field(..., description="节点唯一标识")
    
    class Config:
        from_attributes = True


# 关系模型

class EdgeBase(BaseModel):
    source: str = Field(..., description="源节点ID")
    target: str = Field(..., description="目标节点ID")
    relation: RelationType = Field(..., description="关系类型")
    description: str = Field("", description="关系描述")


class EdgeCreate(EdgeBase):
    pass


class EdgeUpdate(BaseModel):
    source: Optional[str] = None
    target: Optional[str] = None
    relation: Optional[RelationType] = None
    description: Optional[str] = None


class Edge(EdgeBase):
    id: str = Field(..., description="关系唯一标识")
    
    class Config:
        from_attributes = True


# 案例模型

class CaseBase(BaseModel):
    title: str = Field(..., description="案例标题")
    description: str = Field(..., description="案例描述")
    chapter: Chapter = Field(Chapter.CH6, description="所属章节")
    difficulty: int = Field(1, ge=1, le=5, description="难度等级 1-5")
    related_nodes: List[str] = Field(default_factory=list, description="关联知识点ID列表")
    background: str = Field("", description="案例背景")
    steps: List[str] = Field(default_factory=list, description="案例实施步骤")
    analysis: str = Field("", description="案例分析与结论")
    content: str = Field("", description="案例详细内容")
    tags: List[str] = Field(default_factory=list, description="标签")
    image_urls: List[str] = Field(default_factory=list, description="配图URL列表")
    video_url: Optional[str] = Field(None, description="视频URL")


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    chapter: Optional[Chapter] = None
    difficulty: Optional[int] = None
    related_nodes: Optional[List[str]] = None
    background: Optional[str] = None
    steps: Optional[List[str]] = None
    analysis: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None


class Case(CaseBase):
    id: str = Field(..., description="案例唯一标识")
    
    class Config:
        from_attributes = True


# 试题模型

class QuestionType(str, Enum):
    SINGLE_CHOICE = "单选题"
    MULTI_CHOICE = "多选题"
    TRUE_FALSE = "判断题"
    FILL_BLANK = "填空题"
    SHORT_ANSWER = "简答题"
    CALCULATION = "计算题"


class QuestionBase(BaseModel):
    name: str = Field("", description="题目名称（在图中显示）")
    title: str = Field(..., description="题目标题/题干")
    question: str = Field("", description="兼容独立题库的题干字段")
    type: QuestionType = Field(..., description="题型")
    chapter: Chapter = Field(Chapter.CH6, description="所属章节")
    description: str = Field("", description="题目描述")
    keywords: List[str] = Field(default_factory=list, description="关键词列表")
    related_nodes: List[str] = Field(default_factory=list, description="关联知识点ID列表")
    knowledge_point_id: Optional[str] = Field(None, description="主要关联知识点ID")
    options: List[str] = Field(default_factory=list, description="选项列表")
    answer: str = Field("", description="参考答案")
    explanation: str = Field("", description="解析")
    analysis: str = Field("", description="兼容独立题库的解析字段")
    difficulty: int = Field(1, ge=1, le=5, description="难度等级 1-5")
    difficulty_label: Optional[str] = Field(None, description="难度中文分级：易/中/难")


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    question: Optional[str] = None
    type: Optional[QuestionType] = None
    chapter: Optional[Chapter] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    related_nodes: Optional[List[str]] = None
    knowledge_point_id: Optional[str] = None
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    analysis: Optional[str] = None
    difficulty: Optional[int] = None
    difficulty_label: Optional[str] = None


class Question(QuestionBase):
    id: str = Field(..., description="试题唯一标识")
    
    class Config:
        from_attributes = True


# 图谱统计

class GraphStats(BaseModel):
    total_nodes: int
    total_edges: int
    total_cases: int
    total_questions: int
    nodes_by_layer: dict
    nodes_by_chapter: dict
    edges_by_relation: dict
