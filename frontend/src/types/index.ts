// 枚举

export type NodeType = '概念' | '案例' | '问题' | '协议' | '算法' | '原理' | '技术';

export type RelationType = '包含' | '前置知识' | '属于层' | '相关案例' | '关联试题' | '应用于' | '对比' | '依赖';

export type Layer = '概念层' | '案例层' | '问题层';

export type Chapter =
  | '计算机网络概述'
  | '物理层'
  | '数据链路层'
  | '局域网原理'
  | '网络层'
  | '传输层'
  | '应用层'
  | '网络性能优化'
  | '软件定义网络与边缘计算'
  | '课程综合项目';

export type QuestionType = '单选题' | '多选题' | '判断题' | '填空题' | '简答题' | '计算题';

// 节点

export interface KnowledgeNode {
  id: string;
  name: string;
  type: NodeType;
  layer: Layer;
  chapter: Chapter;
  description: string;
  keywords: string[];
  difficulty: number;
  image_urls?: string[];
  video_url?: string;
}

export interface NodeCreate {
  name: string;
  type: NodeType;
  layer: Layer;
  chapter: Chapter;
  description: string;
  keywords: string[];
  difficulty: number;
  image_urls?: string[];
  video_url?: string;
}

// 关系

export interface Edge {
  id: string;
  source: string;
  target: string;
  relation: RelationType;
  description: string;
}

export interface EdgeCreate {
  source: string;
  target: string;
  relation: RelationType;
  description: string;
}

// 案例

export interface CaseItem {
  id: string;
  title: string;
  description: string;
  chapter: Chapter;
  difficulty: number;
  related_nodes: string[];
  content: string;
  tags: string[];
  image_urls?: string[];
  video_url?: string;
}

// 试题

export interface QuestionItem {
  id: string;
  name: string;
  title: string;
  type: QuestionType;
  chapter: Chapter;
  description: string;
  keywords: string[];
  related_nodes: string[];
  options: string[];
  answer: string;
  explanation: string;
  difficulty: number;
}

// 图谱

export interface GraphData {
  nodes: KnowledgeNode[];
  edges: Edge[];
}

export interface NeighborData {
  node: KnowledgeNode | null;
  neighbors: KnowledgeNode[];
  edges: Edge[];
}

export interface GraphStats {
  total_nodes: number;
  total_edges: number;
  total_cases: number;
  total_questions: number;
  nodes_by_layer: Record<string, number>;
  nodes_by_chapter: Record<string, number>;
  edges_by_relation: Record<string, number>;
}

// 筛选条件

export interface FilterParams {
  keyword?: string;
  chapter?: Chapter;
  node_type?: NodeType;
  layer?: Layer;
}
