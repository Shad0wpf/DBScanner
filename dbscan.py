#!/usr/bin/env python
#coding:utf-8
#Author:se55i0n
#针对常见sql、No-sql数据库进行安全检查
#增加从文件读取IP或命令行读取IP的参数    2018.06.05 By:Shad0wpf
#IP解析模块替换为ipaddr（子网网络地址错误时ipaddr仍可解析，IPy会报错）    2018.06.06 By:Shad0wpf
#增加MySQL连接超时时间为10s      2018.06.07 By:Shad0wpf
#增加Socket连接超时时间为10s      2018.06.15 By:Shad0wpf
#增加Hadoop和ZooKeeper未授权访问检测      2018.06.15 By:Shad0wpf
#修改Zookeeper未授权访问检测方式，"echo envi"方式检测存在误报，修改为调用系统命令执行zkCli.sh获取结果（需在Linux系统下使用）    2018.9.18 By:Shad0wpf
#修复一个屏幕打印乱码问题     2018.3.29  By:Shad0wpf
#修改MongoDB未授权访问检测方式，Pymongo库不支持2.6之前版本Mongodb，存在漏报    2019.04.17  By:Shad0wpf
#增加Rsync未授权访问检测  2020.02.19  By:Shad0wpf


import sys
import ipaddr
import time
import socket
import gevent
import argparse
from gevent import monkey
from multiprocessing.dummy import Pool as ThreadPool
from lib.config import *
from lib.exploit import *

monkey.patch_all()

class DBScanner(object):
    def __init__(self, ips, thread):
        self.thread = int(thread)
        self.ips    = ips
        self.ports  = []
        self.time   = time.time()
        self.get_port()
        self.check = check()
    

    def get_port(self):
        self.ports = list(p for p in service.itervalues())


    def scan(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            if s.connect_ex((ip, port)) == 0:
                self.handle(ip, port)
        except Exception as e:
            pass
        finally:
            s.close()


    def handle(self, ip, port):
        for v,k in service.iteritems():
            if k == str(port):
                if v == 'mysql':
                    self.check.mysql(ip)
                elif v == 'mssql':
                    self.check.mssql(ip)
                elif v == 'oracle':
                    self.check.oracle(ip)
                elif v == 'postgresql':
                    self.check.postgresql(ip)
                elif v == 'redis':
                    self.check.redis(ip)
                elif v == 'mongodb':
                    self.check.mongodb(ip)
                elif v == 'memcached':
                    self.check.memcached(ip)
                elif v == 'elasticsearch':
                    self.check.elasticsearch(ip)
                elif v == 'hadoop_namenode':
                    self.check.hadoop_namenode(ip)
                elif v == 'hadoop_resourcemanager':
                    self.check.hadoop_resourcemanager(ip)
                elif v == 'zookeeper':
                    self.check.zookeeper(ip)
                elif v== 'rsync':
                    self.check.rsync(ip)

    def start(self, ip):
        try:
            gevents = []
            for port in self.ports:
                gevents.append(gevent.spawn(self.scan, ip, int(port)))
            gevent.joinall(gevents)
        except Exception as e:
            pass
        print(u"IP:{}\t\t完成扫描".format(ip))


    def run(self):
        try:
            pool = ThreadPool(processes=self.thread)
            pool.map_async(self.start, self.ips).get(0xffff)
            pool.close()
            pool.join()
        except Exception as e:
            pass
        except KeyboardInterrupt:
            print(u'\n{}[-] 用户终止扫描...{}'.format(R, W))
            sys.exit(1)
        finally:
            print('-' * 55)
            print(u'{}[+] stop at {},扫描耗时 {} 秒.{}'.format(O, time.asctime(), time.time()-self.time, W))
            with open('weakpass.txt', 'a+') as f:
            	f.write("-" * 70 + "\n")
            	f.write('[+] stop at {},扫描耗时 {} 秒.\r\n\r\n'.format(time.asctime(), time.time()-self.time))


def banner():
    banner = '''
    ____  ____ _____
   / __ \/ __ ) ___/_________ _____  ____  ___  _____
  / / / / __  \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / /_/ / /_/ /__/ / /__/ /_/ / / / / / / /  __/ /
/_____/_____/____/\___/\__,_/_/ /_/_/ /_/\___/_/
    '''
    print(B + banner + W)
    print('-'*55)


def main():
    banner()
    parser = argparse.ArgumentParser(description='Example: python {0} -i 192.168.1.0/24 \n\r or python {0} -f iplist.txt -t 30'.format(sys.argv[0]))
    parser.add_argument('-i', type=str, default='', dest='ip', help=u'扫描IP或IP段')
    parser.add_argument('-f', type=str, default='', dest='file', help=u'IP清单文件')
    parser.add_argument('-t', type=int, default=50, dest='thread', help=u'线程数(默认50)')
    args   = parser.parse_args()
    if args.ip:
        ips = []
        try:
            ipxx = ipaddr.IPNetwork(args.ip)
            for ip in ipxx:
                ips.append(str(ip))
        except Exception as e:
            print(e)
            pass

        with open('weakpass.txt', 'a+') as f:
            f.write("+" * 70 + "\r\n")
            f.write('[+] start at {},共扫描{}个IP.\r\n\r\n'.format(time.asctime(), len(ips)))
        print(u'start at {},共扫描{}个IP.\r\n'.format(time.asctime(), len(ips)))
        myscan = DBScanner(ips, args.thread)
        myscan.run()

    if args.file:
        ips = []
        with open(args.file, 'r') as fl:
            for line in fl.readlines():
                ipx = line.rstrip("\n\r")
                try:
                    ipxx = ipaddr.IPNetwork(ipx)
                    for ip in ipxx:
                        ips.append(str(ip))
                except Exception as e:
                    print(e)
                    pass

        with open('weakpass.txt', 'a+') as f:
            f.write("+" * 70 + "\r\n")
            f.write('[+] start at {},共扫描{}个IP.\r\n\r\n'.format(time.asctime(), len(ips)))
        print(u'start at {},共扫描{}个IP.\r\n'.format(time.asctime(), len(ips)))
        myscan = DBScanner(ips, args.thread)
        myscan.run()


if __name__ == '__main__':
    main()
