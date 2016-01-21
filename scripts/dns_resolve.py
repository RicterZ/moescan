# coding=utf-8
import re
import requests
import json
from lib.exploit import BaseExploit
from lib.logger import logger


class Exploit(BaseExploit):
    # TODO: DNS resolve using http://ping.aizhan.com/
    def exploit(self):
        ip = []
        is_cdn = False
        logger.warn('DNS resolve starting of target {}'.format(self.target_netloc))
        match_result = re.compile('flightHandler\((.*?)\)')
        url = 'http://ping.aizhan.com/?r=site/PingResult&callback=flightHandler&type=ping&id={}'
        data = requests.get(url.format(self.target_netloc)).content
        result = match_result.findall(data)
        if not result:
            logger.critical('Failed to get ping result of target {}'.format(self.target_netloc))
            return
        result = json.loads(result[0])
        if 'status' in result and result['status'] == 500:
            logger.critical('Failed to get ping result of target {}'.format(self.target_netloc))
            return

        for i in result:
            logger.info(u'IP address of {} ({}): {}'.format(self.target_netloc, result[i]['monitor_name'],
                                                            result[i]['ip']))
            ip.append(result[i]['ip'])

        if len(set(ip)) > 2:
            logger.warn('It seems target use CDN according to the result'.format(self.target_netloc))
            is_cdn = True

        return {'result': {'is_cdn': is_cdn, 'ip': ip}, 'status': True}
