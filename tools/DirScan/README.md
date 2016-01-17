# DirScan

##需求
   python 2.x
   
   requests
   
   ProgressBar

一些智能错误关键字判断 和网站域名备份文件

希望多提意见:)
```
croxy@Dell ~/DirScan> python dirscan.py


 mmmm     "            mmmm
 #   "m mmm     m mm  #"   "  mmm    mmm   m mm
 #    #   #     #"  " "#mmm  #"  "  "   #  #"  #
 #    #   #     #         "# #      m"""#  #   #
 #mmm"  mm#mm   #     "mmm#" "#mm"  "mm"#  #   #



   Author: RickGray@0xFA-Team          |
           Cupport@0xFA-Team           |
   Create: 2015-10-25                  |
   Update: 2015-10-25                  |
  Version: 0.2-alpha                   |
_______________________________________|

Usage: dirscan.py [options] http://www.c-chicken.cc

Options:
  -h, --help            show this help message and exit
  -t THREADS_NUM, --threads=THREADS_NUM
                        Number of threads. default = 10
  -e EXT, --ext=EXT     You want to Scan WebScript. default is php
```



##v0.2

**1. 避免备份文件过大所以使用stream探测备份文件**

**2. 去掉长度为0即为404判断**

**3. 增加与错误页面进行相似度识别 如果相似度达到90% 即判断为404页面**

**4. 增加fast.py 使用head探测 速度飞快:)**

**5. 解决线程kill不掉的问题**

**6. 增加pldirsca.py 在target.txt放入你的目标 进行批量扫描**

**7. 感谢LGrok添加进度查看**

###感谢RickGray Ricter等人的帮助以及建议:)
