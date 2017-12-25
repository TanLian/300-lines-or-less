#!/usr/bin/env python
#coding: utf-8

from .thread_pool import ThreadPool, Job
import os
import time

BASE_DIR = '/root/test/'

def deal_func(p):
    print 'dealing with ' + p
    time.sleep(2)

    return {'p':os.path.basename(p), 'size':os.stat(p).st_size}

def deal_func2(name, age=25, sex='male', id=13):
    return {'name':name, 'age':age, 'sex':sex, 'id':id}


def main():
    pool = ThreadPool(10)

    for fd in os.listdir(BASE_DIR):
        pool.add_job(Job(deal_func, os.path.join(BASE_DIR, fd)))

    pool.add_job(Job(deal_func2, 'bruce'))
    pool.add_job(Job(deal_func2, 'jack', 26))
    pool.add_job(Job(deal_func2, 'tom', 24, 'male'))
    pool.add_job(Job(deal_func2, 'alice', 21, 'female', id=14))

    pool.start()

    pool.wait_until_complete()

    print pool.get_result()

if __name__ == '__main__':
    start = time.time()
    main()
    print 'cost time: ' + str(time.time() - start)

