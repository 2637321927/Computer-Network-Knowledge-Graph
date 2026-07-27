import { useEffect, useRef, useState } from 'react';
import {
  Card, Select, Input, Button, Space, Tag, Drawer, message,
  Row, Col, Upload, Typography, Spin, Empty
} from 'antd';
import {
  SearchOutlined, ReloadOutlined, ExportOutlined, ImportOutlined,
} from '@ant-design/icons';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';
import ForceGraph3D from '3d-force-graph';
import * as THREE from 'three';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { KnowledgeNode, GraphStats, GraphData, NeighborData, CaseItem, QuestionItem } from '../types';
import {
  fetchGraph, fetchGraphStats, fetchNeighbors, exportData, importData,
  fetchCaseById, fetchQuestionById, fetchNodeCases, fetchNodeQuestions
} from '../services/api';
import type { UploadProps } from 'antd';

const { Option } = Select;
const { Paragraph, Title } = Typography;

// 节点颜色映射
const layerColors: Record<string, string> = {
  '概念层': '#5B8FF9',
  '案例层': '#5AD8A6',
  '问题层': '#F6BD16',
};

// 核心篇按协议层分色：网络层蓝、传输层绿、应用层橙。
const chapterColors: Record<string, string> = {
  '网络层': '#1677FF',
  '传输层': '#52C41A',
  '应用层': '#FA8C16',
};

const getNodeColor = (node: KnowledgeNode) => chapterColors[node.chapter] || layerColors[node.layer] || '#5B8FF9';

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

// 半透明版（用于边线，减少视觉杂乱）
const relationColorsDim: Record<string, string> = {
  '包含': 'rgba(91,143,249,0.35)',
  '前置知识': 'rgba(246,189,22,0.35)',
  '属于层': 'rgba(90,216,166,0.35)',
  '相关案例': 'rgba(255,107,59,0.35)',
  '关联试题': 'rgba(232,104,74,0.35)',
  '应用于': 'rgba(109,200,236,0.35)',
  '对比': 'rgba(146,112,202,0.35)',
  '依赖': 'rgba(255,153,195,0.35)',
};

