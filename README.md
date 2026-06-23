# 🔍 ClairScan — AI 增强漏洞扫描与渗透测试辅助平台

基于 **DeepSeek 大模型** 的智能漏洞扫描工具，支持资产探测、AI 漏洞研判、自适应 Payload 生成与中文渗透报告自动导出。  
旨在辅助安全工程师提高渗透测试效率，尤其适用于日常手工测试与报告编写场景。

---

## 🚀 功能亮点

- **资产探测**：异步端口扫描 + HTTP 服务发现，替代 Nmap 基础功能。
- **AI 漏洞研判**：自动分析 HTTP 响应，识别 **SQL 注入、XSS、信息泄露、未授权访问** 等漏洞，并给出风险等级、证据和修复建议。
- **自适应 Payload 生成**：
  - SQL 注入载荷（根据注入点类型、数据库类型生成绕过 WAF 的测试向量）
  - XSS 载荷（根据上下文动态生成绕过过滤的脚本）
- **报告自动化**：一键生成规范的中文渗透测试报告，并导出 **PDF**。
- **异步任务系统**：基于 Celery + Redis 实现扫描任务队列，支持高并发场景。
- **API 服务化**：FastAPI 提供 RESTful 接口，自带 Swagger 文档，方便集成与演示。

---

## 🧰 技术栈

| 类别       | 技术                                |
|------------|-------------------------------------|
| 后端框架   | Python 3.11+ · FastAPI · Uvicorn    |
| AI 引擎    | DeepSeek API (Chat V3)              |
| 任务队列   | Celery · Redis                      |
| 异步扫描   | asyncio · httpx                      |
| 报告生成   | Markdown · pdfkit · wkhtmltopdf     |
| 开发辅助   | VS Code · Claude Code (仅辅助编码)  |

---

## ⚙️ 快速开始

### 前置依赖
- Python 3.11+
- Redis（Windows 下推荐 [Memurai](https://www.memurai.com/)）
- wkhtmltopdf（PDF 导出需要，[下载地址](https://wkhtmltopdf.org/downloads.html)）

### 安装与配置
```bash
# 1. 克隆仓库
git clone https://github.com/Kismet0329/clairscan.git
cd clairscan

# 2. 创建虚拟环境并安装依赖
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env 文件，填入你的 DeepSeek API Key 和 Redis 地址