import { useEffect, useState } from 'react';
import {
  Table, Button, Space, Modal, Form, Input, Select, Tag, message,
  Popconfirm, Card, InputNumber, Drawer, Typography, Radio
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, ReloadOutlined, EyeOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { QuestionItem } from '../types';
import { fetchQuestions, fetchQuestionById } from '../services/api';
import axios from 'axios';

const { Paragraph, Title } = Typography;
const { Option } = Select;

const questionTypes = ['单选题', '多选题', '判断题', '填空题', '简答题', '计算题'];
const chapters = [
  '计算机网络概述', '物理层', '数据链路层', '局域网原理',
  '网络层', '传输层', '应用层', '网络性能优化',
  '软件定义网络与边缘计算', '课程综合项目'
];

export default function QuestionsPage() {
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [detailOpen, setDetailOpen] = useState(false);
  const [editingQ, setEditingQ] = useState<QuestionItem | null>(null);
  const [viewingQ, setViewingQ] = useState<QuestionItem | null>(null);
  const [form] = Form.useForm();
  const [chapterFilter, setChapterFilter] = useState<string | undefined>(undefined);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 15 });

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const data = await fetchQuestions({ chapter: chapterFilter });
      setQuestions(data);
    } catch {
      message.error('加载试题失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadQuestions(); }, [chapterFilter]);
  
  // 切换筛选时重置分页
  useEffect(() => { setPagination(prev => ({ ...prev, current: 1 })); }, [chapterFilter]);

  const handleAdd = () => {
    setEditingQ(null);
    form.resetFields();
    setModalOpen(true);
  };

  const handleEdit = (q: QuestionItem) => {
    setEditingQ(q);
    form.setFieldsValue({
      ...q,
      related_nodes: (q.related_nodes || []).join(', '),
      keywords: q.keywords || [],
    });
    setModalOpen(true);
  };

  const handleView = async (q: QuestionItem) => {
    try {
      const detail = await fetchQuestionById(q.id);
      setViewingQ(detail);
    } catch {
      setViewingQ(q);
    }
    setDetailOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await axios.delete(`/api/questions/${id}`);
      message.success('删除成功');
      loadQuestions();
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
        options: values.options || [],
        keywords: values.keywords || [],
      };

      if (editingQ) {
        await axios.put(`/api/questions/${editingQ.id}`, payload);
        message.success('更新成功');
      } else {
        await axios.post('/api/questions', payload);
        message.success('创建成功');
      }
      setModalOpen(false);
      loadQuestions();
    } catch (err: any) {
      if (err.errorFields) return;
      message.error('操作失败');
    }
  };

  const typeColors: Record<string, string> = {
    '单选题': 'blue',
    '多选题': 'purple',
    '判断题': 'cyan',
    '填空题': 'green',
    '简答题': 'orange',
    '计算题': 'red',
  };

  const columns: ColumnsType<QuestionItem> = [
    { title: 'ID', dataIndex: 'id', width: 90 },
    { title: '名称', dataIndex: 'name', width: 160 },
    {
      title: '题目', dataIndex: 'title', width: 260,
      render: (text, record) => <a onClick={() => handleView(record)}>{text}</a>
    },
    {
      title: '题型', dataIndex: 'type', width: 80,
      render: (t: string) => <Tag color={typeColors[t]}>{t}</Tag>
    },
    { title: '章节', dataIndex: 'chapter', width: 120 },
    {
      title: '难度', dataIndex: 'difficulty', width: 70,
      render: (d: number) => '⭐'.repeat(d)
    },
    {
      title: '关键词', dataIndex: 'keywords', width: 150,
      render: (kw: string[]) => <Space wrap>{kw?.map(k => <Tag key={k}>{k}</Tag>)}</Space>
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
        title="试题管理"
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
            <Button icon={<ReloadOutlined />} onClick={loadQuestions}>刷新</Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增试题</Button>
          </Space>
        }
      >
        <Table
          rowKey="id"
          columns={columns}
          dataSource={questions}
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
        title={editingQ ? '编辑试题' : '新增试题'}
        open={modalOpen}
        onOk={handleSubmit}
        onCancel={() => setModalOpen(false)}
        width={640}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="题目名称（图中显示）" rules={[{ required: true }]}>
            <Input placeholder="如：TCP 三次握手过程" />
          </Form.Item>
          <Form.Item name="title" label="题目标题/题干" rules={[{ required: true }]}>
            <Input.TextArea rows={2} placeholder="请输入题目内容" />
          </Form.Item>
          <Space>
            <Form.Item name="type" label="题型" rules={[{ required: true }]}>
              <Select style={{ width: 120 }}>
                {questionTypes.map(t => <Option key={t} value={t}>{t}</Option>)}
              </Select>
            </Form.Item>
            <Form.Item name="chapter" label="章节">
              <Select style={{ width: 160 }}>
                {chapters.map(c => <Option key={c} value={c}>{c}</Option>)}
              </Select>
            </Form.Item>
            <Form.Item name="difficulty" label="难度 (1-5)">
              <InputNumber min={1} max={5} />
            </Form.Item>
          </Space>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={2} placeholder="题目简要描述" />
          </Form.Item>
          <Form.Item name="keywords" label="关键词">
            <Select mode="tags" placeholder="输入后按回车添加关键词" />
          </Form.Item>
          <Form.Item name="options" label="选项（每个选项用回车分隔，仅选择/判断题需要）">
            <Select mode="tags" placeholder="输入选项后按回车" />
          </Form.Item>
          <Form.Item name="answer" label="参考答案">
            <Input placeholder="正确答案，如：C 或 ABD" />
          </Form.Item>
          <Form.Item name="explanation" label="解析">
            <Input.TextArea rows={2} placeholder="题目解析" />
          </Form.Item>
          <Form.Item name="related_nodes" label="关联知识点 ID（逗号分隔）">
            <Input placeholder="tcp, tcp_handshake" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 查看详情抽屉 */}
      <Drawer
        title="试题详情"
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
        width={560}
      >
        {viewingQ && (
          <>
            <Tag color={typeColors[viewingQ.type]} style={{ marginBottom: 12 }}>
              {viewingQ.type}
            </Tag>
            <Tag style={{ marginBottom: 12 }}>难度：{'⭐'.repeat(viewingQ.difficulty)}</Tag>

            <Title level={5}>题目</Title>
            <Paragraph>{viewingQ.title}</Paragraph>

            {viewingQ.options.length > 0 && (
              <>
                <Title level={5}>选项</Title>
                {viewingQ.options.map((opt, i) => (
                  <Paragraph key={i} style={{ marginBottom: 4 }}>{opt}</Paragraph>
                ))}
              </>
            )}

            <Title level={5}>答案</Title>
            <Paragraph style={{ color: '#52c41a', fontWeight: 'bold' }}>
              {viewingQ.answer}
            </Paragraph>

            <Title level={5}>解析</Title>
            <Paragraph>{viewingQ.explanation || '暂无解析'}</Paragraph>

            <Title level={5}>关联知识点</Title>
            <Space wrap>
              {viewingQ.related_nodes.map(id => <Tag key={id}>{id}</Tag>)}
            </Space>
          </>
        )}
      </Drawer>
    </>
  );
}
