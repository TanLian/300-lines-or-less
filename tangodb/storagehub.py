# -*- coding: utf-8 -*-
#Author: tanlian

import const

class TableNotExist(Exception):
    pass

class DocIdInvalid(Exception):
    pass

class StorageHub(object):
    def __init__(self, storage, table=const.DEFAULT_TABLE):
        self.storage = storage
        self.table = table

    def read(self, docid=None):
        data = self.storage.read()
        if self.table not in data:
            raise TableNotExist

        if docid and not isinstance(docid, int):
            raise DocIdInvalid

        return data[self.table][docid] if docid else data[self.table]

    def write(self, document):
        try:
            data = self.read()
        except TableNotExist:
            data = {}
        data[document.docId] = document

        content = self.storage.read()
        content[self.table] = data
        self.storage.write(content)

    def deleteDocument(self, docid):
        content = self.storage.read()
        del content[self.table][docid]
        self.storage.write(content)