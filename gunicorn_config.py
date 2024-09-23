import os



workers = int(os.environ.get('GUNICORN_PROCESSES', '4'))

threads = int(os.environ.get('GUNICORN_THREADS', '8'))

timeout = int(os.environ.get('GUNICORN_TIMEOUT', '800'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8001')



forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }