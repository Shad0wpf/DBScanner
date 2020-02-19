# DBScanner（未授权访问漏洞批量检测）


## DBScanner简介

Github：[https://github.com/Shad0wpf/DBScanner](https://github.com/Shad0wpf/DBScanner)

在se55i0n的[DBScanner](https://github.com/se55i0n/DBScanner)脚本上做了部分修改，增加部分漏洞检测的准确性和检测方法。

自动扫描内网常见sql、no-sql数据库未授权访问漏洞及常规弱口令检测

- mysql（扫描root账号弱口令）
- mssql（扫描sa账号弱口令）
- oracle（扫描system/sys/scott等账号弱口令）
- postgresql（扫描postgres账号弱口令）
- redis（扫描弱口令及未授权访问）
- mongodb（扫描未授权访问）
- memcached（扫描未授权访问）
- elasticsearch（扫描未授权访问）
- hadoop（扫描未授权访问）
- zookeeper（扫描未授权访问）
- rsync（扫描未授权访问）


## 安装

该脚本使用Python2运行


### 安装Python库**
```
pip install -r requirements.txt
```


### 安装Oracle客户端支持
a. 安装cx_Oracle库
```shell
python -m pip install cx_Oracle --upgrade
```

b. 安装Oracle Instant Client<br />i. Kali下使用apt安装
```shell
apt install oracle-instantclient-basic
```

ii. 手动安装<br />下载Oracle Instant Client，解压后将Oracle Instant Client目录加入环境变量。
```shell
mkdir -p /opt/oracle
cd /opt/oracle
unzip instantclient-basic-linux.x64-19.3.0.0.0dbru.zip

sudo sh -c "echo /opt/oracle/instantclient_19_3 > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig
```

Seafile：[https://183.221.111.23:9001/d/1a912274e1974e978d41/](https://183.221.111.23:9001/d/1a912274e1974e978d41/)<br />官网下载地址：[https://www.oracle.com/database/technologies/instant-client/downloads.html](https://www.oracle.com/database/technologies/instant-client/downloads.html)
> 参考：[https://oracle.github.io/odpi/doc/installation.html#macos](https://oracle.github.io/odpi/doc/installation.html#macos)<br />[https://www.zhihu.com/question/19629769/answer/123755085](https://www.zhihu.com/question/19629769/answer/123755085)


### 安装ZooKeeper客户端
检测Zookeeper未授权访问，需安装Zookeeper客户端。<br />Ubuntu or Kali
```
sudo apt install zookeeper
```

或下载官方发布的压缩包文件，解压后使用，根据实际情况修改lib/exploit.py代码中客户端路径

> 压缩包文件同时提供对Linux和Windows的支持，Linux客户端文件zkCli.sh，Windows客户端文件zkCli.cmd
> 建议先测试zkCli是否能正常使用，否则引起漏报。
> [https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/current/](https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/current/)


> zookeeper客户端Java报错处理
> [https://www.jianshu.com/p/9529249a26e7](https://www.jianshu.com/p/9529249a26e7)


### 
### psycopg2安装报错处理
需先安装postgresql-server-dev-x.x
```shell
sudo apt install postgresql-server-dev-9.5
```

## 

## 使用
```
python dbscan.py -f iplist.txt
or
python dbscan.py -i 192.168.1.0/24
```

### 参数

```
  -h, --help  显示帮助文件
  -i IP       扫描IP或IP段
  -f FILE     IP清单文件
  -t THREAD   线程数(默认50)
```

![](https://cdn.nlark.com/yuque/0/2020/png/259770/1582030455047-0305f4d3-8275-4265-9596-5f470bab25e0.png#align=left&display=inline&height=425&originHeight=425&originWidth=759&size=0&status=done&style=none&width=759)
