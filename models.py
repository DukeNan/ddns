# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, MetaData, Table, text
from sqlalchemy.dialects.mysql import INTEGER

metadata = MetaData()

t_nat_log = Table(
    'nat_log', metadata,
    Column('id', INTEGER(11), primary_key=True, comment='主键ID'),
    Column('create_time', TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间'),
    Column('ip_addr', String(20, 'utf8mb4_bin'), nullable=False, comment='外网ip'),
    Column('ip_hash', String(40, 'utf8mb4_bin'), nullable=False, unique=True,
           comment='日期和ip的hash值MD5(2020-12-12@60.249.20.249  md5值)'),
    Column('ssh_cmd', String(100, 'utf8mb4_bin'), nullable=False, comment='ssh远程登录（ssh -p 6622 ubuntu@120.80.20.107）')
)
