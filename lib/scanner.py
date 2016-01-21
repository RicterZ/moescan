# coding=utf-8
from lib.logger import logger
from lib.exploit import exploit


class Scanner(object):
    def __init__(self, target=None, mode='single'):
        self.target = target
        self.mode = mode

    def single_mode(self):
        # TODO: 多线程什么鬼的..要改要改
        result = exploit.run('dns_resolve', target=self.target)
        if not result.get('status'):
            logger.error('Something wrong, do you want to continue?[y/N]:')
            if not raw_input().lower() == 'y':
                logger.critical('User abort, quit.')
                return

        if result.get('result').get('is_cdn'):
            logger.warn('Target is using CDN, port scan skipped.')

    def moe_mode(self):
        pass

    def ep_mode(self):
        pass

    def run(self):
        runner = self.__class__.__dict__.get('{}_mode'.format(self.mode))
        if not runner:
            logger.critical('Mode {} not exist, quit.'.format(self.mode))
            return
        runner(self)
