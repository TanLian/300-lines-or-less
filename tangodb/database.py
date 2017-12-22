# -*- coding: utf-8 -*-
#Author: tanlian

import const
from storagehub import StorageHub
from storage import LocalFileStorage

class Document(dict):
    def __init__(self, docId, value):
        super(Document, self).__init__()
        self.update(value)
        self.docid = docId

    @property
    def docId(self):
        return  self.docid

class Table(object):

    def __init__(self, storage, tableName):
        self.storagehub = StorageHub(storage, tableName)

    def _get_netxt_dicid(self):
        next_id = -1
        try:
            content = self.storagehub.read()
            next_id = int(max(content.keys(), key = lambda x:int(x)))
        except Exception:
            pass

        return next_id + 1

    def insert(self, document):
        if not isinstance(document, dict):
            raise Exception('document must be a dict')
        doc = Document(self._get_netxt_dicid(), document)
        self.storagehub.write(doc)

    def remove(self, cond=None, docids=None):
        if not cond and not docids:
            raise Exception('One of cond and docids is required.')
        if cond and docids:
            raise Exception('You can not set both cond and docids.')
        if cond:
            ids = self._get_docids_by_cond(cond)
            return self.remove(cond=None, docids=ids)

        for docid in docids:
            self.storagehub.deleteDocument(docid)

    def update(self, values, cond=None, docids=None):
        if not isinstance(values, dict):
            raise Exception('values must be a dict.')
        if not cond and not docids:
            raise Exception('One of cond and docids is required.')
        if cond and docids:
            raise Exception('You can not set both cond and docids.')
        if cond:
            ids = self._get_docids_by_cond(cond)
            return self.update(values, cond=None, docids=ids)

        content = self.storagehub.read()
        for docid in docids:
            new_value = content[docid]
            new_value.update(values)
            self.storagehub.write(Document(docid, new_value))

    def _get_docids_by_cond(self, cond=None):
        content = self.storagehub.read()
        if not cond:
            return content.keys()
        return [k for k in content if self._is_sub_dict(content[k], cond)]

    def _is_sub_dict(self, d, sub_d):
        for k in sub_d:
            if k not in d or d[k] != sub_d[k]:
                return False
        return True

    def search(self, **kwargs):
        result = []
        content = self.storagehub.read()
        for k in content:
            if self._is_sub_dict(content[k], kwargs):
                result.append(content[k])
        return result


class TangoDB(object):
    def __init__(self, storage=LocalFileStorage, **kwargs):
        self.storage = storage(**kwargs)

    def gettable(self, tableName=const.DEFAULT_TABLE):
        return Table(self.storage, tableName)