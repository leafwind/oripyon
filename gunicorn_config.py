import multiprocessing
debug = True
loglevel = 'info'
bind = '0.0.0.0:8443'  # telegram web hook only allow 80, 88, 443 and 8443 port
pidfile = 'gunicorn.pid'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
certfile = '/etc/ssl/private/letsencrypt-domain.pem'
keyfile = '/etc/ssl/private/letsencrypt-domain.key'
accesslog = '-'  # stdout
errorlog = '-'  # stderr
