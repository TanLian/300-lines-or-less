# TangoDB
A document oriented database written in pure python.It's very lighweight.It stores data in files or in memory, depending on your choice of storage engine.

# Example code
import lib

```python
from tangodb import TangoDB
from tangodb.storage import LocalFileStorage, MemoryStorage
```

get a database object and a table object

```python
db = TangoDB(storage=LocalFileStorage, path='/root/db.json')
#db = TangoDB(storage=MemoryStorage)
table = db.gettable()	#get default table
```

insert

```python
table.insert({'name':'tom', 'age':25})
table.insert({'name':'joe', 'age':23, 'sex':'male'})
table.insert({'name':'alice', 'age':21, 'sex':'female'})
```

remove

```python
table.remove(cond={'name':'joe'})
```

update

```python
table.update({'age':26, 'sex':'male'}, cond={'name':'tom'})
```

search

```python
print table.search(name='alice')
```

