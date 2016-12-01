# -*- coding: utf-8 -*- 
'''
Created on 2016年10月08日
@author: shenyanf
'''

import urllib2
import json
from time import sleep
import mysql.connector
from mysql.connector import errorcode

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

class MyUtil:
    CALLBACKMETHODNAME = 'jsonpCallback12345'
    
    @classmethod
    def getDatas(cls, url, referer=None):
        '''获取指定地址的html内容 .
        @param  url: request url
        @param referer: request header's referer
        @return: a instance of JSONObject'''
        
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
        
        # 尝试3次，如果每次都是timeout，打印提示信息，返回none 
        maxNum = 3
        for i in range(maxNum):
            try:    
                response = urllib2.urlopen(url=request, timeout=2)
                # 慢一点 不然被屏蔽
                sleep(0.3)
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
        
        str2JsonData = str(result)[len(cls.CALLBACKMETHODNAME) + 1:-1]
        pythonObjData = json.loads(str2JsonData, object_hook=JSONObject)
        
        return pythonObjData
    
    @classmethod
    def getConnection(cls):
        '''
        @return: a connection instance
        '''
        try:
            cnx = mysql.connector.connect(user='root', password='mysql',
                              host='127.0.0.1',
                              database='test', charset='utf8')
        except mysql.connector.Error as err:
            cnx = None
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            
        return cnx
    
    @classmethod
    def closeConn(cls, cnx):
        '''
        close connection
        @param cnx: connection which to close
        '''
        try:
            cnx.close()
        except Exception, e:
            print e
    
    @classmethod   
    def delChinese(cls, checkStr):
        '''
        replace chinese with ' '  in  checkStr
        @return str not contain chinese 
        '''
        
        return ''.join([x if 'a' <= x <= 'z' or 'A' <= x <= 'Z' or x == ',' or x == '.'  or '0' <= x <= '9' else ' '  for x in checkStr])
      
    indexs = 'companyCode, companyShortName, companyName, companyEnlishName , ipoAddress, aSharesCode , aSharesShortName, aSharesIPODate, \
  aSharesTotalCapital, aSharesOutstandingCaptial, bSharesCode, bSharesShortName, bSharesIPODate, bSharesTotalCapital, bSharesOutstandingCaptial, area, \
  province, city, trade, website'
  
    addCompany = "insert into listed_company(" + indexs + ') values(' + '%s,' * 19 + "%s)"
    
    selectCompany = "select %s from listed_company"
    
    selectCompanyCode = selectCompany.replace('%s', 'companyCode')
    
    selectSSECompanyCode = selectCompanyCode + " where companyCode like '6%'"
    
    selectSZSECompanyCode = selectCompanyCode + " where companyCode like '3%' or companyCode like '0%'"
    # just for test 
    testInsert = "insert into listed_company(companyName,status) values(%s,%s)"
