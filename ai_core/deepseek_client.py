import asyncio
from openai import AsyncOpenAI, APIError, RateLimitError
from typing import List, Dict
from config import settings   # 改用 settings 对象，不依赖环境变量

class DeepSeekClient:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or settings.ai_api_key
        self.base_url = base_url or settings.ai_base_url
        self.model = model or settings.ai_model
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def ask(self, prompt: str, system: str = "", temperature: float = 0.7) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(3):
            try:
                resp = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=4096
                )
                return resp.choices[0].message.content
            except RateLimitError:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)
            except APIError:
                if attempt == 2:
                    raise
                await asyncio.sleep(1)

    async def chat(self, messages: List[Dict[str, str]], system: str = "") -> str:
        full = [{"role": "system", "content": system}] if system else []
        full.extend(messages)
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=full,
            temperature=0.7,
            max_tokens=4096
        )
        return resp.choices[0].message.content