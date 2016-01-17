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
import difflib
import random
import string
import urlparse
from progressbar import ProgressBar

header = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
'Accept-Encoding': 'gzip, deflate, compress',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
}

Banner = r'''

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
'''


class DirScan:
    def __init__(self, target, threads_num, ext):
        global errtext
        self.target = target.strip()
        self.threads_num = threads_num
        self.ext = ext
        self.lock = threading.Lock()
        self.thread_count = self.threads_num = threads_num
        self.__load_dir_dict()
        errtext = self.build_not_found_template(self.target)
        self.errorpage = r'信息提示|参数错误|no exists|User home page for|可疑输入拦截|D盾|安全狗|无法加载模块|[nN]ot [fF]ound|不存在|未找到|Error|Welcome to nginx!|404|'
        self.regex = re.compile(self.errorpage)

    # def errtext(self):
    #     target = self.target
    #     choices = string.letters + string.digits
    #     path = ''.join([random.choice(choices) for _ in range(int(16))])
    #     url = target + '/' + path
    #     print url
    #     try:
    #         r =requests.get(url, headers=header, timeout=5)
    #         errtext = r.text
    #     except Exception,e:
    #         print e
    #     return errtext
    #
    #

    def __load_dir_dict(self):
        self.queue = Queue.Queue()
        ext = self.ext
        target = self.target
        hostuser = target.split('.')
        hostuser = hostuser[len(hostuser)-2]
        bak =  ['/'+hostuser+'.rar','/'+hostuser+'.zip','/'+hostuser+hostuser+'.rar','/'+hostuser+'.rar','/'+hostuser+'.tar.gz','/'+hostuser+'.tar','/'+hostuser+'123.zip','/'+hostuser+'123.tar.gz','/'+hostuser+hostuser+'.zip','/'+hostuser+hostuser+'.tar.gz','/'+hostuser+hostuser+'.tar','/'+hostuser+'.bak']
        with open('dir.txt') as f:
            for line in f:
                mulu = line.replace('$ext$',ext).strip()
                if mulu:
                    self.queue.put(mulu)

    def get_random_string(self,length=16):
        """ 随机生成指定长度由大小写字母和数字构成的字符串 """
        choices = string.letters + string.digits
        return ''.join([random.choice(choices) for _ in range(int(length))])

    def build_random_path(self):
        """ 随机生成由大小写字母和数字构成的路径 """
        random_string = self.get_random_string(random.randint(5, 10))
        ext_choices = ['.html', '.php', '.asp', '.htm', '.jpeg', '.png', '.zip']
        random_path = random_string
        while True:
            # 随机构建子路径，当 random.choice([True, False]) 为 False 时退出循环
            if not random.choice([True, False]):
                random_path += random.choice(ext_choices)
                break
            else:
                random_string = self.get_random_string(random.randint(5, 10))
                random_path += '/' + random_string

        return random_path

    def build_not_found_template(self,url):
        """ 获取扫描URL基本路径，构建基于当前目录的404页面模板 """
        base_url = urlparse.urljoin(url, './')

        pre_responses = []
        for _ in range(6):
            # 随机生成路径，相继访问得到页面内容，对成功返回的结果进行比较得到404页面模板
            random_path = self.build_random_path()
            random_url = urlparse.urljoin(base_url, random_path)
            try:
                response = requests.get(random_url)
            except requests.exceptions.RequestException, ex:
                err = 'failed to access %s, ' % random_url
                err += str(ex)
                print err
                continue
            pre_responses.append(response)

        if len(pre_responses) < 2:
            # 由于随机获取到的页面内容数量太少不能进行 404页面模板 提取操作
            return None

        ratios = []
        pre_content = pre_responses[0].content
        for response in pre_responses[1:]:
            cur_content = response.content
            ratio = difflib.SequenceMatcher(None, pre_content, cur_content).quick_ratio()
            ratios.append(ratio)
            pre_content = cur_content

        average = float(sum(ratios)) / len(ratios)
        if average > 0.9:
            #print 'succeed to build %s 404 page template' % url

            return random.choice(pre_responses).content
        else:
            return None

    def _scan(self):
        #print errtext
        while True:
            if self.queue.empty():
                break
            try:
                sub = self.queue.get_nowait()
        #try:
                #print sub
                domain = self.target + sub
                #print domain
                self.lock.acquire()
                r = requests.get(domain, headers = header, timeout=5, stream=True)
                code = r.status_code
                if ('gz' or 'zip' or 'rar' or 'tar' or '7z' or 'bz2') in domain and code == 200:
                    print "[*] %s =======> 200\n" %domain,
                text = r.text
                #print errtext
                ratios = dict((_, difflib.SequenceMatcher(None, text, errtext).quick_ratio()) for _ in (True, False))
                is404 = all(ratios.values()) and ratios[True] > 0.9
                #print is404
                #print code
                if code == 200 and not self.regex.findall(text) and not is404:
                    try:
                        title = re.findall(r"<title>(.+?)</title>",text)
                        print "[*] %s =======> 200 (Title:%s)\n" %(domain, title[0]),
                    except Exception,e:
                        print "[*] %s =======> 200\n" %domain,
                self.lock.release()
            except Exception,e:
                print e

    def progress(self):
        """show progress"""
        dirCount = self.queue.unfinished_tasks
        bar = ProgressBar().start()
        while self.queue.qsize()!=0:
            bar.update(int(((dirCount-self.queue.qsize())/float(dirCount))*100))
            time.sleep(1)
        bar.finish()
        exit()

    def run(self):
        self.start_time = time.time()
        t_sequ = []
        t_pro = threading.Thread(target=self.progress, name="progress")
        t_pro.setDaemon(True)
        t_pro.start()

        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t_sequ.append(t)
            t.start()
        while self.thread_count > 0:
            time.sleep(0.01)

        for t in t_sequ:
            t.join()

        print "finished"

def patch_url(url):
    """ 修复不标准URL """
    res = urlparse.urlparse(url)
    if not res.scheme:
        url = 'http://' + url

    return url

if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [options] http://www.c-chicken.cc')
    parser.add_option('-t', '--threads', dest='threads_num',
              default=10, type='int',
              help='Number of threads. default = 5')
    parser.add_option('-e', '--ext', dest='ext', default='php',
               type='string', help='You want to Scan WebScript. default is php')
   # parser.add_option('-o', '--output', dest='output', default=None,
   #          type='string', help='Output file name. default is {target}.txt')

    (options, args) = parser.parse_args()
    if len(args) < 1:
        print Banner
        parser.print_help()
        sys.exit(0)
    url = patch_url(args[0])
    d = DirScan(target=url,threads_num=options.threads_num,ext=options.ext)
    d.run()
