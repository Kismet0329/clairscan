import asyncio
from scanner.port_scan import scan_ports
from scanner.http_probe import probe_services
from ai_core.agents.vuln_analyzer import VulnAnalyzer
from reporter.generator import generate_report, markdown_to_pdf
from config import settings

async def run_full_scan(targets: list) -> str:
    # 1. 端口扫描（这里简单处理，假设targets里是IP/域名）
    open_ports = {}
    for t in targets:
        print(f"Scanning ports on {t}")
        ports = await scan_ports(t, 1, 1024, settings.scan_max_concurrency)
        open_ports[t] = ports

    # 2. HTTP探测
    http_targets = []
    for ip, ports in open_ports.items():
        for p in ports:
            if p in [80, 443, 8080, 8443]:
                scheme = "https" if p in [443, 8443] else "http"
                http_targets.append(f"{scheme}://{ip}:{p}")

    print("Probing HTTP services...")
    responses = await probe_services(http_targets)

    # 3. AI漏洞分析
    analyzer = VulnAnalyzer()
    vulns = []
    for r in responses:
        if r["status"] != 0:
            result = await analyzer.analyze_response(
                "GET", r["url"], r["status"], r["headers"], r.get("title", "")
            )
            if result["is_vulnerable"]:
                vulns.append({"url": r["url"], **result})

    # 4. 生成报告
    print(f"Found {len(vulns)} vulnerabilities. Generating report...")
    if vulns:
        md = await generate_report(vulns)
        pdf_path = f"{settings.report_dir}/report.pdf"
        markdown_to_pdf(md, pdf_path)
        return {"vulnerabilities": vulns, "report_pdf": pdf_path}
    return {"vulnerabilities": [], "report_pdf": None}