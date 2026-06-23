# ClairScan - AI 增强漏洞扫描器

基于 DeepSeek 大模型的智能渗透测试辅助平台，支持资产探测、AI 漏洞研判、自适应 Payload 生成与中文报告自动输出。

## 功能
- 异步端口扫描与服务发现
- AI 驱动漏洞分析（SQL注入/XSS/信息泄露/未授权访问）
- 动态生成绕过 WAF 的测试载荷
- 一键导出专业中文渗透测试报告（PDF）

## 技术栈
Python · FastAPI · Celery · Redis · DeepSeek API · pdfkit

## 快速开始
1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 复制 `.env.example` 为 `.env`，填入 DeepSeek API Key
4. 启动 Redis、Celery Worker、FastAPI
5. 访问 `http://127.0.0.1:8000/docs` 使用

详细文档请参考下方说明。

## 许可
MIT License