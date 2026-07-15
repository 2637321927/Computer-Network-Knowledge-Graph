import axios from 'axios';
import type {
  KnowledgeNode, NodeCreate,
  Edge, EdgeCreate,
  CaseItem,
  QuestionItem,
  GraphData, NeighborData, GraphStats,
  FilterParams
} from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// 节点 API

export async function fetchNodes(params?: FilterParams): Promise<KnowledgeNode[]> {
  const { data } = await api.get('/nodes', { params });
  return data;
}

export async function fetchNodeById(id: string): Promise<KnowledgeNode> {
  const { data } = await api.get(`/nodes/${id}`);
  return data;
}

export async function createNode(node: NodeCreate): Promise<KnowledgeNode> {
  const { data } = await api.post('/nodes', node);
  return data;
}

export async function updateNode(id: string, node: Partial<NodeCreate>): Promise<KnowledgeNode> {
  const { data } = await api.put(`/nodes/${id}`, node);
  return data;
}

export async function deleteNode(id: string): Promise<void> {
  await api.delete(`/nodes/${id}`);
}

export async function fetchNeighbors(id: string): Promise<NeighborData> {
  const { data } = await api.get(`/nodes/${id}/neighbors`);
  return data;
}

// 关系 API

export async function fetchEdges(): Promise<Edge[]> {
  const { data } = await api.get('/edges');
  return data;
}

export async function createEdge(edge: EdgeCreate): Promise<Edge> {
  const { data } = await api.post('/edges', edge);
  return data;
}

export async function updateEdge(id: string, edge: Partial<EdgeCreate>): Promise<Edge> {
  const { data } = await api.put(`/edges/${id}`, edge);
  return data;
}

export async function deleteEdge(id: string): Promise<void> {
  await api.delete(`/edges/${id}`);
}

// 案例 API

export async function fetchCases(): Promise<CaseItem[]> {
  const { data } = await api.get('/cases');
  return data;
}

export async function fetchCaseById(id: string): Promise<CaseItem> {
  const { data } = await api.get(`/cases/${id}`);
  return data;
}

// 试题 API

export async function fetchQuestions(): Promise<QuestionItem[]> {
  const { data } = await api.get('/questions');
  return data;
}

export async function fetchQuestionById(id: string): Promise<QuestionItem> {
  const { data } = await api.get(`/questions/${id}`);
  return data;
}

// 图谱 API

export async function fetchGraph(params?: { chapter?: string; layer?: string }): Promise<GraphData> {
  const { data } = await api.get('/graph', { params });
  return data;
}

export async function fetchGraphStats(): Promise<GraphStats> {
  const { data } = await api.get('/graph/stats');
  return data;
}

// 导入导出

export async function exportData(): Promise<{
  nodes: KnowledgeNode[];
  edges: Edge[];
  cases: CaseItem[];
  questions: QuestionItem[];
}> {
  const { data } = await api.get('/export');
  return data;
}

export async function importData(payload: {
  nodes?: KnowledgeNode[];
  edges?: Edge[];
  cases?: CaseItem[];
  questions?: QuestionItem[];
}): Promise<{ message: string; stats: Record<string, number> }> {
  const { data } = await api.post('/import', payload);
  return data;
}
