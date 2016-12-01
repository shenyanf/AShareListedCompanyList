# -*- coding: gbk -*- 
'''
Created on 2016年4月19日
@author: shenyf
'''
import urllib2
import re
import string

class AchieveSSEStockInfo_Deprecated:
    '''获得上海证卷交易所股票信息.'''
    
    # 默认的获取指标值的表达式
    __patternStr = "<td.+>(.+)</td>"
    # 访问页面成功
    __urlAccessSuccess = False
    
    # 指标的方法，顺序已经排好，请不要乱动
    __public__ = ['getCompanyCode', 'getCompanyShortName', 'getCompanyName', 'getCompanyEnlishName', 'getIpoAddress', 'getASharesCode',
                  'getASharesShortName', 'getASharesIPODate', 'getASharesTotalCapital', 'getASharesOutstandingCaptial', 'getBSharesCode',
                  'getBSharesShortName', 'getBSharesIPODate', 'getBSharesTotalCapital', 'getBSharesOutstandingCaptial', 'getArea',
                  'getProvince', 'getCity', 'getTrade', 'getWebsite']
    '''
    all indexs as follow:
        companyCode     公司代码
        companyShortName     公司简称
        companyName      公司全称
        companyEnlishName      英文名称
        ipoAddress      注册地址
        aSharesCode      A股代码
        aSharesShortName      A股简称
        aSharesIPODate      A股上市日期
        aSharesTotalCapital      A股总股本
        aSharesOutstandingCaptial      A股流通股本
        bSharesCode      B股代码
        bSharesShortName      B股简称
        bSharesIPODate      B股上市日期 
        bSharesTotalCapital       B股总股本  
        bSharesOutstandingCaptial      B股流通股本
        area      地区 
        province      省份
        city      城市
        trade      所属行业
        website      公司网址
        
        status A股状态/B股状态
    '''
    
    def getCompanyCode(self):
        return self.__getBasicValue(u'公司代码')
    
    def getStatus(self):
        v = self.__getBasicValue(u'A股状态/B股状态', pattern='<td>(.+)</td>')
