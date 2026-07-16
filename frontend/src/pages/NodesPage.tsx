import { useEffect, useState } from 'react';
import {
  Table, Button, Space, Modal, Form, Input, Select, Tag, message,
  Popconfirm, Card, InputNumber, Drawer, Typography, Divider
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, ReloadOutlined, EyeOutlined, LinkOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { KnowledgeNode, NodeCreate, Edge, RelationType } from '../types';
import { fetchNodes, createNode, updateNode, deleteNode, fetchEdges, createEdge, deleteEdge } from '../services/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const { Option } = Select;
const { Paragraph, Title } = Typography;

const nodeTypes = ['概念', '案例', '问题', '协议', '算法', '原理', '技术'];
const layers = ['概念层', '案例层', '问题层'];
const chapters = [
  '计算机网络概述', '物理层', '数据链路层', '局域网原理',
  '网络层', '传输层', '应用层', '网络性能优化',
  '软件定义网络与边缘计算', '课程综合项目'
];
const relationTypes: RelationType[] = ['包含', '前置知识', '属于层', '相关案例', '关联试题', '应用于', '对比', '依赖'];

const layerColors: Record<string, string> = {
  '概念层': '#5B8FF9',
  '案例层': '#5AD8A6',
  '问题层': '#F6BD16',
};

const relationColors: Record<string, string> = {
  '包含': '#5B8FF9',
  '前置知识': '#F6BD16',
  '属于层': '#5AD8A6',
  '相关案例': '#FF6B3B',
  '关联试题': '#E8684A',
  '应用于': '#6DC8EC',
  '对比': '#9270CA',
  '依赖': '#FF99C3',
};

export default function NodesPage() {
  const [nodes, setNodes] = useState<KnowledgeNode[]>([]);
  const [allEdges, setAllEdges] = useState<Edge[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingNode, setEditingNode] = useState<KnowledgeNode | null>(null);
  const [form] = Form.useForm();
  const [chapterFilter, setChapterFilter] = useState<string | undefined>(undefined);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 15 });

  // 预览
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewNode, setPreviewNode] = useState<KnowledgeNode | null>(null);
  const [previewEdges, setPreviewEdges] = useState<Edge[]>([]);

  // 关联关系管理
  const [nodeEdges, setNodeEdges] = useState<Edge[]>([]);
  const [newEdgeForm] = Form.useForm();

  const loadNodes = async () => {
    setLoading(true);
    try {
      const data = await fetchNodes({ chapter: chapterFilter as any });
      setNodes(data);
      const edges = await fetchEdges();
      setAllEdges(edges);
    } catch {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadNodes(); }, [chapterFilter]);
  
  // 切换筛选时重置分页
  useEffect(() => { setPagination(prev => ({ ...prev, current: 1 })); }, [chapterFilter]);

  // 加载某节点的关联关系
  const loadNodeEdges = async (nodeId: string) => {
    try {
      const edges = await fetchEdges();
      setNodeEdges(edges.filter(e => e.source === nodeId || e.target === nodeId));
    } catch {
      setNodeEdges([]);
    }
  };

  const handleAdd = () => {
    setEditingNode(null);
    form.resetFields();
    setNodeEdges([]);
    newEdgeForm.resetFields();
    setModalOpen(true);
  };

  const handleEdit = (node: KnowledgeNode) => {
    setEditingNode(node);
    form.setFieldsValue(node);
    loadNodeEdges(node.id);
    newEdgeForm.resetFields();
    setModalOpen(true);
  };

  const handlePreview = (node: KnowledgeNode) => {
    setPreviewNode(node);
    const edges = allEdges.filter(e => e.source === node.id || e.target === node.id);
    setPreviewEdges(edges);
    setPreviewOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteNode(id);
      message.success('删除成功');
      loadNodes();
    } catch {
      message.error('删除失败');
    }
  };

  // 添加关联关系
  const handleAddEdge = async () => {
    try {
      const values = await newEdgeForm.validateFields();
      if (!editingNode) return;
      await createEdge({
        source: editingNode.id,
        target: values.target,
        relation: values.relation,
        description: values.description || '',
      });
      message.success('关联添加成功');
      loadNodeEdges(editingNode.id);
      newEdgeForm.resetFields();
      loadNodes();
    } catch (err: any) {
      if (err.errorFields) return;
      message.error('添加失败');
    }
  };

  // 删除关联关系
  const handleDeleteEdge = async (edgeId: string) => {
    try {
      await deleteEdge(edgeId);
      message.success('关联已删除');
      if (editingNode) loadNodeEdges(editingNode.id);
      loadNodes();
    } catch {
      message.error('删除失败');
    }
  };

  const getNodeName = (id: string) => nodes.find(n => n.id === id)?.name || id;

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        ...values,
        keywords: values.keywords || [],
        image_urls: values.image_urls || [],
      };
      if (editingNode) {
        await updateNode(editingNode.id, payload);
        message.success('更新成功');
      } else {
        await createNode(payload as NodeCreate);
        message.success('创建成功');
      }
      setModalOpen(false);
      loadNodes();
    } catch (err: any) {
      if (err.errorFields) return; // 表单验证错误
      message.error('操作失败');
    }
  };

  const columns: ColumnsType<KnowledgeNode> = [
    { title: 'ID', dataIndex: 'id', width: 100 },
    { title: '名称', dataIndex: 'name', width: 160,
      render: (text, record) => <a onClick={() => handlePreview(record)}>{text}</a>
    },
    { title: '类型', dataIndex: 'type', width: 70,
      render: (t) => <Tag>{t}</Tag>
    },
    {
      title: '层次', dataIndex: 'layer', width: 80,
      render: (l: string) => <Tag color={layerColors[l]}>{l}</Tag>
    },
    { title: '章节', dataIndex: 'chapter', width: 140 },
    {
      title: '难度', dataIndex: 'difficulty', width: 80,
      render: (d: number) => '⭐'.repeat(d)
    },
    {
      title: '关键词', dataIndex: 'keywords', width: 180,
      render: (kw: string[]) => <Space wrap>{kw?.map(k => <Tag key={k}>{k}</Tag>)}</Space>
    },
    {
      title: '操作', key: 'actions', width: 140,
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EyeOutlined />} onClick={() => handlePreview(record)} />
          <Button size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)} />
          <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      )
    },
  ];

  return (
    <>
      <Card
        title="知识点管理"
        extra={
          <Space>
            <Select
              allowClear
              placeholder="按章节筛选"
              style={{ width: 180 }}
              value={chapterFilter}
              onChange={(val) => setChapterFilter(val)}
              options={chapters.map(c => ({ label: c, value: c }))}
            />
            <Button icon={<ReloadOutlined />} onClick={loadNodes}>刷新</Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增知识点</Button>
          </Space>
        }
      >
        <Table
          rowKey="id"
          columns={columns}
          dataSource={nodes}
          loading={loading}
          size="middle"
          pagination={{
            current: pagination.current,
            pageSize: pagination.pageSize,
            showSizeChanger: true,
            pageSizeOptions: ['10', '15', '20', '50', '100'],
            showTotal: (t) => `共 ${t} 条`,
            onChange: (page, pageSize) => setPagination({ current: page, pageSize }),
          }}
        />
      </Card>

      {/* 编辑/新增弹窗 */}
      <Modal
        title={editingNode ? '编辑知识点' : '新增知识点'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => setModalOpen(false)}
        width={700}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="名称" rules={[{ required: true }]}>
            <Input placeholder="如：TCP 协议" />
          </Form.Item>
          <Space>
            <Form.Item name="type" label="类型" rules={[{ required: true }]}>
              <Select style={{ width: 120 }}>
                {nodeTypes.map(t => <Option key={t} value={t}>{t}</Option>)}
              </Select>
            </Form.Item>
            <Form.Item name="layer" label="层次" rules={[{ required: true }]}>
              <Select style={{ width: 120 }}>
                {layers.map(l => <Option key={l} value={l}>{l}</Option>)}
              </Select>
            </Form.Item>
            <Form.Item name="chapter" label="章节" rules={[{ required: true }]}>
              <Select style={{ width: 180 }}>
                {chapters.map(c => <Option key={c} value={c}>{c}</Option>)}
              </Select>
            </Form.Item>
          </Space>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={2} placeholder="详细描述这个知识点" />
          </Form.Item>
          <Form.Item name="difficulty" label="难度 (1-5)">
            <InputNumber min={1} max={5} />
          </Form.Item>
          <Form.Item name="keywords" label="关键词">
            <Select mode="tags" placeholder="输入后按回车添加关键词" />
          </Form.Item>
          <Form.Item name="image_urls" label="配图URL（可多个）">
            <Select mode="tags" placeholder="输入图片URL后按回车" />
          </Form.Item>
          <Form.Item name="video_url" label="视频URL（B站/YouTube/直链）">
            <Input placeholder="https://www.bilibili.com/video/BVxxx" />
          </Form.Item>
        </Form>

        {/* 关联关系管理（仅编辑时显示） */}
        {editingNode && (
          <>
            <Divider orientation="left" style={{ fontSize: 13, marginTop: 8 }}><LinkOutlined /> 关联关系管理</Divider>
            <div style={{ marginBottom: 12 }}>
              {nodeEdges.length === 0 ? (
                <span style={{ color: '#999' }}>暂无关联</span>
              ) : (
                <Space direction="vertical" style={{ width: '100%' }}>
                  {nodeEdges.map(e => (
                    <div key={e.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '4px 8px', background: '#fafafa', borderRadius: 4 }}>
                      <span>
                        <Tag color={relationColors[e.relation]}>{e.relation}</Tag>
                        {e.source === editingNode.id
                          ? <span>→ <Tag>{getNodeName(e.target)}</Tag></span>
                          : <span><Tag>{getNodeName(e.source)}</Tag> →</span>}
                        <span style={{ color: '#999', marginLeft: 8, fontSize: 12 }}>{e.description}</span>
                      </span>
                      <Popconfirm title="删除此关联？" onConfirm={() => handleDeleteEdge(e.id)}>
                        <Button size="small" danger icon={<DeleteOutlined />} />
                      </Popconfirm>
                    </div>
                  ))}
                </Space>
              )}
            </div>
            <Form form={newEdgeForm} layout="inline" style={{ gap: 8 }}>
              <Form.Item name="target" label="目标节点" rules={[{ required: true }]}>
                <Select showSearch placeholder="选择节点" style={{ width: 160 }}
                  filterOption={(input, option) => (option?.label as string)?.toLowerCase().includes(input.toLowerCase())}
                  options={nodes.filter(n => n.id !== editingNode.id).map(n => ({ label: n.name, value: n.id }))}
                />
              </Form.Item>
              <Form.Item name="relation" label="关系" rules={[{ required: true }]}>
                <Select style={{ width: 100 }}>
                  {relationTypes.map(r => <Option key={r} value={r}>{r}</Option>)}
                </Select>
              </Form.Item>
              <Form.Item name="description" label="说明">
                <Input placeholder="关系描述" style={{ width: 140 }} />
              </Form.Item>
              <Form.Item>
                <Button type="dashed" icon={<PlusOutlined />} onClick={handleAddEdge}>添加</Button>
              </Form.Item>
            </Form>
          </>
        )}
      </Modal>

      {/* 预览抽屉 */}
      <Drawer
        title={previewNode?.name || '知识点详情'}
        open={previewOpen}
        onClose={() => setPreviewOpen(false)}
        width={500}
        extra={previewNode && <Tag color={layerColors[previewNode.layer]}>{previewNode.layer}</Tag>}
      >
        {previewNode && (
          <>
            <div style={{ marginBottom: 16 }}>
              <Title level={5}>基本信息</Title>
              <table style={{ width: '100%', fontSize: 13, borderCollapse: 'collapse' }}>
                <tbody>
                  <tr><td style={{ padding: '4px 8px', color: '#999', width: 70 }}>ID</td><td>{previewNode.id}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>名称</td><td>{previewNode.name}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>类型</td><td><Tag>{previewNode.type}</Tag></td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>章节</td><td>{previewNode.chapter}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>难度</td><td>{'⭐'.repeat(previewNode.difficulty)}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>关键词</td>
                    <td><Space wrap>{previewNode.keywords?.map(k => <Tag key={k}>{k}</Tag>)}</Space></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div style={{ marginBottom: 16 }}>
              <Title level={5}>描述</Title>
              <div style={{ lineHeight: 1.8 }}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{previewNode.description}</ReactMarkdown>
              </div>
            </div>
            {previewNode.image_urls && previewNode.image_urls.length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>配图</Title>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {previewNode.image_urls.map((url, i) => (
                    <img key={i} src={url} alt={`${previewNode.name}`} referrerPolicy="no-referrer"
                      style={{ maxWidth: '100%', maxHeight: 200, borderRadius: 8, border: '1px solid #eee', cursor: 'pointer' }}
                      onClick={() => window.open(url, '_blank')}
                      onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }} />
                  ))}
                </div>
              </div>
            )}
            {previewNode.video_url && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>视频</Title>
                {(() => {
                  const bvid = previewNode.video_url.match(/BV[a-zA-Z0-9]{10}/);
                  return bvid ? (
                    <iframe src={`https://player.bilibili.com/player.html?bvid=${bvid[0]}&page=1&as_wide=1&high_quality=1`}
                      style={{ width: '100%', height: 240, border: 'none', borderRadius: 8 }} allowFullScreen />
                  ) : null;
                })()}
              </div>
            )}
            <div style={{ marginBottom: 16 }}>
              <Title level={5}>关联关系 ({previewEdges.length})</Title>
              {previewEdges.map(e => (
                <div key={e.id} style={{ marginBottom: 6, padding: 6, background: '#fafafa', borderRadius: 4 }}>
                  <Tag color={relationColors[e.relation]}>{e.relation}</Tag>
                  <span style={{ fontSize: 13 }}>
                    {e.source === previewNode.id ? `→ ${getNodeName(e.target)}` : `${getNodeName(e.source)} →`}
                  </span>
                  {e.description && <span style={{ color: '#999', marginLeft: 8, fontSize: 12 }}>{e.description}</span>}
                </div>
              ))}
            </div>
          </>
        )}
      </Drawer>
    </>
  );
}
