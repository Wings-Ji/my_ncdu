# -*- coding: utf-8 -*-
# @Time    : 18/6/28 下午 9:44
# @Author  : Ji
# @File    : json-dec.py
# @Software: PyCharm

import os
import sys
import json
import getopt

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

def main(argv):
    help = '''python3 my_ncdu.py  <-d>  <directory>  <options>  <value>
    eg. python3 my_ncdu -d /opt/ -m 3

 -h         Help message
 -d         The directory(if is null,scan current directory)
 -m         Print input > MB
 -g         Prin input >GB
'''
    path = "."
    msize = ""
    gsize = ""
    if len(argv)  == 0:
        print(help)
    try:
        opts, args = getopt.getopt(argv, "hd:m:g:")
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ("-d", "--d"):
            path = arg
        elif opt in ("-m", "--m"):
            msize = arg
        elif opt in ("-g", "--g"):
            gsize = arg
        else:
            print(help)
            sys.exit()

    if msize:
        os.system("ncdu -x %s -o scanresult"%path)
        data = json.loads(readFile('scanresult'))
        print("File > %s MB belows："%msize)
        display(data[-1], data[-1][0]["name"], int(msize), 'm')
    elif gsize:
        os.system("ncdu -x %s -o scanresult"%path)
        data = json.loads(readFile('scanresult'))
        print("File > %s GB belows：" % gsize)
        gs = int(gsize)*1024
        display(data[-1], data[-1][0]["name"], gs,'g')


if __name__ == '__main__':
    main(sys.argv[1:])