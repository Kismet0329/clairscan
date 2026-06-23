@echo off
call venv\Scripts\activate
python -m celery -A tasks.scanner_task worker --pool=solo --loglevel=info
pause