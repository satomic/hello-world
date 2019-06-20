# coding=utf-8

import datetime


def current_time(fmt='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.datetime.now().strftime(fmt)[:-3]


def print_base(base_info, type):
    print("%s [%s] %s" % (current_time(), type, base_info))


def print_err(err, type="ERRO"):
    print_base(err, type)


def print_info(info, type="INFO"):
    print_base(info, type)


def print_warn(warn, type="WARN"):
    print_base(warn, type)


if __name__ == "__main__":
    print(current_time())
    print_info("这是一条信息")
    print_warn("这是一条告警")
    print_err("这是一条错误")