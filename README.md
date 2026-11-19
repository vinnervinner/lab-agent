# 智能实验室预约系统

一个面向实验室场景的全栈预约管理系统，提供用户认证、实验室与设备管理、预约申请、管理员审核，以及基于大模型 Agent 的自然语言操作入口。

## 功能概览

- 用户注册、登录与 JWT 鉴权
- 实验室、设备和开放时间查询
- 实验室/设备预约、取消和管理员审核
- 基于 LangGraph 的智能 Agent 对话
- 知识库检索：安全规范、预约规则、开放时间等
- 文件上传与静态资源访问
- 过期预约自动扫描
- Agent 运行日志：工具调用、执行状态、耗时和异常摘要

## 技术栈

### 后端

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy
- MySQL（通过 `DATABASE_URL` 配置）
- LangGraph、LangChain OpenAI
- ChromaDB 与 sentence-transformers

### 前端

- Vue 3
- Vite
- Element Plus
- Axios
- Vue Router

## 项目结构

```text
lab-agent/
├── backend/
│   ├── app/
│   │   ├── api/          # HTTP API
│   │   ├── models/       # 数据库模型
│   │   ├── schemas/      # 请求和响应模型
│   │   ├── services/     # 业务逻辑与 Agent
│   │   └── utils/        # JWT、密码和日志工具
│   ├── data/kb/          # 知识库文档
│   ├── requirements.txt
│   └── .env              # 本地配置，不提交到 Git
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

## 本地运行

### 1. 配置后端

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

在 `backend/.env` 中配置以下变量：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/lab_agent
JWT_SECRET_KEY=请替换为随机密钥
JWT_EXPIRE_HOURS=24
LLM_API_KEY=你的模型服务密钥
LLM_BASE_URL=模型服务地址
LLM_MODEL=模型名称
```

### 2. 启动后端

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动后可访问：

- API：`http://localhost:8000`
- Swagger 文档：`http://localhost:8000/docs`

### 3. 启动前端

```powershell
cd frontend
npm install
npm run dev
```

前端默认地址为 `http://localhost:5173`。

## Agent 日志

Agent 调试日志写入：

```text
backend/logs/agent.log
```

日志使用 Python `RotatingFileHandler`：单个文件达到 5MB 后自动轮转，并保留 3 个历史文件。日志记录用户 ID、请求成功状态、工具名称、工具执行状态、耗时和异常摘要，不记录用户原始对话内容。`backend/logs/` 已加入 `.gitignore`，不会上传到仓库。

预约、取消和审核等关键业务数据仍由业务表保存，运行调试日志与业务数据分开管理。

## 安全说明

- 不要提交 `backend/.env`、数据库文件、上传文件或模型密钥。
- 生产环境请替换默认密钥，并限制 CORS 来源。
- 生产环境建议将日志目录交给集中式日志系统或定期归档。

## 介绍

> 我为 Agent 增加了带轮转和保留期限的运行日志，记录工具调用、执行状态、耗时和异常摘要，但没有把所有调试信息永久写入数据库。预约、取消、审核等关键业务操作由业务数据单独保留。这样既便于问题排查，也能控制存储量并减少用户隐私暴露。
