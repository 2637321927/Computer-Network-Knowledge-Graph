"""
计算机网络知识图谱 - FastAPI 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import nodes, edges, cases, questions, graph

app = FastAPI(
    title="计算机网络知识图谱 API",
    description="面向《计算机网络》课程的三维知识图谱交互平台",
    version="1.0.0"
)

# CORS配置-允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(cases.router)
app.include_router(questions.router)
app.include_router(graph.router)


@app.get("/")
async def root():
    return {"message": "计算机网络知识图谱 API 服务运行中", "docs": "/docs"}


@app.post("/api/import")
async def import_data(data: dict):
    """批量导入数据"""
    from database import (
        _write_json, NODES_FILE, EDGES_FILE, CASES_FILE, QUESTIONS_FILE
    )
    if "nodes" in data:
        _write_json(NODES_FILE, data["nodes"])
    if "edges" in data:
        _write_json(EDGES_FILE, data["edges"])
    if "cases" in data:
        _write_json(CASES_FILE, data["cases"])
    if "questions" in data:
        _write_json(QUESTIONS_FILE, data["questions"])
    return {"message": "导入成功", "stats": {
        "nodes": len(data.get("nodes", [])),
        "edges": len(data.get("edges", [])),
        "cases": len(data.get("cases", [])),
        "questions": len(data.get("questions", [])),
    }}


@app.get("/api/export")
async def export_data():
    """批量导出所有数据"""
    from database import (
        _read_json, NODES_FILE, EDGES_FILE, CASES_FILE, QUESTIONS_FILE
    )
    return {
        "nodes": _read_json(NODES_FILE),
        "edges": _read_json(EDGES_FILE),
        "cases": _read_json(CASES_FILE),
        "questions": _read_json(QUESTIONS_FILE),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
