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
    for i in data:
        if isinstance(i,list):
            display(i, os.path.join(parentpath, i[0]["name"]),size)
            continue
        if "dsize" in i and size:
            if i["dsize"] > size * 1024 * 1024:
                if formt == 'k':
                    print(i['dsize']/1024,end='kb： ')
                    print(os.path.join(parentpath,i["name"]))
                if formt == 'm':
                    print(i['dsize'] / (1024*1024), end='Mb： ')
                    print(os.path.join(parentpath, i["name"]))
                if formt == 'g':
                    print(i['dsize'] / (1024*1024*1024), end='Gb： ')
                    print(os.path.join(parentpath, i["name"]))

if __name__ == '__main__':
    path = '.'
    os.system("ncdu -x %s -o scanresult"%path)
    data = json.loads(readFile('scanresult'))
    display(data[-1], data[-1][0]["name"], 1024,'g')
