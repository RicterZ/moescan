#__author__ = 'croxy'
# -*- coding: UTF-8 -*-
#!/usr/bin/python

import requests
import optparse
import sys
import threading
import time
import Queue
import re
from progressbar import ProgressBar

header = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
'Accept-Encoding': 'gzip, deflate, compress',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
}


class DirScan:
    def __init__(self, target, threads_num, ext):
        self.target = target.strip()
        self.threads_num = threads_num
        self.ext = ext
        self.lock = threading.Lock()
        #outfile
        self.__load_dir_dict()
        self.errorpage = r'无法加载模块|[nN]ot [fF]ound|不存在|未找到|Error|Welcome to nginx!|404|美容|百姓大事件|功能入口'
        self.regex = re.compile(self.errorpage)

    def __load_dir_dict(self):
        self.queue = Queue.Queue()
        ext = self.ext
        target = self.target
        hostuser = target.split('.')
        hostuser = hostuser[len(hostuser)-2]
        #print hostuser
        bak =  ['/'+hostuser+'.rar','/'+hostuser+'.zip','/'+hostuser+hostuser+'.rar','/'+hostuser+'.rar','/'+hostuser+'.tar.gz','/'+hostuser+'.tar','/'+hostuser+'123.zip','/'+hostuser+'123.tar.gz','/'+hostuser+hostuser+'.zip','/'+hostuser+hostuser+'.tar.gz','/'+hostuser+hostuser+'.tar','/'+hostuser+'.bak']
        for j in range(len(bak)):
            BAK = bak[j]
            self.queue.put(BAK)
        with open('mulu.txt') as f:
            for line in f:
                mulu = line.replace('$ext$',ext).strip()
                if mulu:
                    #print mulu
                    self.queue.put(mulu)

    def _scan(self):
        #print "[*]%s Scaning...." % self.target
        try:
            while self.queue.qsize() > 0:
                sub = self.queue.get(timeout=1.0)
        #try:
                #print sub
                domain = self.target + sub
                #print domain
                r = requests.get(domain, headers = header, allow_redirects=False, timeout=5)
                code = r.status_code
                text = r.content
                lens = len(text)
                if code == 200 and not self.regex.findall(text) and lens != 0 :
                 try:
                     title = re.findall(r"<title>(.+?)</title>",text)
                     print "[*] %s =======> 200 (Title:%s)\n" %(domain, title[0]),
                 except Exception,e:
                     print "[*] %s =======> 200\n" %domain,

        except Exception,e:
            pass


    def run(self):
        self.start_time = time.time()
        t_sequ = []
        t_pro = threading.Thread(target=self.progress, name="progress")
        t_pro.setDaemon(True)
        t_pro.start()

        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t.setDaemon(True)
            t.start()
        while self.thread_count > 0:
            time.sleep(0.01)


if __name__ == '__main__':
    #parser = optparse.OptionParser('usage: %prog [options] http://www.c-chicken.cc')
    #parser.add_option('-t', '--threads', dest='threads_num',
     #         default=10, type='int',
     #         help='Number of threads. default = 10')
   # parser.add_option('-e', '--ext', dest='ext', default='php',
      #         type='string', help='You want to Scan WebScript. default is php')
   # parser.add_option('-o', '--output', dest='output', default=None,
   #          type='string', help='Output file name. default is {target}.txt')

   # (options, args) = parser.parse_args()
    #if len(args) < 1:
     #   parser.print_help()
      #  sys.exit(0)
    f = open('target.txt','r')
    hosts = f.read().split()
    for i in range(len(hosts)):
        Dict = 'http://'+hosts[i]
        d = DirScan(target=Dict,threads_num=10,ext='php')
        d.run()
