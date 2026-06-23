from celery import Celery
from config import settings
from orchestrator import run_full_scan

app = Celery(
    'scanner',
    broker=settings.redis_url,
    backend=settings.redis_url
)

@app.task
def scan_targets(targets: list):
    import asyncio
    return asyncio.run(run_full_scan(targets))