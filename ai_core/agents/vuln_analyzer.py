import json
from ai_core.deepseek_client import DeepSeekClient

SYSTEM_PROMPT = """你是一位资深网络安全专家。根据提供的HTTP响应，分析是否存在安全漏洞。
严格遵守以下JSON输出格式，不要附加任何解释：
{
  "is_vulnerable": bool,
  "vuln_type": "SQL注入/XSS/信息泄露/未授权访问/其他",
  "severity": "high/medium/low",
  "evidence": "响应中的具体证据，若无则为空字符串",
  "recommendation": "修复建议"
}
规则：
1. 响应体含数据库错误（如SQL syntax, mysql_fetch, ORA-）可能是SQL注入。
2. 响应含堆栈跟踪、服务器路径、内网IP为信息泄露。
3. 需认证的页面直接返回数据为未授权访问。
4. 证据不足时 is_vulnerable 必须为 false。
"""

class VulnAnalyzer:
    def __init__(self, client: DeepSeekClient = None):
        self.client = client or DeepSeekClient()

    async def analyze_response(self, method: str, url: str, status: int, headers: dict, body: str) -> dict:
        prompt = f"""
HTTP Method: {method}
URL: {url}
Status Code: {status}
Headers: {json.dumps(headers, indent=2)}
Body (前2000字符): {body[:2000]}
"""
        raw = await self.client.ask(prompt, system=SYSTEM_PROMPT, temperature=0.3)
        try:
            return json.loads(raw)
        except:
            return {"is_vulnerable": False, "vuln_type": "", "severity": "low", "evidence": "", "recommendation": ""}