export default function GraphPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const container3dRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const graph3dRef = useRef<any>(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<GraphStats | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selectedNode, setSelectedNode] = useState<KnowledgeNode | null>(null);
  const [neighborData, setNeighborData] = useState<NeighborData | null>(null);
  const [caseDetail, setCaseDetail] = useState<CaseItem | null>(null);
  const [questionDetail, setQuestionDetail] = useState<QuestionItem | null>(null);
  const [relatedCases, setRelatedCases] = useState<CaseItem[]>([]);
  const [relatedQuestions, setRelatedQuestions] = useState<QuestionItem[]>([]);
  const [filterChapter, setFilterChapter] = useState<string | undefined>();
  const [filterLayer, setFilterLayer] = useState<string | undefined>();
  const [searchKeyword, setSearchKeyword] = useState('');
  const [layoutMode, setLayoutMode] = useState<'force' | '3d'>('force');
  const layoutModeRef = useRef<'force' | '3d'>('force');
  const [panMode3d, setPanMode3d] = useState(false);

  // 同步ref
  useEffect(() => { layoutModeRef.current = layoutMode; }, [layoutMode]);

  // 最近一次加载的完整数据（用于点击查询）
  const lastDataRef = useRef<GraphData>({ nodes: [], edges: [] });

  const showNodeDetails = async (node: KnowledgeNode) => {
    setSelectedNode(node);
    setCaseDetail(null);
    setQuestionDetail(null);
    setRelatedCases([]);
    setRelatedQuestions([]);
    setDrawerOpen(true);

    const [neighbors, cases, questions] = await Promise.allSettled([
      fetchNeighbors(node.id),
      fetchNodeCases(node.id),
      fetchNodeQuestions(node.id),
    ]);
    setNeighborData(neighbors.status === 'fulfilled' ? neighbors.value : null);
    setRelatedCases(cases.status === 'fulfilled' ? cases.value : []);
    setRelatedQuestions(questions.status === 'fulfilled' ? questions.value : []);

    if (node.type === '案例' || node.layer === '案例层') {
      try { setCaseDetail(await fetchCaseById(node.id)); } catch { setCaseDetail(null); }
    }
    if (node.type === '问题' || node.layer === '问题层') {
      try { setQuestionDetail(await fetchQuestionById(node.id)); } catch { setQuestionDetail(null); }
    }
  };

  // 初始化统计
  useEffect(() => {
    fetchGraphStats().then(setStats).catch(console.error);
  }, []);

  // 仅在首次挂载时初始化 vis-network
  useEffect(() => {
    if (!containerRef.current) return;
    const options = {
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -60,
          centralGravity: 0.005,
          springLength: 200,
          springConstant: 0.04,
          damping: 0.5,
        },
        stabilization: { enabled: true, iterations: 200 },
      },
      interaction: { hover: true, tooltipDelay: 200, zoomView: true, dragView: true },
      layout: { improvedLayout: true },
    };
    const network = new Network(containerRef.current, {}, options);
    network.on('click', async (params: any) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = lastDataRef.current.nodes.find(n => n.id === nodeId);
        if (node) {
          void showNodeDetails(node);
        }
      }
    });
    networkRef.current = network;
    // 初始加载
    doLoadGraph();
    return () => {
      network.destroy();
      if (graph3dRef.current) { try { graph3dRef.current._destructor(); } catch(e) {} }
    };
  }, []);

  // 筛选条件变化时自动刷新图谱
  useEffect(() => {
    if (networkRef.current) {
      doLoadGraph();
    }
  }, [filterChapter, filterLayer]);

  // 3D平移/旋转切换
  useEffect(() => {
    const g3d = graph3dRef.current;
    if (g3d) {
      const ctrl = g3d.controls();
      if (ctrl) {
        ctrl.mouseButtons = panMode3d
          ? { LEFT: THREE.MOUSE.PAN, MIDDLE: THREE.MOUSE.ROTATE }
          : { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.PAN };
        ctrl.panSpeed = 0.2;
      }
    }
  }, [panMode3d]);

  // 更新图谱数据（不重建 network 实例）
  const updateGraph = (data: GraphData, mode: 'force' | '3d') => {
    lastDataRef.current = data;

    // 3D力导向模式
    if (mode === '3d') {
      if (graph3dRef.current) { try { graph3dRef.current._destructor(); } catch(e) {} }
      if (!container3dRef.current) return;
      const gData = {
        nodes: data.nodes.map(n => ({
          id: n.id,
          name: n.name,
          layer: n.layer,
          nodeType: n.type,
          chapter: n.chapter,
          color: getNodeColor(n),
        })),
        links: data.edges.map(e => ({
          source: e.source,
          target: e.target,
          relation: e.relation,
          color: relationColors[e.relation] || '#999',
        })),
      };
      const graph3d = (ForceGraph3D as any)()(container3dRef.current)
        .graphData(gData)
        .nodeColor((n: any) => n.color)
        .nodeLabel((n: any) => `<b>${n.name}</b><br>类型：${n.nodeType}<br>章节：${n.chapter}`)
        .nodeThreeObject((node: any) => {
          const group = new THREE.Group();
          // 小球
          const sphereGeom = new THREE.SphereGeometry(2);
          const sphereMat = new THREE.MeshBasicMaterial({ color: node.color });
          const sphere = new THREE.Mesh(sphereGeom, sphereMat);
          group.add(sphere);
          // 文字标签
          const canvas = document.createElement('canvas');
          canvas.width = 128;
          canvas.height = 40;
          const ctx = canvas.getContext('2d')!;
          ctx.font = '14px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillStyle = '#fff';
          const name = node.name.length > 8 ? node.name.slice(0, 8) + '...' : node.name;
          ctx.fillText(name, 64, 26);
          const texture = new THREE.CanvasTexture(canvas);
          const mat = new THREE.SpriteMaterial({ map: texture, depthTest: false });
          const sprite = new THREE.Sprite(mat);
          sprite.scale.set(12, 4, 1);
          sprite.position.set(0, 4, 0);
          group.add(sprite);
          return group;
        })
        .linkColor((l: any) => l.color)
        .linkWidth(1)
        .linkDirectionalArrowLength(4)
        .linkDirectionalArrowRelPos(1)
        .enableNodeDrag(true)
        .onNodeClick(async (n: any) => {
          const node = data.nodes.find(x => x.id === n.id);
          if (node) {
            void showNodeDetails(node);
          }
        });
      graph3dRef.current = graph3d;
      // 根据panMode设置控制模式
      const ctrl = graph3d.controls();
      if (ctrl) {
        ctrl.mouseButtons = panMode3d
          ? { LEFT: THREE.MOUSE.PAN, MIDDLE: THREE.MOUSE.ROTATE }
          : { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.PAN };
        ctrl.panSpeed = 0.2;
      }
      return;
    }

    // 2D模式（力导向/按层次）
    const network = networkRef.current;
    if (!network) return;

    const visNodes = new DataSet(
      data.nodes.map(n => ({
        id: n.id,
        label: n.name,
        title: `<b>${n.name}</b><br>类型：${n.type}<br>章节：${n.chapter}<br>点击查看详情`,
        color: {
          background: getNodeColor(n),
          border: '#fff',
          highlight: { background: getNodeColor(n), border: '#333' },
        },
        font: { color: '#333', size: 14 },
        borderWidth: 2,
        shape: 'dot',
        size: 18,
      }))
    );

    const visEdges = new DataSet(
      data.edges.map(e => ({
        id: e.id,
        from: e.source,
        to: e.target,
        arrows: e.relation === '对比' ? 'to, from' : 'to',
        color: { color: relationColorsDim[e.relation] || 'rgba(153,153,153,0.35)', highlight: relationColors[e.relation] || '#999' },
        width: 0.8,
        smooth: { enabled: true, type: 'continuous', roundness: 0.5 },
        label: e.relation,
        font: { color: relationColors[e.relation] || '#666', size: 9, strokeWidth: 2, strokeColor: '#fff', align: 'middle' },
        title: e.description,
      }))
    );

    network.setData({ nodes: visNodes as any, edges: visEdges as any });

    network.setOptions({
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
            gravitationalConstant: -60,
            centralGravity: 0.008,
            springLength: 150,
            springConstant: 0.02,
            damping: 0.5,
          },
          stabilization: { enabled: true, iterations: 200 },
        },
      });
  };

  const doLoadGraph = async () => {
    setLoading(true);
    try {
      const data = await fetchGraph({
        chapter: filterChapter,
        layer: filterLayer,
      });
      let filteredData = data;
      if (searchKeyword) {
        const kw = searchKeyword.toLowerCase();
        filteredData = {
          nodes: data.nodes.filter(n =>
            n.name.toLowerCase().includes(kw) ||
            n.keywords.some(k => k.toLowerCase().includes(kw)) ||
            n.description.toLowerCase().includes(kw)
          ),
          edges: data.edges.filter(e => {
            const nodeIds = new Set(filteredData.nodes.map(n => n.id));
            return nodeIds.has(e.source) && nodeIds.has(e.target);
          })
        };
      }
      updateGraph(filteredData, layoutModeRef.current);
      fetchGraphStats().then(setStats).catch(console.error);
    } catch (err) {
      message.error('加载图谱数据失败');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 导出数据
  const handleExport = async () => {
    try {
      const data = await exportData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `知识图谱数据_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      message.success('导出成功');
    } catch {
      message.error('导出失败');
    }
  };

  // 导入数据
  const handleImport: UploadProps['beforeUpload'] = async (file) => {
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      await importData(data);
      message.success('导入成功');
      doLoadGraph();
    } catch {
      message.error('导入失败，请检查文件格式');
    }
    return false;
  };

  return (
    <div>
      {/* 统计卡片 */}
      {stats && (
        <Row gutter={12} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Card size="small" hoverable style={{ borderRadius: 10, borderLeft: '4px solid #5B8FF9' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ fontSize: 32, fontWeight: 700, color: '#5B8FF9' }}>{stats.total_nodes}</div>
                <div style={{ color: '#888', fontSize: 14 }}>知识点</div>
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" hoverable style={{ borderRadius: 10, borderLeft: '4px solid #F6BD16' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ fontSize: 32, fontWeight: 700, color: '#F6BD16' }}>{stats.total_edges}</div>
                <div style={{ color: '#888', fontSize: 14 }}>关系</div>
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" hoverable style={{ borderRadius: 10, borderLeft: '4px solid #5AD8A6' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ fontSize: 32, fontWeight: 700, color: '#5AD8A6' }}>{stats.total_cases}</div>
                <div style={{ color: '#888', fontSize: 14 }}>案例</div>
              </div>
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small" hoverable style={{ borderRadius: 10, borderLeft: '4px solid #FF6B3B' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ fontSize: 32, fontWeight: 700, color: '#FF6B3B' }}>{stats.total_questions}</div>
                <div style={{ color: '#888', fontSize: 14 }}>试题</div>
              </div>
            </Card>
          </Col>
        </Row>
      )}

      {/* 操作栏 */}
      <Card size="small" style={{ marginBottom: 16 }}>
        <Space wrap>
          <Select
            allowClear
            placeholder="全部章节"
            style={{ width: 180 }}
            value={filterChapter}
            onChange={setFilterChapter}
          >
            {['计算机网络概述', '物理层', '数据链路层', '局域网原理', '网络层', '传输层', '应用层', '网络性能优化', '软件定义网络与边缘计算', '课程综合项目'].map(c => (
              <Option key={c} value={c}>{c}</Option>
            ))}
          </Select>
          <Space size={4} aria-label="核心篇协议层颜色图例">
            <Tag color={chapterColors['网络层']}>网络层</Tag>
            <Tag color={chapterColors['传输层']}>传输层</Tag>
            <Tag color={chapterColors['应用层']}>应用层</Tag>
          </Space>
          <Select
            allowClear
            placeholder="全部层次"
            style={{ width: 140 }}
            value={filterLayer}
            onChange={setFilterLayer}
          >
            <Option value="概念层">概念层</Option>
            <Option value="案例层">案例层</Option>
            <Option value="问题层">问题层</Option>
          </Select>
          <Input.Search
            placeholder="搜索知识点..."
            style={{ width: 240 }}
            value={searchKeyword}
            onChange={e => setSearchKeyword(e.target.value)}
            onSearch={doLoadGraph}
            enterButton={<SearchOutlined />}
          />
          <Button icon={<ReloadOutlined />} onClick={doLoadGraph}>刷新</Button>
          <Button
            type={layoutMode !== 'force' ? 'primary' : 'default'}
            onClick={() => {
              const modes: Array<'force' | '3d'> = ['force', '3d'];
              const idx = modes.indexOf(layoutMode);
              const next = modes[(idx + 1) % 2];
              layoutModeRef.current = next;
              setLayoutMode(next);
              // 切换到3D时需要重新加载
              setTimeout(() => doLoadGraph(), 50);
            }}
          >
            {layoutMode === 'force' ? '力导向' : '3D力导向'}
          </Button>
          <Button icon={<ExportOutlined />} onClick={handleExport}>导出</Button>
          <Upload beforeUpload={handleImport} showUploadList={false} accept=".json">
            <Button icon={<ImportOutlined />}>导入</Button>
          </Upload>
        </Space>
      </Card>

      {/* 图谱画布 */}
      <div style={{ position: 'relative' }}>
        <div
          className="graph-container"
          ref={containerRef}
          style={{ background: '#fff', display: layoutMode === '3d' ? 'none' : 'block' }}
        />
        <div
          ref={container3dRef}
          onContextMenu={(e) => e.preventDefault()}
          style={{ width: '100%', height: 'calc(100vh - 140px)', display: layoutMode === '3d' ? 'block' : 'none', position: 'relative' }}
        />
        {layoutMode === '3d' && (
          <Button
            size="small"
            type={panMode3d ? 'primary' : 'default'}
            onClick={() => setPanMode3d(!panMode3d)}
            style={{ position: 'absolute', bottom: 12, right: 12, zIndex: 20, opacity: 0.85 }}
          >
            {panMode3d ? '平移中' : '旋转中'}
          </Button>
        )}
        {loading && (
          <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }}>
            <Spin size="large" />
          </div>
        )}
        {!loading && stats?.total_nodes === 0 && (
          <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
            <Empty description="暂无数据，请先导入知识图谱数据" />
          </div>
        )}
      </div>

      {/* 节点详情抽屉 */}
      <Drawer
        title={selectedNode?.name || '节点详情'}
        open={drawerOpen}
        onClose={() => { setDrawerOpen(false); setNeighborData(null); }}
        width={480}
        extra={<Tag color={selectedNode ? getNodeColor(selectedNode) : undefined}>{selectedNode?.chapter}</Tag>}
      >
        {selectedNode && (
          <>
            <div style={{ marginBottom: 16 }}>
              <Title level={5}>基本信息</Title>
              <table style={{ width: '100%', fontSize: 13, borderCollapse: 'collapse' }}>
                <tbody>
                  <tr><td style={{ padding: '4px 8px', color: '#999', width: 70 }}>ID</td><td>{selectedNode.id}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>名称</td><td>{selectedNode.name}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>类型</td><td><Tag>{selectedNode.type}</Tag></td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>章节</td><td>{selectedNode.chapter}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>难度</td><td>{'⭐'.repeat(selectedNode.difficulty)}</td></tr>
                  <tr><td style={{ padding: '4px 8px', color: '#999' }}>关键词</td>
                    <td><Space wrap>{selectedNode.keywords.map(k => <Tag key={k}>{k}</Tag>)}</Space></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div style={{ marginBottom: 16 }}>
              <Title level={5}>描述</Title>
              <div style={{ lineHeight: 1.8 }}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {selectedNode.description}
                </ReactMarkdown>
              </div>
            </div>

            {relatedQuestions.length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>关联试题 ({relatedQuestions.length})</Title>
                {relatedQuestions.map(question => (
                  <Card key={question.id} size="small" style={{ marginBottom: 8 }}>
                    <Paragraph strong>{question.title}</Paragraph>
                    {question.options.map(option => <div key={option}>{option}</div>)}
                    <div style={{ marginTop: 8 }}>
                      <Tag color="green">答案：{question.answer}</Tag>
                      {question.difficulty_label && <Tag>{question.difficulty_label}</Tag>}
                    </div>
                    <Paragraph style={{ marginTop: 8, marginBottom: 0, color: '#666' }}>
                      解析：{question.explanation || question.analysis}
                    </Paragraph>
                  </Card>
                ))}
              </div>
            )}

            {relatedCases.length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>关联案例 ({relatedCases.length})</Title>
                {relatedCases.map(item => (
                  <Card key={item.id} size="small" title={item.title} style={{ marginBottom: 8 }}>
                    <Paragraph>{item.description}</Paragraph>
                    {item.analysis && <Paragraph style={{ color: '#666', marginBottom: 0 }}>分析：{item.analysis}</Paragraph>}
                  </Card>
                ))}
              </div>
            )}

            {/* 配图展示（支持多张） */}
            {selectedNode.image_urls && selectedNode.image_urls.length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>配图 ({selectedNode.image_urls.length}张)</Title>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {selectedNode.image_urls.map((url, i) => (
                    <img
                      key={i}
                      src={url}
                      alt={`${selectedNode.name} - ${i + 1}`}
                      referrerPolicy="no-referrer"
                      crossOrigin="anonymous"
                      style={{ maxWidth: '100%', maxHeight: 300, borderRadius: 8, border: '1px solid #eee', cursor: 'pointer' }}
                      onClick={() => window.open(url, '_blank')}
                      onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* 视频展示 */}
            {selectedNode.video_url && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>视频</Title>
                {selectedNode.video_url.includes('bilibili.com') || selectedNode.video_url.includes('b23.tv') ? (
                  (() => {
                    const url = selectedNode.video_url;
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
                        style={{ width: '100%', height: 260, border: 'none', borderRadius: 8 }}
                        allowFullScreen
                      />
                    );
                  })()
                ) : selectedNode.video_url.includes('youtube.com') || selectedNode.video_url.includes('youtu.be') ? (
                  <iframe
                    src={selectedNode.video_url.replace('watch?v=', 'embed/').replace('youtu.be/', 'youtube.com/embed/')}
                    style={{ width: '100%', height: 260, border: 'none', borderRadius: 8 }}
                    allowFullScreen
                  />
                ) : (
                  <video
                    src={selectedNode.video_url}
                    controls
                    style={{ maxWidth: '100%', borderRadius: 8 }}
                  />
                )}
              </div>
            )}

            {/* 案例详细内容 */}
            {caseDetail && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>案例详情</Title>
                <div style={{ background: '#fafafa', padding: 12, borderRadius: 8, lineHeight: 1.8 }}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {caseDetail.content}
                  </ReactMarkdown>
                </div>
              </div>
            )}

            {/* 试题详细内容 */}
            {questionDetail && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>试题详情</Title>
                <div style={{ background: '#fafafa', padding: 12, borderRadius: 8 }}>
                  <Paragraph strong>{questionDetail.title}</Paragraph>
                  {questionDetail.options.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      {questionDetail.options.map((opt, i) => (
                        <div key={i}>{opt}</div>
                      ))}
                    </div>
                  )}
                  <div style={{ marginTop: 8 }}>
                    <Tag color="green">答案：{questionDetail.answer}</Tag>
                  </div>
                  {questionDetail.explanation && (
                    <div style={{ marginTop: 8, color: '#666' }}>
                      <strong>解析：</strong>{questionDetail.explanation}
                    </div>
                  )}
                </div>
              </div>
            )}

            {neighborData && (
              <>
                <div style={{ marginBottom: 16 }}>
                  <Title level={5}>相邻节点 ({neighborData.neighbors.length})</Title>
                  <Space wrap>
                    {neighborData.neighbors.map(n => (
                      <Tag
                        key={n.id}
                        color={getNodeColor(n)}
                        style={{ cursor: 'pointer' }}
                        onClick={() => { void showNodeDetails(n); }}
                      >
                        {n.name}
                      </Tag>
                    ))}
                  </Space>
                </div>

                <div style={{ marginBottom: 16 }}>
                  <Title level={5}>关联关系 ({neighborData.edges.length})</Title>
                  {neighborData.edges.map(e => (
                    <div key={e.id} style={{ marginBottom: 8, padding: 8, background: '#fafafa', borderRadius: 4 }}>
                      <Tag color={relationColors[e.relation]}>{e.relation}</Tag>
                      <span style={{ fontSize: 13 }}>{e.description}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </>
        )}
      </Drawer>
    </div>
  );
}
