import asyncio
import socket
from typing import List

async def scan_port(ip: str, port: int, sem: asyncio.Semaphore) -> int | None:
    async with sem:
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=1
            )
            writer.close()
            await writer.wait_closed()
            return port
        except:
            return None

async def scan_ports(ip: str, start: int = 1, end: int = 1024, concurrency: int = 10) -> List[int]:
    sem = asyncio.Semaphore(concurrency)
    tasks = [scan_port(ip, p, sem) for p in range(start, end+1)]
    results = await asyncio.gather(*tasks)
    return [p for p in results if p is not None]