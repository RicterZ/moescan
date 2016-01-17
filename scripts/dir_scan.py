# coding=utf-8
from lib import exploit
from tools import _tools_DirScan_fast, _tools_DirScan_general


class Exploit(exploit.BaseExploit):
    protocol = 'http'

    def help(self):
        pass

    def exploit(self):
        scan_type = self.extra_arg.get('type')
        scan_ext = self.extra_arg.get('ext')
        scan_threads = self.extra_arg.get('threads')

        if scan_type == 'general':
            # dir_scan_obj = _tools_DirScan_general
            # TODO: general 模式的 DirScan 还有 bug , 在修复之前我是不会用的..qwq
            dir_scan_obj = _tools_DirScan_fast
        else:
            dir_scan_obj = _tools_DirScan_fast

        scan = dir_scan_obj(target=self.target, threads_num=scan_threads, ext=scan_ext)
        scan.run()
