## DDNS

### 说明

> 通过定时更新域名解析来实现ddns功能。如果路由器支持ddns更好，不过我的路由器不支持，所有开发脚本动态更新域名解析来时间ddns功能。

### 准备

* 宽带拨号具有公网ip
* 局域网长时间运行主机一台
* 阿里云已备案域名一个
* 数据库（可有可无）

### 流程



![ddns流程图](http://image.dukenan.top/blog/未命名文件.jpg)

### 运行

进入项目目录，创建虚拟环境

```bash
python3 -m venv .env
```

安装依赖

```bash
source .nat/bin/activate

pip install -r requirements.txt

deactivate
```

每分钟运行一次脚本

```bash
*/1 * * * * /home/root/ddns/.env/bin/python3 /home/root/ddns/update_dns.py
```

