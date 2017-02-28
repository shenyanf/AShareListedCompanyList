#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 2016年11月22日

@author: 58
'''
from mysql.connector import connection
from openpyxl.reader.excel import load_workbook
from myutil import MyUtil
from operateDB import OperateDB
import re
import time
from string import zfill

class MyClass():
    '''
    classdocs
'''
    def test(self):
        add_company = ('''insert into listed_company(companyCode,companyShortName,  companyName,  companyEnlishName ,  
        ipoAddress,  aSharesCode ,  aSharesShortName,  aSharesIPODate, aSharesTotalCapital,  aSharesOutstandingCaptial,  
        bSharesCode,  bSharesShortName,  bSharesIPODate,  bSharesTotalCapital,  bSharesOutstandingCaptial,  area,
        province,  city,  trade,  website) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''')
        data_company = ('000011', '深物业A', '深圳市物业发展(集团)股份有限公司', '''SHENZHEN PROPERTIES & RESOURCES DEVELOPMENT 
        (GROUP)CO., LTD''', '广东省深圳市人民南路国贸大厦39、42层', '11', '深物业A', '1992/3/30', '528,373,849', '175,831,365',
        '200011', '深物业B', '1992/3/30', '67,605,243', '67,605,243', '华南', '广东', '深圳市', 'K 房地产', 'www.szwuye.com.cn')
        cnx = connection.MySQLConnection(user='root', password='mysql',
                              host='127.0.0.1',
                              database='test')
        cursor = cnx.cursor()
        cursor.execute(add_company, data_company)
        cnx.commit()
        cursor.close()
        cnx.close()
    
    def fib(self, max):
        a, b = 0, 1
        while b < max:
            yield b
            a, b = b, a + b

    def f(self, x):
        return x * x
    
    def readXlsx(self):
        l = []
        wb = load_workbook(u"d:\\A股上市公司列表.xlsx")
        sheet = wb.active
        sum = 0
        for row in sheet.iter_rows():
            if sum == 0:
                sum = 1
                continue
            for num in range(len(row)):
                v = row[num].value
                l.append('%s' % v)
                print v
#                 if num == 7 or num == 12:
#                     ipoDate = str(row[num].value)[18:-7].replace(', ', '-')
#                     print ipoDate
            sum += 1
            print sum 
            print tuple(l)
          
def firstCharUpper(strr):
    srcStr = strr.strip()
    destStr = ''
    for i in range(len(srcStr)):
        if i == 0:
           destStr = srcStr[i].upper()
        else:
            destStr += srcStr[i]
    return destStr
            
def getWeather():
    print time.time()
    print MyUtil.getDatas("http://d1.weather.com.cn/sk_2d/101010100.html?_=", "http://www.weather.com.cn/weather1d/101010100.shtml")

def test():
    code = str(1)
    print code.zfill(6)
    
if __name__ == '__main__':
    print u'\u9ec4\u5c71\u65c5\u6e38/HSTD'.encode('utf8')
    mc = MyClass()
    test()
    
#     mc.readXlsx()
    l = ['adb', 'abc']
    print tuple(l)
    print len('ANHUI WANWEI UPDATED HIGH-TECH MATERIAL INDUSTRY COMPANY LIMITED')

    print l.sort()
    print l
    ll = list(MyUtil.indexs.split(','))
    print ll
    print map(lambda x:'get' + x, map(firstCharUpper, ll))
    
    downLoadSZSE = raw_input("download szse xls?Y|N")
#     print downLoadSZSE
    m = re.search('^[Y|y][E|e]{0,}[S|s]{0,}', downLoadSZSE)
    if m  :
        print m.group()
    else:
        print 'ddd'
    getWeather()
