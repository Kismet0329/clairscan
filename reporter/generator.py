import markdown
from pathlib import Path
from ai_core.deepseek_client import DeepSeekClient

async def generate_report(vulns: list, client: DeepSeekClient = None) -> str:
    if client is None:
        client = DeepSeekClient()
    system = "你是一位专业渗透测试报告撰写人，输出Markdown格式。"
    user = f"根据以下漏洞列表生成渗透测试报告，含综述、漏洞详情、修复建议：\n{vulns}"
    md = await client.ask(user, system=system)
    return md

def markdown_to_pdf(md_text: str, output_path: str):
    # 延迟导入 pdfkit，避免 Celery 启动时加载
    import pdfkit
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    full_html = f"""
<html>
<head><meta charset="utf-8">
<style>
    body {{ font-family: "Microsoft YaHei", sans-serif; margin: 2cm; }}
    h1 {{ color: #d32f2f; border-bottom: 2px solid #d32f2f; }}
    h2 {{ color: #1976d2; }}
    pre {{ background: #f5f5f5; padding: 10px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
</style>
</head>
<body>{html}</body>
</html>
"""
    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
        'page-size': 'A4',
        'margin-top': '15mm',
        'margin-bottom': '15mm'
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdfkit.from_string(full_html, output_path, options=options)