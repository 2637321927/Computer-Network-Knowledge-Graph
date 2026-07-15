import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Typography } from 'antd';
import {
  ApartmentOutlined,
  NodeIndexOutlined,
  FileTextOutlined,
  QuestionCircleOutlined,
  ExportOutlined,
} from '@ant-design/icons';
import GraphPage from './pages/GraphPage';
import NodesPage from './pages/NodesPage';
import CasesPage from './pages/CasesPage';
import QuestionsPage from './pages/QuestionsPage';

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: '/', icon: <ApartmentOutlined />, label: '知识图谱' },
  { key: '/nodes', icon: <NodeIndexOutlined />, label: '知识点管理' },
  { key: '/cases', icon: <FileTextOutlined />, label: '案例管理' },
  { key: '/questions', icon: <QuestionCircleOutlined />, label: '试题管理' },
];

export default function App() {
  const navigate = useNavigate();
  const location = useLocation();

  // 默认选中图谱页
  const selectedKey = location.pathname === '/' ? '/' : location.pathname;

  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <ApartmentOutlined style={{ fontSize: 28, color: '#fff' }} />
          <Typography.Title level={4} style={{ color: '#fff', margin: 0 }}>
            计算机网络 · 知识图谱
          </Typography.Title>
        </div>
      </Header>
      <Layout>
        <Sider width={200} className="app-sider">
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            items={menuItems}
            onClick={({ key }) => navigate(key)}
            style={{ height: '100%', borderRight: 0, paddingTop: 8 }}
          />
        </Sider>
        <Content className="app-content">
          <Routes>
            <Route path="/" element={<GraphPage />} />
            <Route path="/nodes" element={<NodesPage />} />
            <Route path="/cases" element={<CasesPage />} />
            <Route path="/questions" element={<QuestionsPage />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}
