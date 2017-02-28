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
import codecs
import settings
import os
from ConfigParser import ConfigParser

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

class MyUtil:
    # jsonp回调函数名称
    CALLBACKMETHODNAME = 'jsonpCallback12345'
    cp = None
    __instance = None
    fileName = ''
    
    def __new__(cls, *args, **kwd):
        '''
        确保当前类为单例
        @return: MyUtil instance
        '''
        if MyUtil.__instance is None:
            MyUtil.__instance = object.__new__(cls, *args, **kwd)
        print 'Myutil instance: %s ' % MyUtil.__instance
        return MyUtil.__instance
    
    def __init__(self):
        MyUtil.fileName = settings.ROOT_DIR + os.sep + 'database.conf'
        MyUtil.cp = ConfigParser()
        print '配置文件 %s' % MyUtil.fileName
        MyUtil.cp.read(MyUtil.fileName)
        
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
        request.add_header('User-Agent', '''Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) 
        Chrome/48.0.2564.97 Safari/537.36''')
        
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
            user = MyUtil.loadProperty('mysql', 'user')
            passwd = MyUtil.loadProperty('mysql', 'password')
            host = MyUtil.loadProperty('mysql', 'host')
            db = MyUtil.loadProperty('mysql', 'database')

            cnx = mysql.connector.connect(user=user, password=passwd, host=host, database=db, charset='utf8')
        except mysql.connector.Error as err:
            cnx = None
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"
            else:
                print err
                
            raise Exception('Can\'t connect to MySQL server')
        
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
        return ''.join([x if 'a' <= x <= 'z' or 'A' <= x <= 'Z' or x == ',' or x == '.'  or '0' <= x <= '9' else ' '  
                        for x in checkStr])
    
    @classmethod
    def firstCharUpper(cls, strr):
        '''
        把字符串第一个字符改成大写
        @param strr: 需要修改的字符串
        @return: string
        '''
        srcStr = strr.strip()
        destStr = ''
        for i in range(len(srcStr)):
            if i == 0:
                destStr = srcStr[i].upper()
            else:
                destStr += srcStr[i]
        return destStr   
        
    @classmethod
    def loadProperty(cls, section, key):
        '''
        从配置文件中获得key对应的值
        @param key: 参数名
        @return: 得到的结果string类型，如果没有取得值返回None
        '''
        if MyUtil.cp is None:
            MyUtil.cp = ConfigParser()
            if MyUtil.fileName is None:
                raise  Exception('%s配置文件没有找到' % MyUtil.fileName)
            MyUtil.cp.readfp(codecs.open(MyUtil.fileName, "r", "utf-8-sig"))
            
        s = MyUtil.cp.sections()
        try:
            if s is not None and section in s:
                value = MyUtil.cp.get(section, key)
            else:
                value = None
        except Exception, e:
            print e
            value = None

        return value 
    
    indexs = '''companyCode, companyShortName, companyName, companyEnlishName , ipoAddress, aSharesCode , 
    aSharesShortName, aSharesIPODate, aSharesTotalCapital, aSharesOutstandingCaptial, bSharesCode, bSharesShortName, 
    bSharesIPODate, bSharesTotalCapital, bSharesOutstandingCaptial, area,   province, city, trade, website'''
  
    addCompany = "insert into listed_company(" + indexs + ') values(' + '%s,' * 19 + "%s)"
    
    selectCompany = "select %s from listed_company"
    
    selectCompanyCode = selectCompany.replace('%s', 'companyCode')
    
    selectSSECompanyCode = selectCompanyCode + " where companyCode like '6%' and status =1"
    
    selectSZSECompanyCode = selectCompanyCode + " where (companyCode like '3%' or companyCode like '0%') and status =1"
    # just for test 
    testInsert = "insert into listed_company(companyName,status) values(%s,%s)"
