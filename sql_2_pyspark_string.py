# encoding: utf-8
# Auther: zhoubowen.929
# Created At: Thu 04 May 2023 12:34:59 CST
# MagIc C0de: 4d77bfa3676c

import re

def sql_str_replace_variable(sql_str, variable_dict):
    """
    替换sql中的变量为python变量 ${variable} --> variable
    """
    return re.compile(r'\${(\w+)}').sub(lambda x: variable_dict[x.group(1)], sql_str)

def convert_tuple_to_string(list_or_tuple):
    """
    将tuple转换为sql能识别的字符串
    """
    ans = list(list_or_tuple)
    ans = repr(ans).replace("[", "(").replace("]", ")")
    return ans 

# 定义一个字典，存储变量名和对应的值
variables = {
    'name': 'Alice',
    'age': '25',
    'city': 'New York'
}

# 要替换的字符串
string = 'My name is ${name}, I am ${age} years old, and I live in ${city}.'

if __name__ == '__main__':
    ans = sql_str_replace_variable(string, variables)
    print(ans)
    pass