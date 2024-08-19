# Gunicorn configuration file
import multiprocessing

# Port is specified by the PORT environment variable in Render
bind = "0.0.0.0:$PORT"

# Use multiple workers to handle requests
workers = multiprocessing.cpu_count() * 2 + 1

# Use threads for concurrency
threads = 2

# Timeout for worker processes
timeout = 120

# Access log - records incoming HTTP requests
accesslog = "-"

# Error log - records Gunicorn server goings-on
errorlog = "-"

# Whether to send Django output to the error log 
capture_output = True

# How verbose the Gunicorn error logs should be 
loglevel = "info"