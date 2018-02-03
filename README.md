工作之余写的Python代码！！

## TangoDB
轻量的（大概200行代码）使用纯Python写的文档型数据库。
[查看详情](https://github.com/TanLian/300-lines-or-less/tree/master/tangodb)

## ThreadPool
使用纯Python语言实现的**线程池**

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

## 模板引擎

文档地址： https://juejin.im/post/5a4c93a7f265da430b7ba1d4

## 统计一个目录下的文件个数（可递归统计子目录）

用法：

```
[root@WUKONG ~]# python number_of_files.py --help
usage: number_of_files.py [-h] [--recursive] [--hidden]
                          [--maxlayers MAXLAYERS] [--timeout TIMEOUT]
                          path

Gets the number of files under the specified folder

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  --recursive, -r       Recursive statistics subdirectory
  --hidden, -H          including Hidden files.
  --maxlayers MAXLAYERS, -m MAXLAYERS
                        maxlayers
  --timeout TIMEOUT, -t TIMEOUT
                        Quit when timeout
```

用法示例:

```
[root@WUKONG tangodb]# python ../number_of_files.py ./
14
[root@WUKONG tangodb]# ls ./ | wc -l
14
```