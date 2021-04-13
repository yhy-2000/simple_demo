import csv
import requests
import traceback
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def get_url():
    import pandas as pd
    lines=pd.read_csv("./Validation_GCC-1.1.0-Validation.tsv",delimiter='\t')
    # print(lines)
    li=[]
    name=[]
    for line in lines.iloc:
        name.append(line[0])
        li.append(line[1])
    return name,li


# url,name=get_url()
name,urls = get_url()
proxies = { "http": "http://127.0.0.1:7893", "https": "http://127.0.0.1:7893", }

path='./test/'

queue=list(range(0,len(urls)))

while len(queue)>0:
    for i in range(66,len(urls)):
        url = urls[i]
        descrip = name[i]
        del queue[0]

        try:
            r = requests.request('get', url,proxies=proxies)  # 获取网页

            # time.sleep(100)
            print(r.status_code)

            with open(path + descrip + '.jpg', 'wb') as f:  # 打开写入到path路径里-二进制文件，返回的句柄名为f
                f.write(r.content)  # 往f里写入r对象的二进制文件
            f.close()
        except:
            queue.append(i)

