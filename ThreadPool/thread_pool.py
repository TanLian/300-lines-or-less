#!/usr/bin/env python
#coding: utf-8

from threading import Thread
import Queue
import logging

class Job(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

class Worker(Thread):
    def __init__(self, task_queue, result_queue):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            try:
                job = self.task_queue.get()
                if job is None:
                    break
                ret = job.func(*job.args, **job.kwargs)
            except Exception as e:
                logging.warning('Failed to execute task: %s' % e)
            finally:
                if ret:
                    self.result_queue.put(ret)
                self.task_queue.task_done()

class ThreadPool(object):
    def __init__(self, nworker=10):
        self.nworker = nworker
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.threads = []
        self.init_threads(nworker)
        self.finished = False

    def init_threads(self, nworker):
        for i in xrange(self.nworker):
            self.threads.append(Worker(self.task_queue, self.result_queue))

    def start(self):
        for worker in self.threads:
            worker.start()

    def add_job(self, job):
        if not isinstance(job, Job):
            raise Exception('job must be a instance of Job')
        self.task_queue.put(job)

    def get_result(self):
        if not self.finished:
            raise Exception('Please wait for the execution finished.')
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results

    def wait_until_complete(self):
        self.task_queue.join()

        for i in xrange(self.nworker):
            self.task_queue.put(None)
        self.finished = True