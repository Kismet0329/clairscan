from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from typing import Optional

# Celery 相关导入
from tasks.scanner_task import app as celery_app, scan_targets

# AI 分析相关导入
from ai_core.deepseek_client import DeepSeekClient
from ai_core.agents.vuln_analyzer import VulnAnalyzer
from ai_core.agents.payload_gen import SQLiPayloadGenerator, XSSPayloadGenerator

# FastAPI 应用
app = FastAPI(title="ClairScan - AI 增强漏洞扫描器")

# 全局 AI 客户端（复用，减少重复初始化）
ai_client = DeepSeekClient()
vuln_analyzer = VulnAnalyzer(client=ai_client)
sqli_gen = SQLiPayloadGenerator(client=ai_client)
xss_gen = XSSPayloadGenerator(client=ai_client)

# ==================== 任务存储 ====================
tasks_db = {}

# ==================== 请求模型 ====================
class ScanRequest(BaseModel):
    targets: list[str]

class SqliPayloadRequest(BaseModel):
    context: str = "字符型"          # 注入点类型：数字型/字符型/搜索型等
    db_type: str = "MySQL"          # 数据库类型：MySQL/PostgreSQL/MSSQL等

class XssPayloadRequest(BaseModel):
    context: str = "HTML标签内"     # 注入上下文：HTML标签内/属性中/JS字符串等

class AnalyzeRequest(BaseModel):
    method: str = "GET"
    url: str
    status: int = 200
    headers: dict = {}
    body: str = ""

# ==================== 扫描接口 ====================
@app.post("/scan")
async def create_scan(req: ScanRequest):
    task_id = str(uuid.uuid4())[:8]
    task = scan_targets.delay(req.targets)
    tasks_db[task_id] = task.id
    return {"task_id": task_id, "celery_id": task.id}

@app.get("/scan/{task_id}")
async def get_scan(task_id: str):
    celery_id = tasks_db.get(task_id)
    if not celery_id:
        return {"error": "Task not found"}
    result = celery_app.AsyncResult(celery_id)
    if result.ready():
        return {"status": "completed", "result": result.result}
    return {"status": "pending"}

# ==================== AI Payload 生成接口 ====================
@app.post("/payload/sqli")
async def generate_sqli_payload(req: SqliPayloadRequest):
    payloads = await sqli_gen.generate(context=req.context, db_type=req.db_type)
    return {"context": req.context, "db_type": req.db_type, "payloads": payloads}

@app.post("/payload/xss")
async def generate_xss_payload(req: XssPayloadRequest):
    payloads = await xss_gen.generate(context=req.context)
    return {"context": req.context, "payloads": payloads}

# ==================== 单项漏洞分析接口 ====================
@app.post("/analyze")
async def analyze_response(req: AnalyzeRequest):
    result = await vuln_analyzer.analyze_response(
        method=req.method,
        url=req.url,
        status=req.status,
        headers=req.headers,
        body=req.body
    )
    return result