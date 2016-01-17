#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import optparse
import sys
import threading
import time
import Queue
import re
import urlparse
from lib.logger import logger

__author__ = 'croxy'

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate, compress',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
}


class DirScan(object):
    def __init__(self, target, threads_num, ext, status_code=None):
        self.target = target.strip()
        self.threads_num = threads_num
        self.ext = ext
        self.lock = threading.Lock()
        self.thread_count = self.threads_num = threads_num
        self.__load_dir_dict()
        self.errorpage = (r'防火墙|出错啦|信息提示|参数错误|no exists|User home page for|可疑输入拦截|D盾|安全狗|无法加载模块|'
                          r'[nN]ot\s[fF]ound|不存在|未找到|Error|Welcome to nginx!|404|')
        self.regex = re.compile(self.errorpage)

        if isinstance(status_code, (list, tuple, set)) or status_code is None:
            self.status_code = status_code if status_code else [200, 301, 302, 403, 500]
        else:
            raise TypeError('status_code')

    def __load_dir_dict(self):
        self.queue = Queue.Queue()
        ext = self.ext
        target = self.target
        hostuser = target.split('.')
        hostuser = hostuser[len(hostuser) - 2]
        bak = ['/' + hostuser + '.rar', '/' + hostuser + '.zip', '/' + hostuser + hostuser + '.rar',
               '/' + hostuser + '.rar',
               '/' + hostuser + '.tar.gz', '/' + hostuser + '.tar', '/' + hostuser + '123.zip',
               '/' + hostuser + '123.tar.gz',
               '/' + hostuser + hostuser + '.zip', '/' + hostuser + hostuser + '.tar.gz',
               '/' + hostuser + hostuser + '.tar', '/' + hostuser + '.bak']

        for i in bak:
            self.queue.put(i)

        with open('{}/dir.txt'.format(os.path.dirname(__file__))) as f:
            for line in f:
                mulu = line.replace('$ext$', ext).strip()
                if mulu:
                    self.queue.put(mulu)

    def _scan(self):
        while True:
            if self.queue.empty():
                break
            try:
                sub = self.queue.get_nowait()
                self.queue.task_done()
                domain = self.target + sub
                r = requests.head(domain, headers=header, timeout=5, stream=True)
                code = r.status_code
                if code in self.status_code:
                    logger.info('status code {} -> {}'.format(code, domain))

            except Exception, e:
                pass

        self.thread_count -= 1

    def run(self):
        self.start_time = time.time()
        t_sequ = []

        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t.setDaemon(True)
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


def parse_args():
    parser = optparse.OptionParser('usage: %prog [options] http://www.c-chicken.cc')
    parser.add_option('-t', '--threads', dest='threads_num',
                      default=10, type='int',
                      help='Number of threads. default = 10')
    parser.add_option('-e', '--ext', dest='ext', default='php',
                      type='string', help='You want to Scan WebScript. default is php')

    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()

if __name__ == '__main__':
    (options, args) = parse_args()
    url = patch_url(args[0])
    d = DirScan(target=url, threads_num=options.threads_num, ext=options.ext)
    d.run()
