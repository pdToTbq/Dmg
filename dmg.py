#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 时间: 2022/1/19 下午2:21
# 名称: 东风摇百草
# 文件: dmg.py
import argparse
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}

def cmd():
    """
    终端接口

    Returns:
    """
    args = argparse.ArgumentParser(description='Personal Information', epilog="东风夜放花千树。更吹落、星如雨")
    args.add_argument("file1", type=str, help="要查询的域名文件")
    args.add_argument("file2", type=str, help="保存的结果，文件存在会清空")
    return args.parse_args()


def read_file(file):
    """
    读取文件内容

    Args:
        file:

    Returns:

    """
    with open(file, 'r') as f:
        return [line.strip() for line in f]


def write_file(domains,file2):
    """
    存活数据写入文件

    Args:
        domain:

    Returns:

    """
    with open(file2, 'w') as f:
        for domain in domains:
            f.writelines("%s\n" % domain)


def check_alive(domain):
    """
    检测域名是否存活

    Returns: 存活返回True,不存货返回False

    """
    if ":" not in domain:
        domain = "http://%s" % domain
    try:
        print(domain)
        reponse = requests.get(domain, headers=headers, timeout=10)
        if reponse.status_code in [200, 301, 302, 404, 403, 500]:
            return domain
        return False
    except:
        return False


def run():
    arge = cmd()
    with ThreadPoolExecutor(max_workers=100) as t:
        domains = read_file(arge.file1)
        alive = []
        obj_list = []
        for domain in domains:
            obj = t.submit(check_alive, domain)
            obj_list.append(obj)

        for result in as_completed(obj_list):
            if result.result():
                alive.append(result.result())

        write_file(alive,arge.file2)

    print("---------------完成----------------------------")


if __name__ == '__main__':
    run()