#         print v
        if v == 0 or u'摘牌' in v:
            return False
        else:
            return True
    
    def getCompanyShortName(self):
        return self.__getBasicValue(u'公司简称')
    
    def getCompanyName(self):
        return self.__getBasicValue(u'公司全称').split('/')[0]
    
    def getCompanyEnlishName(self):
        return self.__getBasicValue(u'公司全称').split('/')[1]
    
    def getIpoAddress(self):
        return self.__getBasicValue(u'注册地址')
    
    def getASharesCode(self):
        return self.__getBasicValue(u'股票代码(A股/B股)').split('/')[0]
    
    def getASharesShortName(self):
        return self.__getBasicValue(u'公司简称')
    
    def getASharesIPODate(self):
        return self.__getBasicValue(u'上市日(A股/B股)', '.*<a.+>(\d{4}-\d{2}-\d{2})</a>')

    def getASharesTotalCapital(self):      
        return self.__getCapitalValue(u'股份总数')
    
    def getASharesOutstandingCaptial(self):
        return self.__getCapitalValue(u'已流通股份合计')
    
    def getBSharesCode(self):
        return self.__getBasicValue(u'股票代码(A股/B股)').split('/')[1]
    
    def getBSharesShortName(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesShortName()
    
    def getBSharesIPODate(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.__getBasicValue(u'上市日(A股/B股)', '.*<a.+>/(.+)</a>.*')
    
    def getBSharesTotalCapital(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesTotalCapital()  
    
    def getBSharesOutstandingCaptial(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesOutstandingCaptial()
    
    def getArea(self):
        return self.__getBasicValue(u'所属省/直辖市')
    
    def getProvince(self):
        return self.__getBasicValue(u'所属省/直辖市') 
    
    def getCity(self):
        return self.__getBasicValue(u'所属省/直辖市') 
    
    def getTrade(self):
        return self.__getBasicValue(u'CSRC行业')
    
    def getWebsite(self):
        return self.__getBasicValue(u'网址', '.+>(.+)</a></td>')
        
    def __getPage(self, url):
        '''获取指定地址的html内容 .'''
        
        request = urllib2.Request(url)
        # 下列参数实际上可以不设置
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Encoding', 'gzip, deflate, sdch')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        request.add_header('Cache-Control', 'max-age=0')
        request.add_header('Connection', 'keep-alive')
        request.add_header('Host', 'biz.sse.com.cn')
        request.add_header('Upgrade-Insecure-Requests', '1')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36')
        
        # 尝试5次，如果每次都是timeout，打印提示信息，返回none 
        Max_Num = 5
        for i in range(Max_Num):
            try:    
                response = urllib2.urlopen(url=request, timeout=15)
                self.__urlAccessSuccess = True
                break
            except:
                pass
            
            if i < Max_Num - 1:
                continue
            else:
                print 'URLError: <urlopen error timed out> All times is failed '
                return None
        
        # gbk包含gb2312
        response.encoding = 'gbk'
        result = response.read()
        # 消除行结尾为br的情况,拿到的页面是以\r\n换行
        result = result.replace("<br>\r\n", '/').replace('<BR>\r\n', '/')
#         print result
        return  unicode(result, "gbk")
    
    def __locateIndex(self, resultList, key):
        """获得指定指标所在行数."""
        
        # 获得指标所在行
        for i in range(0, resultList.__len__()):
    #         print 'list' + resultList[i]
            if key in resultList[i]:
                    return  i
        # 如果没有查到指标，返回-1
        return -1    
    
    def __getValue(self, key, resultList, pattern):
        '''获得指标的值 '''
        
        lineStartAndEnd = '^<td.+</td>'
        sourceStr = ''
        
        lineNumber = self.__locateIndex(resultList, key)
        
        # 如果没有指标所在行为-1，值直接返回0
        if lineNumber == -1:
            return 0
            
        for i in range(lineNumber, resultList.__len__()):
            sourceStr = sourceStr + resultList[i + 1].replace('\r\n', '')
        #       print sourceStr
            # 如果不满足<td>*</td>形式,多行拼接为一行
            m = re.match(lineStartAndEnd, sourceStr)
            if m:
                m = re.match(pattern, sourceStr)
                if m:
#                     print key + " " + m.group(1)
                    return m.group(1)
                else:
                    break
            else:
                i = i + 1
        return 0
    
    def __getBasicValue(self, key, pattern=__patternStr):
        '''获得上市公司基本信息的值.'''
        
        # 首次使用该方法，需要访问url，获取网页内容
        if self.basicResultList == None:
            result = self.__getPage(self.url)
            if self.__urlAccessSuccess:
                self.basicResultList = result.split('\r\n')
        
        # 如果第一次getPage 访问失败，该股相关指标直接返回None，不再继续尝试访问页面
        if not self.__urlAccessSuccess:
            return None
        
        return self.__getValue(key, self.basicResultList, pattern)

    def __getCapitalValue(self, key, pattern=__patternStr):
        '''获得上市公司股本信息的值.'''
        
        # 首次使用该方法，需要访问url，获取网页内容
        if self.capitalResultList == None:
            result = string.lower(self.__getPage(self.capitalUrl))
            if self.__urlAccessSuccess:
                self.capitalResultList = result.split('\r\n')
                
        # 如果第一次getPage 访问失败，该股相关指标直接返回None，不再继续尝试访问页面
        if not self.__urlAccessSuccess:
                return None
        
        return self.__getValue(key, self.capitalResultList, pattern)
    
    def __init__(self, stockCode):
        self.url = r'http://biz.sse.com.cn/sseportal/webapp/datapresent/SSEQueryListCmpAct?reportName=QueryListCmpRpt&COMPANY_CODE=' + str(stockCode) + '&REPORTTYPE=GSZC&PRODUCTID=' + str(stockCode)
        self.capitalUrl = r'http://biz.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStckStructAct?PRODUCT=' + str(stockCode) + '&COMPANYCODE=' + str(stockCode)
        self.basicResultList = None
        self.capitalResultList = None
        pass 
    
        
if __name__ == '__main__':
    a = AchieveSSEStockInfo(600292)
    for c in a.__public__:
        f = getattr(a, c)
        print c 
        print f()
    
    print a.getStatus()
