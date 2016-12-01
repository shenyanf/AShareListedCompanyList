# -*- coding: utf-8 -*- 
'''
Created on 2016年10月08日
@author: shenyanf
'''

from myutil import MyUtil

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

class AchieveSSEStockInfo:
    '''获得上海证卷交易所股票信息.'''
    
    # 指标的方法，顺序已经排好，请不要乱动
    __public__ = ['getCompanyCode', 'getCompanyShortName', 'getCompanyName', 'getCompanyEnlishName', 'getIpoAddress', 'getASharesCode',
                  'getASharesShortName', 'getASharesIPODate', 'getASharesTotalCapital', 'getASharesOutstandingCaptial', 'getBSharesCode',
                  'getBSharesShortName', 'getBSharesIPODate', 'getBSharesTotalCapital', 'getBSharesOutstandingCaptial', 'getArea', 'getProvince', 'getCity', 'getTrade', 'getWebsite']
    
    achieveIndexFromURLA = ['CHANGEABLE_BOND_ABBR', 'OFFICE_ZIP', 'AREA_NAME_DESC', 'FULL_NAME_IN_ENGLISH', 'COMPANY_CODE', 'CSRC_MIDDLE_CODE_DESC', 'SECURITY_ABBR_A', 'COMPANY_ADDRESS', 'SECURITY_CODE_A', 'SECURITY_CODE_B', 'SECURITY_30_DESC', 'COMPANY_ABBR', 'OFFICE_ADDRESS', 'CHANGEABLE_BOND_CODE', 'ENGLISH_ABBR', 'LEGAL_REPRESENTATIVE', 'REPR_PHONE', 'E_MAIL_ADDRESS', 'FOREIGN_LISTING_ADDRESS', 'STATE_CODE_A_DESC', 'SSE_CODE_DESC', 'FOREIGN_LISTING_DESC', 'SECURITY_CODE_A_SZ', 'CSRC_GREAT_CODE_DESC', 'WWW_ADDRESS', 'CSRC_CODE_DESC', 'STATE_CODE_B_DESC', 'FULLNAME']
    
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
        return self.__getBasicValue('COMPANY_CODE')
    
    def getStatus(self):
        v = self.__getBasicValue('STATE_CODE_A_DESC') + '/' + self.__getBasicValue('STATE_CODE_B_DESC')
