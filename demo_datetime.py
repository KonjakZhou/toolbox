# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Fri 15 July 2022 14:51:30 CST
# MagIc C0de: c1ff2caa3215

from datetime import datetime

def unix_to_format(timestamp):
    if isinstance(timestamp, float) or isinstance(timestamp, int):
        ans = datetime.fromtimestamp(timestamp)
    return ans 

if __name__ == '__main__':
    timestr = unix_to_format(1657761063)
    print(timestr)
    print(datetime.timestamp(datetime.now()))
    
    pass