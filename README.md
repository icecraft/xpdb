基于标准库 bdb.py 和 pdb.py 构建

一： 增加添加源代码目录功能
      source dir A ------- __init__.py
                 '
		 '--------  sr1.py
		 '
		 '--------  dir B ---- sr2.py
      可以直接用 break "src2.py":11|funcname [condition] 来设置断点


二： 增加 watch variable 功能：
     1	class A(object):
     2	    def __init__(self, value=0):
     3	        self.value = value
     4	
     5	    def set_value(self, value):
     6	        self.value = value
     7	
     8	
     9	class B(object):
    10	    def __init__(self, my_a):
    11	        self.my_a = my_a
    12	
    13	    def set_a(self, value):
    14	        self.my_a.set_value(value)
    15	
    16	a = A()
    17	b = B(a)           ---- 假设在此处增加断点
    18
    19	
    20	def uu():
    21	    for i in range(8):
    22	        if i %3 == 0:
    23	            b.set_a(i)    ----- i = 3, 6, 9 时会触发断点
    24	
    25	        print i
    26	
    27	
    28	uu()
    29	
        
    具体的执行结果如下：
     1	> /home/lisp/src/xpdb/cc.py(1)<module>()
     2	-> class A(object):
     3	(Pdb) n
     4	> /home/lisp/src/xpdb/cc.py(9)<module>()
     5	-> class B(object):
     6	(Pdb) n
     7	> /home/lisp/src/xpdb/cc.py(16)<module>()
     8	-> a = A()
     9	(Pdb) n
    10	> /home/lisp/src/xpdb/cc.py(17)<module>()
    11	-> b = B(a)
    12	(Pdb) n
    13	> /home/lisp/src/xpdb/cc.py(18)<module>()
    14	-> import sys
    15	(Pdb) watch a.value
    16	Succ to Add Watch Point
    17	(Pdb) c
    18	0
    19	1
    20	2
    21	 WatchPoint a.value: Old Value = 0, New Value = 3   --- 触发断点
    22	> /home/lisp/src/xpdb/cc.py(25)uu()
    23	-> print i
    24	(Pdb) c
    25	3
    26	4
    27	5
    28	 WatchPoint a.value: Old Value = 3, New Value = 6   --- 触发断点
    29	> /home/lisp/src/xpdb/cc.py(25)uu()
    30	-> print i
    31	(Pdb) c
    32	6
    33	7
    34	8



三：增加步进功能：
    next nums  
    step nums  (不能精确控制， 因为 cPython 内部调试框架会处理 call 和 return 等事件.\
导致当有 函数调用等事件发生时会进入 pdb 交互式环境）

    step/next nums (如果 nums 是负数则当 nums = 1 处理)

四：增加 finish 命令
    1：功能等同与 gdb finish 命令  
    2：如果 while 或者 for 循环运行模块命名空间则不会有任何效果(运行在函数命名空间里才有效)，如
        xxx.py
	   '
	   '
	   '---  import sys
	         while i in range(9):
		     print i

                                        ------ 在这个 while 循环体内调用 finish 命令将没有任何作用

		     print i*2
		     
			    
   3: 注意对以下代码（不完全）
def uu():
   for j in range(3): 
    for i in range(2):
        if i %3 == 0:
            b.set_a(i)
        print i
   i = 3*2       

uu()


(Pdb) s
> /home/lisp/src/xpdb/cc.py(22)uu()
-> for j in range(3):                    
(Pdb) finish                              --- 在此处 执行finish 命令将会finish 掉 函数 uu而不是 for j in range(3) 循环 【因为 pdb 提示的是下一行将运行的代码，
0                                            即此时还没有进入 for j in range(3) 内， 所以 finish 掉函数 uu 而不是 for 循环】
1
0
1
0
1
The program finished and will be restarted


五：增加命令 'shell'
    invoke bash 进入交互式环境
    

待增加功能：
    1： 输出格式的美化
        如 （Pdb） while f: print f; f = f.f_back  将被替换为
	    while  f:
	    ------ print f
	    ------ f = f.f_back
	    ------

    2: 支持自定义命令：
        如 gdb 哪有的自定义命令和从配置文件中读取已有的命令定义


    3: 支持设置变量值



	
