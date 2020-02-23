import multiprocessing
debug = True
loglevel = 'info'
bind = '0.0.0.0:8787'
pidfile = 'log/gunicorn.pid'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
certfile = '/etc/ssl/private/letsencrypt-domain.pem'
keyfile = '/etc/ssl/private/letsencrypt-domain.key'
errorlog = '-'  # stderr
