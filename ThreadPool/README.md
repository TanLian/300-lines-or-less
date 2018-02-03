使用纯Python语言实现的线程池

新建一个线程池对象：

```python
pool = ThreadPool(10)
```
参数：int型，线程池中初始线程对象的个数


添加任务到线程池中：

```python
pool.add_job(Job(func, args, kwargs))
```

一个任务就是一个Job对象，Job定义如下：

```
class Job(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
```

Job的第一个参数是处理函数，余下参数则是该处理函数的参数，如以下Job对象都是合法的

```python
Job(func, 1, 2, 3)
Job(func, 1, 2, name='Bruce', age=25)
```

调用start方法使得整个线程池开始工作

```python
pool.start()
```

等待所有线程执行结束

```python
pool.wait_until_complete()
```

获取结果

```python
print pool.get_result()
```