#         print v
        if v == '-/-' or u'摘牌' in v:
            return False
        else:
            return True
    
    def getCompanyShortName(self):
        return self.__getBasicValue('COMPANY_ABBR') + '/' + self.__getBasicValue('ENGLISH_ABBR')
    
    def getCompanyName(self):
        return self.__getBasicValue('FULLNAME')
    
    def getCompanyEnlishName(self):
        return MyUtil.delChinese(self.__getBasicValue('FULL_NAME_IN_ENGLISH'))
    
    def getIpoAddress(self):
        return self.__getBasicValue('COMPANY_ADDRESS')
    
    def getASharesCode(self):
        return self.__getBasicValue('SECURITY_CODE_A')
    
    def getASharesShortName(self):
        return self.__getBasicValue('COMPANY_ABBR') + '/' + self.__getBasicValue('ENGLISH_ABBR')
    
    def getASharesIPODate(self):
        result = ''
        referer = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=' + str(self.stockCode)
        try:
            rsDict = MyUtil.getDatas(self.basicURLB, referer)
            if rsDict == '-' or rsDict is None:
                result = '-'
            else:
                ipoDate = dict((name, getattr(rsDict.result[0], name)) for name in dir(rsDict.result[0]) if not name.startswith('__'))
                print ipoDate
                result = ipoDate.get('LISTINGDATEA')
        except:
            result = '-'
        return result
        

    def getTotalCapital(self):      
        return self.__getCapitalValue('totalShares')
    
    def getASharesTotalCapital(self):
        aShareTotalShare = 0.0
        
        AShareNonFlowShare = self.__getCapitalValue('totalNonFlowShare')
        AShareFlowShare = self.getASharesOutstandingCaptial()
         
        if  AShareNonFlowShare != '-' and  AShareNonFlowShare:
            aShareTotalShare += float(AShareNonFlowShare)
        if AShareFlowShare != '-' and AShareFlowShare:
            aShareTotalShare += float(AShareFlowShare)

        return repr(aShareTotalShare)
    
    def getASharesOutstandingCaptial(self):
        return self.__getCapitalValue('AShares')
    
    def getBSharesTotalCapital(self):
        return self.getBSharesOutstandingCaptial()
        
    def getBSharesOutstandingCaptial(self):
        return self.__getCapitalValue('BShares')
    
    def getBSharesCode(self):
        return self.__getBasicValue('SECURITY_CODE_B')
    
    def getBSharesShortName(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesShortName()
    
    def getBSharesIPODate(self):
        result = ''
        referer = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=' + str(self.stockCode)
        try:
            rsDict = MyUtil.getDatas(self.basicURLC, referer)
            if rsDict == '-' or rsDict is None:
                result = '-'
            else:
                ipoDate = dict((name, getattr(rsDict.result[0], name)) for name in dir(rsDict.result[0]) if not name.startswith('__'))
                print ipoDate
                result = ipoDate.get('LISTINGDATEB')
        except:
            result = '-'
        return result
        
    def getArea(self):
        return self.__getBasicValue('AREA_NAME_DESC')
    
    def getProvince(self):
        return self.getArea() 
    
    def getCity(self):
        return self.getArea() 
    
    def getTrade(self):
        return self.__getBasicValue('SSE_CODE_DESC')
#    CSRC行业(门类/大类/中类)
#    'CSRC_CODE_DESC') + '/' + self.__getBasicValue('CSRC_GREAT_CODE_DESC') + '/' + self.__getBasicValue('CSRC_MIDDLE_CODE_DESC')
    
    def getWebsite(self):
        return MyUtil.delChinese(self.__getBasicValue('WWW_ADDRESS'))
        
    
    def __getBasicValue(self, key):
        '''获得上市公司基本信息的值.
           @param key: string ,basic info index to fetch
           @return:  string, result of key
        '''
        result = ''
        referer = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=' + str(self.stockCode)
        try:
            # 首次使用该方法，需要访问url，获取网页内容
            if self.stockBasicInfo == None:
                rsDict = MyUtil.getDatas(self.basicURLA, referer)
                if rsDict == '-' or rsDict is None:
                    result = '-'
                else:
                    # jsonObj 转换为字典类型
                    self.stockBasicInfo = dict((name, getattr(rsDict.result[0], name)) for name in dir(rsDict.result[0]) if not name.startswith('__'))
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
        referer = 'http://www.sse.com.cn/assortment/stock/list/info/capital/index.shtml?COMPANY_CODE=' + str(self.stockCode)
        try:
            # 首次使用该方法，需要访问url，获取网页内容
            if self.stockCapitalInfo == None:
                rsDict = MyUtil.getDatas(self.capitalURL, referer)
                if rsDict == '-' or rsDict is None:
                    result = '-'
                else:
                    # jsonObj 转换为字典类型
                    self.stockCapitalInfo = dict((name, getattr(rsDict.result, name)) for name in dir(rsDict.result) if not name.startswith('__'))
#                     print self.stockCapitalInfo
            result = self.stockCapitalInfo.get(key).strip()
        except:
            result = '-'
        
#         print result
        if not isinstance(result, basestring):
            result = repr(result)
    
        return result 
        print '%s,%s' % (result, isinstance(result, basestring))
    
    def __mergeBasicURL(self, sqlId, stockCode):
        ''' base stockCode and info type to merge url
        @param sqlId:  info type, get from chrome develop console(F12), like:COMMON_SSE_ZQPZ_GP_GPLB_C
        @param stockCode:  list company code
        @return: string , request url'''
        return 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=' + MyUtil.CALLBACKMETHODNAME + '&isPagination=false&sqlId=' + sqlId + '&productid=' + str(stockCode) + '&_=14555555555552'
    
    def __init__(self, stockCode):
        ''' 
        generator
        @param stockCode: list company code
        '''
        self.stockCode = stockCode
        self.basicURLA = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_C', stockCode)
        # A股上市时间
        self.basicURLB = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C', stockCode)
        # B股上市时间
        self.basicURLC = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C', stockCode)
        # 秘书信息
        self.basicURLD = self.__mergeBasicURL('COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C', stockCode)
        self.basicURLE = r'http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback46644&isPagination=true&stockCode=' + str(stockCode) + '&tradeBeginDate=19700101&tradeEndDate=20161001&order=tradeBeginDate%7Cdesc&sqlId=PL_SCRL_SCRLB&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=1&pageHelp.pageSize=5&_=1475720975596'
        self.capitalURL = 'http://query.sse.com.cn/security/stock/queryCompanyStockStruct.do?jsonCallBack=jsonpCallback86976&isPagination=false&companyCode=' + str(stockCode) + '&_=1475732919742'
       
        self.stockBasicInfo = None
        self.stockCapitalInfo = None

    def allCompanyInfo(self):
        '''
        map reduce used, need __callMethod
        @return list, all index's value of company
        '''
        l = map(self.__callMethod, self.__public__)
        print l
        return l
    
    def __callMethod(self, methodName):
        '''
        change string to method 
        @return call method, it just like self.methodName()
        '''
        return getattr(self, methodName)()
    
if __name__ == '__main__':
    a = AchieveSSEStockInfo(603227)
    a.allCompanyInfo()
