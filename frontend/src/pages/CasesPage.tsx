import { useEffect, useState } from 'react';
import {
  Table, Button, Space, Modal, Form, Input, Select, Tag, message,
  Popconfirm, Card, Drawer, Typography, InputNumber
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, ReloadOutlined, EyeOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { CaseItem } from '../types';
import { fetchCases, fetchCaseById } from '../services/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const { Option } = Select;
const { Paragraph } = Typography;
import axios from 'axios';

export default function CasesPage() {
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [detailOpen, setDetailOpen] = useState(false);
  const [editingCase, setEditingCase] = useState<CaseItem | null>(null);
  const [viewingCase, setViewingCase] = useState<CaseItem | null>(null);
  const [form] = Form.useForm();
  const [chapterFilter, setChapterFilter] = useState<string | undefined>(undefined);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 15 });

  const loadCases = async () => {
    setLoading(true);
    try {
      const data = await fetchCases({ chapter: chapterFilter });
      setCases(data);
    } catch {
      message.error('加载案例失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadCases(); }, [chapterFilter]);
  
  // 切换筛选时重置分页
  useEffect(() => { setPagination(prev => ({ ...prev, current: 1 })); }, [chapterFilter]);

  const handleAdd = () => {
    setEditingCase(null);
    form.resetFields();
    setModalOpen(true);
  };

  const handleEdit = (c: CaseItem) => {
    setEditingCase(c);
    form.setFieldsValue({
      ...c,
      related_nodes: c.related_nodes.join(', ')
    });
    setModalOpen(true);
  };

  const handleView = async (c: CaseItem) => {
    try {
      const detail = await fetchCaseById(c.id);
      setViewingCase(detail);
    } catch {
      setViewingCase(c);
    }
    setDetailOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await axios.delete(`/api/cases/${id}`);
      message.success('删除成功');
      loadCases();
    } catch {
      message.error('删除失败');
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        ...values,
        related_nodes: typeof values.related_nodes === 'string'
          ? values.related_nodes.split(',').map((s: string) => s.trim()).filter(Boolean)
          : values.related_nodes || [],
        tags: values.tags || [],
        image_urls: values.image_urls || [],
      };

      if (editingCase) {
        await axios.put(`/api/cases/${editingCase.id}`, payload);
        message.success('更新成功');
      } else {
        await axios.post('/api/cases', payload);
        message.success('创建成功');
      }
      setModalOpen(false);
      loadCases();
    } catch (err: any) {
      if (err.errorFields) return;
      message.error('操作失败');
    }
  };

  const columns: ColumnsType<CaseItem> = [
    { title: 'ID', dataIndex: 'id', width: 150 },
    { title: '标题', dataIndex: 'title', width: 220,
      render: (text, record) => <a onClick={() => handleView(record)}>{text}</a>
    },
    {
      title: '描述', dataIndex: 'description', ellipsis: true
    },
    { title: '章节', dataIndex: 'chapter', width: 100 },
    {
      title: '难度', dataIndex: 'difficulty', width: 60,
      render: (d: number) => '⭐'.repeat(d)
    },
    {
      title: '关联知识点', dataIndex: 'related_nodes', width: 150,
      render: (ids: string[]) => <Space wrap>{ids?.map(id => <Tag key={id}>{id}</Tag>)}</Space>
    },
    {
      title: '标签', dataIndex: 'tags', width: 160,
      render: (tags: string[]) => <Space wrap>{tags?.map(t => <Tag key={t} color="green">{t}</Tag>)}</Space>
    },
    {
      title: '操作', key: 'actions', width: 150,
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EyeOutlined />} onClick={() => handleView(record)} />
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
        title="案例管理"
        extra={
          <Space>
            <Select
              allowClear
              placeholder="按章节筛选"
              style={{ width: 180 }}
              value={chapterFilter}
              onChange={(val) => setChapterFilter(val)}
              options={['计算机网络概述', '物理层', '数据链路层', '局域网原理', '网络层', '传输层', '应用层', '网络性能优化', '软件定义网络与边缘计算', '课程综合项目'].map(c => ({ label: c, value: c }))}
            />
            <Button icon={<ReloadOutlined />} onClick={loadCases}>刷新</Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增案例</Button>
          </Space>
        }
      >
        <Table
          rowKey="id"
          columns={columns}
          dataSource={cases}
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

      {/* 新增/编辑弹窗 */}
      <Modal
        title={editingCase ? '编辑案例' : '新增案例'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => setModalOpen(false)}
        width={640}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="title" label="标题" rules={[{ required: true }]}>
            <Input placeholder="案例标题" />
          </Form.Item>
          <Form.Item name="description" label="简要描述">
            <Input.TextArea rows={2} />
          </Form.Item>
          <Space>
            <Form.Item name="chapter" label="章节">
              <Select style={{ width: 180 }}>
                {['计算机网络概述', '物理层', '数据链路层', '局域网原理', '网络层', '传输层', '应用层', '网络性能优化', '软件定义网络与边缘计算', '课程综合项目'].map(c => <Option key={c} value={c}>{c}</Option>)}
              </Select>
            </Form.Item>
            <Form.Item name="difficulty" label="难度 (1-5)">
              <InputNumber min={1} max={5} />
            </Form.Item>
          </Space>
          <Form.Item name="content" label="详细内容（支持 Markdown）">
            <Input.TextArea rows={8} placeholder="案例详细内容..." />
          </Form.Item>
          <Form.Item name="related_nodes" label="关联知识点 ID（逗号分隔）">
            <Input placeholder="tcp, congestion_control" />
          </Form.Item>
          <Form.Item name="tags" label="标签">
            <Select mode="tags" placeholder="输入标签后按回车" />
          </Form.Item>
          <Form.Item name="image_urls" label="配图URL（可多个）">
            <Select mode="tags" placeholder="输入图片URL后按回车" />
          </Form.Item>
          <Form.Item name="video_url" label="视频URL">
            <Input placeholder="https://www.bilibili.com/video/BVxxx" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 查看详情抽屉 */}
      <Drawer
        title={viewingCase?.title}
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
        width={560}
      >
        {viewingCase && (
          <>
            <Paragraph type="secondary">{viewingCase.description}</Paragraph>
            <div style={{ margin: '16px 0' }}>
              <Space wrap>
                {viewingCase.tags?.map(t => <Tag key={t} color="green">{t}</Tag>)}
              </Space>
            </div>

            {/* 配图（支持多张） */}
            {viewingCase.image_urls && viewingCase.image_urls.length > 0 && (
              <div style={{ marginBottom: 16, display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {viewingCase.image_urls.map((url, i) => (
                  <img
                    key={i}
                    src={url}
                    alt={`${viewingCase.title} - ${i + 1}`}
                    referrerPolicy="no-referrer"
                    crossOrigin="anonymous"
                    style={{ maxWidth: '100%', maxHeight: 300, borderRadius: 8, border: '1px solid #eee', cursor: 'pointer' }}
                    onClick={() => window.open(url, '_blank')}
                    onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
                  />
                ))}
              </div>
            )}

            {/* 视频 */}
            {viewingCase.video_url && (
              <div style={{ marginBottom: 16 }}>
                {viewingCase.video_url.includes('bilibili.com') || viewingCase.video_url.includes('b23.tv') ? (
                  (() => {
                    const url = viewingCase.video_url;
                    const bvidMatch = url.match(/BV[a-zA-Z0-9]{10}/);
                    const aidMatch = url.match(/av(\d+)/);
                    let embedUrl = '';
                    if (bvidMatch) {
                      embedUrl = `https://player.bilibili.com/player.html?bvid=${bvidMatch[0]}&page=1&as_wide=1&high_quality=1`;
                    } else if (aidMatch) {
                      embedUrl = `https://player.bilibili.com/player.html?aid=${aidMatch[1]}&page=1&as_wide=1&high_quality=1`;
                    } else {
                      embedUrl = url;
                    }
                    return (
                      <iframe
                        src={embedUrl}
                        style={{ width: '100%', height: 280, border: 'none', borderRadius: 8 }}
                        allowFullScreen
                      />
                    );
                  })()
                ) : (
                  <video src={viewingCase.video_url} controls style={{ maxWidth: '100%', borderRadius: 8 }} />
                )}
              </div>
            )}

            <div style={{ background: '#fafafa', padding: 16, borderRadius: 8, lineHeight: 1.8 }}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {viewingCase.content}
              </ReactMarkdown>
            </div>
          </>
        )}
      </Drawer>
    </>
  );
}
