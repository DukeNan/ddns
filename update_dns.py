import datetime
import hashlib
import json
import time

import requests
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from sqlalchemy import create_engine, text

from settings import DB_URL, ACCESS_KEY_ID, ACCESS_KEY_SECRET, DOMAIN, RECORD_ID, logging, LOGO


class DNS:
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

    def get_dns_list(self):
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DOMAIN)
        response = self.client.do_action_with_exception(request)

        return json.loads(response.decode('utf-8'))

    def update_dns(self, ip_address):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(RECORD_ID)
        request.set_RR("nat")
        request.set_Type("A")
        request.set_Value(ip_address)
        response = self.client.do_action_with_exception(request)

        return json.loads(response.decode('utf-8'))


def update_dns():
    pass


def get_ip_address():
    count = 1
    url = 'http://ip-api.com/json/'
    response = requests.get(url)
    if count > 3:  # 重试三次断开
        return
    if response.status_code != 200:
        time.sleep(5)
        get_ip_address()
    result_dict = response.json()
    return result_dict.get('query', None)


def update_db(data: dict):
    engine = create_engine(DB_URL)
    sql = text(
        'insert into nat_log(ip_addr, ip_hash, ssh_cmd) select :ip_addr, :ip_hash, :ssh_cmd from dual where not exists(select id from nat_log where ip_hash=:ip_hash or (ip_addr=:ip_addr and create_time > date_add(now(), interval -2 day)))')
    with engine.connect() as conn:
        result = conn.execute(sql, **data)
    return result.lastrowid


def get_md5(string: str):
    """
    获取MD5加密字符串
    """
    md5 = hashlib.md5()
    md5.update(string.encode(encoding='utf-8'))
    return md5.hexdigest()


def run():
    logging.info(LOGO)
    ip_address = get_ip_address()
    now = str(datetime.datetime.now().date())
    ip_hash = get_md5(f'{now}@{ip_address}')
    data = {
        'ip_addr': ip_address,
        'ip_hash': ip_hash,
        'ssh_cmd': f'ssh -p 8822 ubuntu@{ip_address}',
    }
    insert_result = update_db(data)
    # ip是否更新
    if not insert_result:
        return
    # 更新dns
    logging.info('==========公网IP已变更==========')
    dns = DNS()
    dns.update_dns(ip_address)


if __name__ == '__main__':
    run()
