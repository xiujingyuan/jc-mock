#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/09
 @file: test_task.py
 @site:
 @email:
"""
import random
import time
from app import celery


@celery.task()
def log(msg):
    print(msg)
    return msg


@celery.task(bind=True)
def long_task(self):
    # total = random.randint(10, 50)
    # for i in range(total):
    #     self.update_state(state='处理中', meta={"current": i, "total": total})
    #     time.sleep(1)
    # return {"current": 100, "total": total, "result": "完成"}
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = 10
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                                  random.choice(adjective),
                                                  random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 10, 'total': 10, 'status': 'Task completed!',
            'result': 10}
