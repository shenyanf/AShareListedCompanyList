# -*- coding: utf-8 -*- 
'''
Created on 2016年10月08日
@author: shenyanf
'''
from myutil import MyUtil
import datetime

class AchieveSSEStockInfo:
    '''获得上海证卷交易所股票信息.'''

    # 方法名由数据库表中的字段和'get'前缀拼接而成
    methodList = map(lambda x:'get' + x, map(MyUtil.firstCharUpper, list(MyUtil.indexs.split(','))))
    
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
        '''
        公司上市代码
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('COMPANY_CODE')
    
    def getStatus(self):
        '''
        公司上市状态
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        v = self.__getBasicValue('STATE_CODE_A_DESC') + '/' + self.__getBasicValue('STATE_CODE_B_DESC')
#         print v
        if v == '-/-' or u'摘牌' in v:
            return False
        else:
            return True
    
    def getCompanyShortName(self):
        '''
        公司简称
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('COMPANY_ABBR') + '/' + self.__getBasicValue('ENGLISH_ABBR')
    
    def getCompanyName(self):
        '''
        公司名称
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('FULLNAME')
    
    def getCompanyEnlishName(self):
        '''
        公司英文名称
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return MyUtil.delChinese(self.__getBasicValue('FULL_NAME_IN_ENGLISH'))
    
    def getIpoAddress(self):
        '''
        公司上市地址
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('COMPANY_ADDRESS')
    
    def getASharesCode(self):
        '''
        公司A股代码
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('SECURITY_CODE_A')
    
    def getASharesShortName(self):
        '''
        公司A股简称
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('COMPANY_ABBR') + '/' + self.__getBasicValue('ENGLISH_ABBR')
    
    def getASharesIPODate(self):
        '''
        公司A股IPO时间
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        result = ''
        str(self.stockCode)
        try:
            rsDict = MyUtil.getDatas(url=self.basicURLB, referer=self.referer)
            if rsDict == '-' or rsDict is None:
                result = '-'
            else:
                if isinstance(rsDict, list):
                    ipoDate = rsDict[0]
                else:
                    ipoDate = rsDict
#                 print ipoDate
                result = ipoDate.get('LISTINGDATEA')
        except:
            result = '-'
        return result
        

    def getTotalCapital(self):
        '''
        总股本
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''      
        return self.__getCapitalValue('totalShares')
    
    def getASharesTotalCapital(self):
        '''
        A股总股本
    @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        aShareTotalShare = 0.0
        
        AShareNonFlowShare = self.__getCapitalValue('totalNonFlowShare')
        AShareFlowShare = self.getASharesOutstandingCaptial()
         
        if  AShareNonFlowShare != '-' and  AShareNonFlowShare:
            aShareTotalShare += float(AShareNonFlowShare)
        if AShareFlowShare != '-' and AShareFlowShare:
            aShareTotalShare += float(AShareFlowShare)

        return repr(aShareTotalShare)
    
    def getASharesOutstandingCaptial(self):
        '''
    A股流通股本
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getCapitalValue('AShares')
    
    def getBSharesTotalCapital(self):
        '''
        B股总股本
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.getBSharesOutstandingCaptial()
        
    def getBSharesOutstandingCaptial(self):
        '''
        B股流通股本
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getCapitalValue('BShares')
    
    def getBSharesCode(self):
        '''
        B股代码
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('SECURITY_CODE_B')
    
    def getBSharesShortName(self):
        '''
        B股简称
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesShortName()
    
    def getBSharesIPODate(self):
        '''
        B股IPO时间
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        result = ''
        try:
            rsDict = MyUtil.getDatas(url=self.basicURLC, referer=self.referer)
            if rsDict == '-' or rsDict is None:
                result = '-'
            else:
                if isinstance(rsDict, list):
                    ipoDate = rsDict[0]
                else:
                    ipoDate = rsDict
#                 print ipoDate
                result = ipoDate.get('LISTINGDATEB')
        except:
            result = '-'
        return result
        
    def getArea(self):
        '''
        上市公司所在地区
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('AREA_NAME_DESC')
    
    def getProvince(self):
        '''
        上市公司所在省份
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.getArea() 
    
    def getCity(self):
        '''
        上市公司所在城市
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.getArea() 
    
    def getTrade(self):
        '''
        上市公司所在行业
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return self.__getBasicValue('SSE_CODE_DESC')
#    CSRC行业(门类/大类/中类)
#    'CSRC_CODE_DESC') + '/' + self.__getBasicValue('CSRC_GREAT_CODE_DESC') + '/' + 
# self.__getBasicValue('CSRC_MIDDLE_CODE_DESC')
    
    def getWebsite(self):
        '''
        上市公司网址
        @return: 返回string类型;如果没有数据或发生异常，返回'-'
        '''
        return MyUtil.delChinese(self.__getBasicValue('WWW_ADDRESS'))
        
    
    def __getBasicValue(self, key):
        '''获得上市公司基本信息的值.
           @param key: string ,basic info index to fetch
           @return:  string, result of key
        '''
        result = ''
        try:
            # 首次使用该方法，需要访问url，获取网页内容
            if self.stockBasicInfo == None:
                rsDict = MyUtil.getDatas(url=self.basicURLA, referer=self.referer)
                if rsDict == '-' or rsDict is None:
                    result = '-'
                else:
                    # jsonObj 转换为字典类型
                    if isinstance(rsDict, list):
                        self.stockBasicInfo = rsDict[0]
                    else:
                        self.stockBasicInfo = rsDict
#                     print self.stockBasicInfo
            result = self.stockBasicInfo.get(key).strip()
        except:
            result = '-'
        
        if not isinstance(result, basestring):
            result = repr(result)
    
        return result
    
    def __getCapitalValue(self, key):
        '''获得上市公司股本信息的值.
            @param key: capital index
            @return:  string, result of key 
        '''
        result = ''
        try:
            # 首次使用该方法，需要访问url，获取网页内容
            if self.stockCapitalInfo == None:
                rsDict = MyUtil.getDatas(url=self.capitalURL, referer=self.referer)
                if rsDict == '-' or rsDict is None:
                    result = '-'
                else:
                    if isinstance(rsDict, list):
                        self.stockCapitalInfo = rsDict[0]
                    else:
                        self.stockCapitalInfo = rsDict
#                     print self.stockCapitalInfo
            result = self.stockCapitalInfo.get(key).strip()
        except:
            result = '-'
        
#         print result
        if not isinstance(result, basestring):
            result = repr(result)
    
        return result 
    
    def __mergeBasicURL(self, sqlId, stockCode):
        ''' 股票代码和sqlId组合成ajax请求的url
        @param sqlId:  info type, get from chrome develop console(F12), like:COMMON_SSE_ZQPZ_GP_GPLB_C
        @param stockCode: 股票代码
        @return: string , request url'''
        return 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=' + MyUtil.CALLBACKMETHODNAME + \
    '&isPagination=false&sqlId=' + sqlId + '&productid=' + str(stockCode) + '&_='
    
    def __init__(self, stockCode):
        ''' 
        basicURLA、basicURLB、basicURLC、basicURLD、capitalURL、disclosure 结尾的'_'需要赋值为当前时间戳，myutil getDatas中会加上
        @param stockCode: 股票代码
        '''
        today = datetime.date.today().strftime('%Y%m%d')
        
        self.stockCode = stockCode
        # 公司概况
        self.basicURLA = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_C', stockCode)
        # A股上市时间
        self.basicURLB = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C', stockCode)
        # B股上市时间
        self.basicURLC = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C', stockCode)
        # 秘书信息
        self.basicURLD = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C', stockCode)
        
        # 获得上市公司股本信息的值
        self.capitalURL = 'http://query.sse.com.cn/security/stock/queryCompanyStockStruct.do?jsonCallBack=' + \
        'jsonpCallback86976&isPagination=false&companyCode=' + str(stockCode) + '&_='
       
        # request header refer，请求头中的refer信息
        self.referer = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=' + \
        str(self.stockCode)
        
        # 市场日历，季报、半年报、年报、分红等公告信息  暂时没有用到
        self.disclosure = 'http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback86207&' + \
        'isPagination=true&stockCode=600066&tradeBeginDate=19700101&tradeEndDate=' + today + '&order=' + \
        'tradeBeginDate%7Cdesc&sqlId=PL_SCRL_SCRLB&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1' + \
        '&pageHelp.endPage=1&pageHelp.pageSize=5&_='
        
        # 当前股票的基本信息
        self.stockBasicInfo = None
        # 当前股票的股本信息
        self.stockCapitalInfo = None

    def allCompanyInfo(self):
        '''
        当前公司的所有信息
        map reduce used, need __callMethod
        @return list, all index's value of company
        '''
        l = map(self.__callMethod, self.methodList)
        print l
        return l
    
    def __callMethod(self, methodName):
        '''
        由方法名变为方法调用
        change string to method 
        @return call method, it just like self.methodName()
        '''
        return getattr(self, methodName)()
    
        
if __name__ == '__main__':
    a = AchieveSSEStockInfo(603227)
    print a.allCompanyInfo()
