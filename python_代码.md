# 解释器
### __pycache__
> cpython-35，cpython代表的是c语言实现的Python解释器，-35代表的是版本为3.5版

> Python解释器已经把编译的字节码放在__pycache__文件夹中，如果被调用的模块未发生改变，以后再次运行的话，那就直接跳过编译这一步，直接去__pycache__文件夹中去运行相关的 *.pyc 文件，大大缩短了项目运行前的准备时间。

> 解释器的具体工作：
1、完成模块的加载和链接；
2、将源代码编译为PyCodeObject对象(即字节码)，写入内存中，供CPU读取；
3、从内存中读取并执行，结束后将PyCodeObject写回硬盘当中，也就是复制到.pyc或.pyo文件中，以保存当前目录下所有脚本的字节码文件。

### #!/usr/bin/env python  
> [见解释](https://zhuanlan.zhihu.com/p/262456371)
  需了解一些linux命令



# 编码
指定文档编码
```python
#coding=utf-8
#! -*- coding:utf-8 -*-
```