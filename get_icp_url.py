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


def seo():
    #通过SEO查询到网站的备案公司名字
    try:
        respone_seo = session.get("http://seo.chinaz.com/{}".format(url), timeout=5)
    except:
        print("检查一下网站能否访问或者系统代理")

    #正则匹配请求拿到网站备案公司
    seo_text = respone_seo.text
    name_r = re.compile(r'<div id="company"><span>名称:</span><strong>(.*?)</strong>')
    name = name_r.findall(seo_text)
    return name[0]

def icp():
    #把SEO函数中的备案公司名丢入ICP备案公司反查
    name = seo()
    #默认
    paramsPost = {"s":name,"type":"com"}
    cookies = {"CNZZDATA5082706":"cnzz_eid%3D1962878551-1583683775-http%253A%252F%252Fseo.chinaz.com%252F%26ntime%3D1583683775","UM_distinctid":"170bafcceee316-07a88add20f6f7-5701732-144000-170bafcceef593","qHistory":"aHR0cDovL2ljcC5jaGluYXouY29tLyvnvZHnq5nlpIfmoYh8aHR0cDovL3Nlby5jaGluYXouY29tX1NFT+e7vOWQiOafpeivog=="}
    headers = {"Origin":"http://icp.chinaz.com","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36","Referer":"http://icp.chinaz.com/%E6%B1%89%E5%BA%AD%E6%98%9F%E7%A9%BA%EF%BC%88%E4%B8%8A%E6%B5%B7%EF%BC%89%E9%85%92%E5%BA%97%E7%AE%A1%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8","Connection":"close","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","Content-Type":"application/x-www-form-urlencoded"}

    try:
        icp = session.post("http://icp.chinaz.com/{}".format(name), data=paramsPost, headers=headers, cookies=cookies, timeout=5)
    except:
        print("检查一下网站能否访问或者系统代理")

    #第一次正则查询，拿到部分代码
    icp_text =icp.text
    code_r = re.compile(r"<td class='tc'>(.*?)</td>")
    code_end = code_r.findall(icp_text)
    #域̶名̶正̶则̶，̶拿̶出̶最̶后̶域̶名̶,这个匹配搞死我了，才发现range才是真爱
    for i in range(0, len(code_end), 6):
        print(code_end[i])

if __name__ == '__main__':
    print(logo)
    icp()