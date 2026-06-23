import httpx
from typing import List, Dict
import asyncio

async def probe_services(targets: List[str], concurrency: int = 20) -> List[Dict]:
    sem = asyncio.Semaphore(concurrency)  # 这里需要 import asyncio，粘贴时补上
    async def _probe(url: str):
        async with sem:
            try:
                async with httpx.AsyncClient(verify=False, timeout=5) as client:
                    resp = await client.get(url, follow_redirects=True)
                    return {
                        "url": url,
                        "status": resp.status_code,
                        "title": resp.text[:200],
                        "headers": dict(resp.headers)
                    }
            except:
                return {"url": url, "status": 0, "title": "", "headers": {}}

    tasks = [_probe(t) for t in targets]
    return await asyncio.gather(*tasks)