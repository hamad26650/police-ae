"""
إعدادات Gunicorn للإنتاج
"""
import multiprocessing
import os

# عنوان الربط
# يقرأ المنفذ من متغير البيئة PORT، الافتراضي 8000
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# عدد العمال (workers)
workers = multiprocessing.cpu_count() * 2 + 1

# نوع العمال
worker_class = "sync"

# Timeout
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# Process naming
proc_name = "gov_services"

# Worker timeout
graceful_timeout = 30


