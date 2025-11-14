"""
إعدادات Gunicorn للإنتاج
"""
import multiprocessing

# عنوان الربط
bind = "127.0.0.1:8000"

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

