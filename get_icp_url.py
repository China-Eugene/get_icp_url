#_*_ coding:utf-8 _*-
# Python 3.x
#Author: Eugene
#Domain ICP Search From Chinaz

import re
import sys
import requests

url = sys.argv[1]
session = requests.Session()
logo = '''
  _____ _____ _____     _____                     _     
 |_   _/ ____|  __ \   / ____|                   | |    
   | || |    | |__) | | (___   ___  __ _ _ __ ___| |__  
   | || |    |  ___/   \___ \ / _ \/ _` | '__/ __| '_ \ 
  _| || |____| |       ____) |  __/ (_| | | | (__| | | |
 |_____\_____|_|      |_____/ \___|\__,_|_|  \___|_| |_|
 
Wait...                                                                                                              
'''


# 通过Host查询到网站的备案公司名字
def host():
    paramsPost = {"type": "host", "s": url}
    headers = {"Origin": "http://icp.chinaz.com",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
               "Referer": "http://icp.chinaz.com/"+url, "Connection": "close",
               "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
               "Content-Type": "application/x-www-form-urlencoded"}
    cookies = {"CNZZDATA5082706": "cnzz_eid%3D119233034-1584423448-%26ntime%3D1584423448",
               "CNZZDATA433095": "cnzz_eid%3D373306718-1584423784-%26ntime%3D1584423784",
               "UM_distinctid": "170e724541edb1-080b9b37f4371c-5701732-144000-170e724542047f",
               "qHistory": "aHR0cDovL2ljcC5jaGluYXouY29tLyvnvZHnq5nlpIfmoYg="}

    try:
        respone_seo = session.post("http://icp.chinaz.com/{}".format(url), data=paramsPost, headers=headers, cookies=cookies, verify=False)
    except:
        print("检查一下网站能否访问或者系统代理")

    #正则匹配请求拿到备案主办单位名称
    seo_text = respone_seo.text
    name_r = re.compile(r'<li class="bg-gray clearfix"><span>主办单位名称</span><p>(.*?)<a class=')
    name = name_r.findall(seo_text)
    if len(name) == 0:
        print('无法查询到数据,可能网站被屏蔽')
    else:
        return name[0]

def icp():
    #把SEO函数中的备案公司名丢入ICP备案公司反查
    name = host()
    #默认
    paramsPost = {"s":name,"type":"com"}
    cookies = {"CNZZDATA5082706":"cnzz_eid%3D1962878551-1583683775-http%253A%252F%252Fseo.chinaz.com%252F%26ntime%3D1583683775","UM_distinctid":"170bafcceee316-07a88add20f6f7-5701732-144000-170bafcceef593","qHistory":"aHR0cDovL2ljcC5jaGluYXouY29tLyvnvZHnq5nlpIfmoYh8aHR0cDovL3Nlby5jaGluYXouY29tX1NFT+e7vOWQiOafpeivog=="}
    headers = {"Origin":"http://icp.chinaz.com","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36","Referer":"http://icp.chinaz.com/%E6%B1%89%E5%BA%AD%E6%98%9F%E7%A9%BA%EF%BC%88%E4%B8%8A%E6%B5%B7%EF%BC%89%E9%85%92%E5%BA%97%E7%AE%A1%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8","Connection":"close","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","Content-Type":"application/x-www-form-urlencoded"}

    try:
        icp = session.post("http://icp.chinaz.com/{}".format(name), data=paramsPost, headers=headers, cookies=cookies, timeout=5, verify=False)
    except:
        print("检查一下网站能否访问或者系统代理")

    #第一次正则查询，拿到部分代码
    icp_text =icp.text
    code_r = re.compile(r"<td class='tc'>(.*?)</td>")
    code_end = code_r.findall(icp_text)
    with open(url+'.txt', "a") as f:
        #域̶名̶正̶则̶，̶拿̶出̶最̶后̶域̶名̶,这个匹配搞死我了，才发现range才是真爱
        for i in range(0, len(code_end), 6):
            end = code_end[i]
            print(end)
            f.write(str(end)+'\n')
        print('\n域名已保存到根目录的'+url+'.txt文件')

if __name__ == '__main__':
    print(logo)
    icp()
