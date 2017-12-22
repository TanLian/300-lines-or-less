# -*- coding: utf-8 -*-
#Author: tanlian

from abc import ABCMeta, abstractmethod
import os
import json
import platform

class NotImplementError(Exception):
    pass

class storage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self):
        raise NotImplementError

    @abstractmethod
    def write(self, data):
        raise NotImplementError

class LocalFileStorage(storage):
    def __init__(self, createDirs=True, **kwargs):
        super(LocalFileStorage, self).__init__()

        default_path = 'D:\\db.json' if platform.system().lower() == 'windows' else '/tmp/db.json'
        path = kwargs.pop('path', default_path)

        self._touch(path, createDirs)
        self.fd = open(path, 'r+')
        self.kwargs = kwargs

    def _get_file_size(self):
        self.fd.seek(0, os.SEEK_END)
        size = self.fd.tell()
        self.fd.seek(0)
        return  size

    def _touch(self, path, createDirs):
        if not path or not path.strip():
            raise Exception('Path can not be null.')
        baseDir = os.path.dirname(path)
        if not os.path.exists(baseDir):
            if not createDirs:
                raise Exception(baseDir + ' does not exist, you need to set createDirs to True')
            os.makedirs(baseDir)
        if not os.path.exists(path):
            os.mknod(path)

    def read(self):
        return json.load(self.fd) if self._get_file_size() else {}

    def write(self, data):
        self.fd.seek(0)
        dataSerialized = json.dumps(data, **self.kwargs)
        self.fd.write(dataSerialized)
        self.fd.flush()
        self.fd.truncate()

    def close(self):
        self.fd.close()

class MemoryStorage(storage):
    def __init__(self):
        super(MemoryStorage, self).__init__()
        self.data = '{}'

    def read(self):
        return json.loads(self.data)

    def write(self, data):
        self.data = json.dumps(data)
