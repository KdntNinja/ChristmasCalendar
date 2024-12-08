# gunicorn_config.py
workers = 4  # Number of worker processes
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"  # Bind to all interfaces on port 8000
