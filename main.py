# coding=utf-8
from lib.exploit.exploit import run


def main():
    # run('port_scan', '127.0.0.1', '81,2049', arg=''%)
    run('dir_scan', 'http://static.ricter.me/', status_code=(200, 403))

main()
