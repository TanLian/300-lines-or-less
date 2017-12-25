使用纯Python语言实现的线程池

声明一个线程池对象：
```python
pool = ThreadPool(10)
```
参数：int类型，线程池中初始线程对象的个数


添加任务到线程池中：
```python
pool.add_job(Job(func, args, kwargs))
```
一个任务就是一个Job对象，Job的第一个参数是处理函数，余下参数则是该处理函数的参数，如以下获取Job对象都是合法的
```python
Job(func, 1, 2, 3)
Job(func, 1, 2, name='Bruce', age=25)
```

调用start方法使得整个线程池开始工作
```python
pool.start()
```

等待所有的线程均执行结束
```python
pool.wait_until_complete()
```

获取结果
```python
print pool.get_result()
```
