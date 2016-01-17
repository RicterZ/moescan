# coding=utf-8
from lib import exploit
from lib.logger import logger
from tools import _tools_DirScan_fast, _tools_DirScan_general


class Exploit(exploit.BaseExploit):
    protocol = 'http'

    def help(self):
        pass

    def exploit(self):
        scan_type = self.extra_arg.get('type')
        scan_ext = self.extra_arg.get('ext')
        scan_threads = self.extra_arg.get('threads')
        scan_status_code = self.extra_arg.get('status_code')

        if scan_type == 'general':
            # dir_scan_obj = _tools_DirScan_general
            # TODO: general 模式的 DirScan 还有 bug , 在修复之前我是不会用的..qwq
            dir_scan_obj = _tools_DirScan_fast
        else:
            dir_scan_obj = _tools_DirScan_fast
        scan_threads = scan_threads if scan_threads else 10
        logger.warn('DirScan start with {} thread(s) of target {}'.format(scan_threads, self.target))
        scan = dir_scan_obj(target=self.target,
                            threads_num=scan_threads,
                            ext=scan_ext if scan_ext else 'php',
                            status_code=scan_status_code)
        scan.run()
