# 计算机网络知识图谱 - 交互展示平台

面向《计算机网络》课程的三维知识图谱（概念层、案例层、问题层）构建与交互式展示平台。

## 快速启动

### 1. 后端

```bash
cd backend
pip install -r requirements.txt
python app.py          # → http://localhost:8000
```

API 文档：http://localhost:8000/docs

### 2. 前端

```bash
cd frontend
npm install
npm run dev            # → http://localhost:5173
```

## 日常启动

首次已安装依赖，后续只需分别启动后端和前端即可：

**启动后端**（二选一）
```bash
# 方式一：直接在 backend 目录下运行
cd backend
python app.py
```
```bash
# 方式二：VS Code 中右键 backend/app.py → "在终端中运行 Python 文件"
```

**启动前端**
```bash
cd frontend
npm run dev
```

两个终端都保持运行，浏览器访问 http://localhost:5173 即可使用。

## 功能概览

### 知识图谱页（首页）
- **力导向可视化** — vis-network 渲染，节点按三层分色（蓝=概念/绿=案例/黄=问题）
- **8 种关系类型** — 包含、前置知识、属于层、相关案例、关联试题、应用于、对比、依赖，各有不同颜色。其中：
  - 包含：A 是 B 的组成部分/子概念（如 TCP 包含 拥塞控制）
  - 前置知识：学 B 之前应先学 A（如 传输层概述 → TCP）
  - 依赖：B 需要 A 才能工作，但 A 不属于 B（如 端口号 → TCP）
  - 对比：两个概念互相对照（双向箭头）
- **点击节点** — 右侧抽屉展示完整信息：基本属性、Markdown 描述、多张配图、B站/YouTube 视频嵌入
- **智能关联** — 点击案例/问题节点自动拉取案例正文或试题详情（题目+选项+答案+解析）
- **筛选搜索** — 按章节/层次筛选，关键词搜索
- **导入导出** — JSON 格式一键导入导出

### 知识点管理
- 表格展示全部知识点，支持 预览 / 编辑 / 删除
- **预览** — 抽屉展示知识点完整信息（配图、视频、关联关系）
- **编辑** — 弹窗编辑所有属性，底部可管理关联关系（增删边）
- 支持 Markdown 描述、多张配图、视频链接

### 案例管理
- 案例 CRUD，Markdown 正文渲染
- 章节、难度、标签、配图、视频字段
- 预览抽屉展示格式化内容

### 试题管理
- 试题 CRUD，支持 6 种题型
- 题目名称、章节、关键词、选项、答案、解析
- 关联知识点管理

## 项目结构

```
├── backend/                  # FastAPI 后端
│   ├── app.py                # 主入口（含导入导出接口）
│   ├── models.py             # Pydantic 数据模型
│   ├── database.py           # JSON 文件 CRUD 操作层
│   ├── routes/               # API 路由
│   │   ├── nodes.py          # 知识点 CRUD
│   │   ├── edges.py          # 关系 CRUD
│   │   ├── cases.py          # 案例 CRUD
│   │   ├── questions.py      # 试题 CRUD
│   │   └── graph.py          # 图谱查询 & 统计
│   ├── data/                 # JSON 数据文件
│   │   ├── nodes.json        # 知识点（200+）
│   │   ├── edges.json        # 关系
│   │   ├── cases.json        # 案例（20+）
│   │   └── questions.json    # 试题（600+）
│   └── requirements.txt
│
├── frontend/                 # React + Vite + TypeScript
│   ├── src/
│   │   ├── pages/
│   │   │   ├── GraphPage.tsx      # 图谱可视化（vis-network）
│   │   │   ├── NodesPage.tsx      # 知识点管理（预览+关联管理）
│   │   │   ├── CasesPage.tsx      # 案例管理（Markdown 渲染）
│   │   │   └── QuestionsPage.tsx  # 试题管理
│   │   ├── services/api.ts        # API 调用层
│   │   ├── types/index.ts         # TypeScript 类型定义
│   │   ├── App.tsx                # 布局与路由
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
└── 要求.txt                  # 需求文档
```

## 数据模型

### 知识点 (Node)
```json
{
  "id": "tcp",
  "name": "TCP 协议",
  "type": "协议",
  "layer": "概念层",
  "chapter": "传输层",
  "description": "传输控制协议（TCP）是一种面向连接的、可靠的...",
  "keywords": ["可靠传输", "拥塞控制", "流量控制"],
  "difficulty": 3,
  "image_urls": ["https://example.com/tcp-header.png"],
  "video_url": "https://www.bilibili.com/video/BV1c4411d7jb"
}
```

### 关系 (Edge)
```json
{
  "id": "edge_001",
  "source": "tcp",
  "target": "congestion_control",
  "relation": "包含",
  "description": "TCP 包含拥塞控制机制"
}
```

### 案例 (Case)
```json
{
  "id": "case_tcp_wireshark",
  "title": "Wireshark TCP 协议分析",
  "description": "使用 Wireshark 捕获 TCP 通信报文...",
  "chapter": "传输层",
  "difficulty": 3,
  "content": "## 实验目的\n1. 掌握 Wireshark...",
  "tags": ["Wireshark", "TCP"],
  "image_urls": [],
  "video_url": null
}
```

### 试题 (Question)
```json
{
  "id": "q_tcp_001",
  "name": "TCP 三次握手过程",
  "title": "TCP 三次握手过程中，第二次握手报文包含的标志位是？",
  "type": "单选题",
  "chapter": "传输层",
  "description": "关于 TCP 三次握手中 SYN 和 ACK 标志位变化的题目",
  "keywords": ["三次握手", "SYN", "ACK"],
  "options": ["A. SYN", "B. ACK", "C. SYN+ACK", "D. FIN"],
  "answer": "C",
  "explanation": "第二次握手是服务器向客户端发送 SYN+ACK 报文...",
  "difficulty": 2
}
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | React 18 + TypeScript |
| 构建工具 | Vite 5 |
| UI 组件 | Ant Design 5 |
| 图谱可视化 | vis-network |
| Markdown 渲染 | react-markdown + remark-gfm |
| 后端框架 | FastAPI (Python) |
| 数据存储 | JSON 文件（可随时替换为数据库） |

## 核心指标

| 指标 | 要求 | 状态 |
|------|------|------|
| 知识点 | >=200 个 | 待填充（现有 15 示例） |
| 试题 | >=600 道 | 待填充（现有 5 示例） |
| 案例 | >=20 个 | 待填充（现有 3 示例） |
| 章节 | 3 篇 10 章 | 已实现 |
| 关系类型 | 8 种 | 已实现 |
| 三层结构 | 概念/案例/问题 | 已实现 |
| CRUD | 完整增删改查 | 已实现 |
| 可视化 | 力导向交互图 | 已实现 |
| 搜索筛选 | 章节/层次/关键词 | 已实现 |
| 导入导出 | JSON 格式 | 已实现 |

## 待完成

1. 按 3 篇 10 章扩充知识点至 200+
2. 收集试题至 600+ 道
3. 完善案例库至 20+ 个
4. 撰写实习报告（8.30 前）
5. 每周进度汇报
