# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Fri 02 June 2023 17:52:56 CST
# MagIc C0de: d7ea6b5e7bfc

import os

import logging
LOG_FORMAT = '%(asctime)s - %(levelname)s : %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def get_file_names_from_bash(input_str):
    ans_str = input_str.split()[-1]
    return ans_str

# 获取ls结果
def hdfs_ls(input_dir):
    logging.info("hdfs_ls input_dir: {}".format(input_dir))
    cmd_result = os.popen("hdfs dfs -ls {}".format(input_dir))
    cmd_result_list = cmd_result.readlines()
    result_list = list(map(get_file_names_from_bash, cmd_result_list[1:]))
    logging.info("hdfs_ls done...")
    return result_list

# 判断是否是一个file
def hdfs_is_file(input_dir):
    logging.info("hdfs_is_file input_dir: {}".format(input_dir))
    cmd_result = os.system("hdfs dfs -test -f {}".format(input_dir))
    if cmd_result == 0:
        return True
    return False

# 判断是否是一个目录
def hdfs_is_directory(input_dir):
    logging.info("hdfs_is_directory input_dir: {}".format(input_dir))
    cmd_result = os.system("hdfs dfs -test -d {}".format(input_dir))
    if cmd_result == 0:
        return True
    return False

if __name__ == '__main__':
    pass