# -*- coding: utf-8 -*- 
'''
Created on 2016年10月08日
@author: shenyanf
'''

import urllib2
import json
from time import sleep

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

class MyUtil:
    @classmethod
    def getDatas(cls, url, referer=None):
        '''获取指定地址的html内容 .'''
        
        request = urllib2.Request(url)

        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Encoding', 'gzip, deflate, sdch')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        request.add_header('Cache-Control', 'max-age=0')
        request.add_header('Connection', 'keep-alive')
        request.add_header('Host', 'query.sse.com.cn')
        request.add_header('Upgrade-Insecure-Requests', '1')
        request.add_header('Referer', referer)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36')
        
        # 尝试5次，如果每次都是timeout，打印提示信息，返回none 
        maxNum = 5
        for i in range(maxNum):
            try:    
                response = urllib2.urlopen(url=request, timeout=15)
                # 慢一点 不然被屏蔽
                sleep(1)
                break
            except:
                pass
            
            if i < maxNum - 1:
                continue
            else:
                print 'URLError: <urlopen error timed out> All times is failed '
                return None
        
        response.encoding = 'utf-8'
        result = response.read()
#         print result
        
        str2JsonData = str(result).split('(')[1].split(')')[0]
        pythonObjData = json.loads(str2JsonData, object_hook=JSONObject)
        
#         print pythonObjData
        return pythonObjData
