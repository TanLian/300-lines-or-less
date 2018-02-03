#!/usr/bin/env python
#coding: utf-8

import argparse
import os
import logging
import sys
from threading import Thread

'''
python hello2.py /tmp(./  ../)  -r(--recursive) -m(--max-layers) -t(--timeout)
'''

class TimeoutError(Exception):
    pass

class Worker(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.setDaemon(True)
        self.func = func
        self.args = args
        self.result = 0

    def run(self):
        self.result = self.func(*self.args)

    @property
    def get_result(self):
        return self.result

def statistic_in_thread(timeout, path, recursive, hidden, maxlayers):
    files = []
    obj = Worker(recursive_statistic_dir, (path, recursive, hidden, maxlayers, 0, files))
    obj.start()
    if timeout:
        obj.join(timeout)
        if obj.isAlive():
            raise TimeoutError
    else:
        obj.join()

    print obj.get_result

def transfer_path(path):
    '''
    function:转换成绝对路径
    :param path:
    :return:
    '''
    if path.startswith('./'):
        return os.path.join(os.getcwd(), path[2:])
    if path.startswith('../'):
        return os.path.join(os.path.dirname(os.getcwd()), path[3:])
    return path

def recursive_statistic_dir(path, recursive, hidden, maxlayers, current_layer, files):
    if not files:
        files = []
    if maxlayers and current_layer >= maxlayers:
        return
    for item in os.listdir(path):
        p = os.path.join(path, item)
        if os.path.isdir(p):
            if recursive:
                recursive_statistic_dir(p, recursive, hidden, maxlayers, current_layer + 1, files)
        else:
            if os.path.basename(p).startswith('.'):
                if hidden:
                    files.append(p)
            else:
                files.append(p)
    return len(files)


def main():
    parser = argparse.ArgumentParser(description="Gets the number of files under the specified folder")
    parser.add_argument('path', default='./')

    parser.add_argument('--recursive', '-r', action='store_true', help='Recursive statistics subdirectory')
    parser.add_argument('--hidden', '-H', action='store_true', help='including Hidden files.')
    parser.add_argument('--maxlayers', '-m', help='maxlayers', type=int, default=0)
    parser.add_argument('--timeout', '-t', help='Quit when timeout', type=float, default=0)

    args = parser.parse_args()

    abs_path = transfer_path(args.path)

    if not os.path.exists(abs_path):
        logging.error('{path} does not exist.'.format(path = abs_path))
        sys.exit(-1)

    try:
        statistic_in_thread(args.timeout, abs_path, args.recursive, args.hidden, args.maxlayers)
    except TimeoutError:
        logging.error('time out')
        sys.exit(-1)
    except Exception as e:
        logging.error(e)
        sys.exit(-1)

if __name__ == '__main__':
    main()
