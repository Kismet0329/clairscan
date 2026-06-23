from ai_core.deepseek_client import DeepSeekClient

class SQLiPayloadGenerator:
    def __init__(self, client: DeepSeekClient = None):
        self.client = client or DeepSeekClient()

    async def generate(self, context: str = "数字型", db_type: str = "MySQL") -> list:
        system = "你是一位高级渗透测试工程师，擅长WAF绕过。只返回payload列表，每行一个，不要序号和解释。"
        user = f"为{context}注入点，数据库{db_type}，生成5个可能绕过基础WAF的SQL注入payload："
        raw = await self.client.ask(user, system=system, temperature=0.8)
        return [line.strip() for line in raw.splitlines() if line.strip()]

class XSSPayloadGenerator:
    def __init__(self, client: DeepSeekClient = None):
        self.client = client or DeepSeekClient()

    async def generate(self, context: str = "HTML标签内") -> list:
        system = "你是一位XSS专家。只返回payload列表，每行一个，不要序号和解释。"
        user = f"在{context}上下文中，生成5个可能绕过过滤的XSS payload："
        raw = await self.client.ask(user, system=system, temperature=0.8)
        return [line.strip() for line in raw.splitlines() if line.strip()]