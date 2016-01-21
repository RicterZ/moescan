# coding=utf-8
from lib.exploit.exploit import run
from lib.scanner import Scanner


def main():
    target = 'www.ricter.me'
    mode = 'single'
    # moe, ep(enterprise), single

    # moe mode:
    # sooooooooooooooooo sloooooooooooow
    # sub-domains brute, ports(1-65535) scan, dir scan, C class IP scan (including previous scans)

    # ep mode:
    # sub-domains brute, ports(21, 22, 53, 80, 81, 82, 88, 873, 2049, 3389, 5900, 8080, 8081, 8888, 7001, 9200
    # ) scan, dir scan, C class IP scan(including ports scan)

    # single mode
    # ports scan (1-65535), dir scan

    # run('port_scan', '127.0.0.1', '81,2049', arg=''%)
    # run('dir_scan', 'http://static.ricter.me/', status_code=(200, 403))
    # run('dns_resolve', 'http://static.ricter.me')
    s = Scanner(target=target, mode=mode)
    s.run()

main()
