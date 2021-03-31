import json
import time
from pathlib import Path
from datetime import datetime

import requests
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from requests.exceptions import Timeout

from settings import ACCESS_KEY_ID, ACCESS_KEY_SECRET, DOMAIN, RECORD_ID, logging, LOGO


class DNS:
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

    def get_dns_list(self):
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DOMAIN)
        response = self.client.do_action_with_exception(request)

        return json.loads(response.decode('utf-8'))

    def update_dns(self, ip_address, prefix):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(RECORD_ID)
        request.set_RR(prefix)
        request.set_Type("A")
        request.set_Value(ip_address)
        response = self.client.do_action_with_exception(request)

        return json.loads(response.decode('utf-8'))


def get_ip_address():
    count = 1
    extract_field = 'query'
    url = 'http://ip-api.com/json/'
    url_1 = 'https://ipapi.co/json'
    try:
        response = requests.get(url, timeout=10)
    except Timeout as e:
        logging.info(e)
        response = requests.get(url_1, timeout=10)
        extract_field = 'ip'
    if count > 3:  # 重试三次断开
        return
    if response.status_code != 200:
        time.sleep(5)
        get_ip_address()
    result_dict = response.json()
    return result_dict.get(extract_field, None)


def match_ip(ip_address):
    "匹配当前ip"
    file_path = Path(__file__).resolve().parent.joinpath('ip.json')
    data = {
        'ip_address': ip_address,
        'create_time': str(datetime.now())
    }
    if not file_path.exists():
        with open(file_path, 'w') as f:
            f.write(json.dumps(data))
        return False

    with open(file_path, 'r') as file:
        temp = json.loads(file.read())
    if temp.get('ip_address') == ip_address:
        return True
    with open(file_path, 'w') as new_f:
        new_f.write(json.dumps(data))
    return False


def run():
    logging.info(LOGO)
    ip_address = get_ip_address()
    # ip是否已存在
    if match_ip(ip_address):
        return
    # 更新dns
    logging.info('==========公网IP已变更==========')
    dns = DNS()
    dns.update_dns(ip_address, prefix='nat')


if __name__ == '__main__':
    run()
