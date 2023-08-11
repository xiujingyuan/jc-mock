#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/09/03
 @file: gunicorn_config.py
 @site:
 @email:
"""
import multiprocessing
import gevent.monkey

gevent.monkey.patch_all()

bind = '0.0.0.0:5102'

# workers = multiprocessing.cpu_count() * 2 * 1
workers = 1
# threads = multiprocessing.cpu_count() * 2
threads = 1
backlog = 2048

preload_app = True

worker_class = "gevent"

worker_connections = 1000

debug = False

reload = True

loglevel = 'info'

proc_name = 'jc_mock'

capture_output = True

pidfile = '/data/www/wwwroot/jc-mock/logs/gunicon/gunicorn.pid'

errorlog = '/data/www/wwwroot/jc-mock/logs/gunicon/error.log'

logfile = '/data/www/wwwroot/jc-mock/logs/gunicon/info.log'

accesslog = '/data/www/wwwroot/jc-mock/logs/gunicon/access.log'
