# -*- coding: utf-8 -*-
# @Time    : 18/6/28 下午 9:44
# @Author  : Ji
# @File    : json-dec.py
# @Software: PyCharm

import os
import json


def readFile(filename):
    try:
        with open(filename,'r',encoding='utf8') as file:
            fileRead = file.read()
            file.close()
        return fileRead
    except Exception as e:
        print("Get Path fail，Please Try：",e)

def display(data, parentpath,size=None,formt = 'm'):
    files_size = 0
    folder_size = 0
    exist_large_file = False
    for i in data:
        if isinstance(i,list):
            folder_size += display(i, os.path.join(parentpath, i[0]["name"]),size)
            continue
        if "dsize" in i and size:
            files_size += i['dsize']
            if i["dsize"] > size * 1024 * 1024:
                exist_large_file = True
                if formt == 'k':
                    print(i['dsize']/1024,end='kb： ')
                    print(os.path.join(parentpath,i["name"]))
                if formt == 'm':
                    print(i['dsize'] / (1024*1024), end='Mb： ')
                    print(os.path.join(parentpath, i["name"]))
                if formt == 'g':
                    print(i['dsize'] / (1024*1024*1024), end='Gb： ')
                    print(os.path.join(parentpath, i["name"]))
    if (files_size > size * 1024 * 1024) and not exist_large_file:#没有大文件 但文件总和大于阈值
        print((files_size+folder_size)/(1024*1024),end='mb: ')
        print(parentpath+'********************DIR')
    return files_size+folder_size


if __name__ == '__main__':
    path = '.'
    # os.system("ncdu -x %s -o scanresult"%path)
    data = json.loads(readFile('scanresult'))
    display(data[-1], data[-1][0]["name"], 10,'m')
