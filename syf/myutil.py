# -*- coding: utf-8 -*- 
'''
Created on 2016年10月08日
@author: shenyanf
'''

import json
from time import sleep
import mysql.connector
from mysql.connector import errorcode
import codecs
import settings
import os
from ConfigParser import ConfigParser
import time
import requests


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
    def getDatas(cls, url, reskey='result', referer=None):
        '''
        获取指定地址的html内容 .
        @param  url: 请求的url
        @param referer: request header's referer
        @param reskey: 返回的结果中的key
        @return: dict or list
        '''
        
        currentTime = '%.0f' % time.time()
        
        headers = {}
        headers['Host'] = 'query.sse.com.cn'
        headers['Connection'] = 'keep-alive'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        headers['Accept'] = '*/*'
        headers['Referer'] = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=600066'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        headers['Cookie'] = 'yfx_c_g_u_id_10000042=_ck18060816540419996375317846011; yfx_f_l_v_t_10000042=f_t_1528448044906__r_t_1528448044906__v_t_1528448044906__r_c_0; VISITED_MENU=%5B%229055%22%5D'
        
        print url
        # 尝试3次，如果每次都是timeout，打印提示信息，返回none 
        maxNum = 3
        for i in range(maxNum):
            try:    
                resp = requests.get(url + currentTime, verify=False, headers=headers)
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
        
        resp.encoding = 'utf-8'
        respContent = resp.text
        
        print respContent
        
        # 结果为jsonpCallback86976({xxxxxxxx})形式,需要转换为python dict类型
        jsonContent = respContent[len(cls.CALLBACKMETHODNAME) + 1:-1]
        # 最外层的dict类型
        objDict = json.loads(jsonContent, encoding='utf-8')
        
        # result 有可能为list,即使是list，但是也只有包含一个dict；也有可能直接就是dict
        if objDict.has_key(reskey):
            resultDict = objDict[reskey]
            return resultDict
        
        return  {}
        
    @classmethod
    def getConnection(cls):
        '''
        数据库连接，目前是直连，后期计划改为连接池
        @return: 数据库连接 
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
    
    # 数据库中的字段名称
    indexs = '''companyCode, companyShortName, companyName, companyEnlishName , ipoAddress, aSharesCode , 
    aSharesShortName, aSharesIPODate, aSharesTotalCapital, aSharesOutstandingCaptial, bSharesCode, bSharesShortName, 
    bSharesIPODate, bSharesTotalCapital, bSharesOutstandingCaptial, area,   province, city, trade, website'''
  
    # 入库sql语句
    addCompany = "insert into listed_company(" + indexs + ') values(' + '%s,' * 19 + "%s)"
    
    # 查询所有股票信息
    selectCompany = "select %s from listed_company"
    
    # 查询所有股票的代码
    selectCompanyCode = selectCompany.replace('%s', 'companyCode')
    
    # 查询上交所的股票信息
    selectSSECompanyCode = selectCompanyCode + " where companyCode like '6%' and status =1"
    
    # 查询深交所的股票信息
    selectSZSECompanyCode = selectCompanyCode + " where (companyCode like '3%' or companyCode like '0%') and status =1"
    

if __name__ == '__main__':
    referer = 'http://www.sse.com.cn/assortment/stock/list/info/capital/index.shtml?COMPANY_CODE=600066'
    url = 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback51357&isPagination=false&sqlId=COMMON_SSE_ZQPZ_GP_GPLB_C&productid=600066&_='
#     print MyUtil().getDatas(url=url, referer=referer)[0]['COMPANY_CODE']
    
