# coding=utf-8
from lib import exploit


class Exploit(exploit.BaseExploit):
    protocol = 'http'

    def exploit(self):
        print(self.target)
