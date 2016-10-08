# -*- coding: utf-8 -*- 
'''
Created on 2016年10月08日
@author: shenyanf
'''

import xlrd
import urllib
from achievestockinfo import AchieveSSEStockInfo
from openpyxl.reader.excel import load_workbook
from openpyxl.styles.borders import Border, Side
from myutil import MyUtil

class ASharesStocks:
    '''目前从深圳交易所下载下来的《上市公司列表》格式就有问题，[无语...]，因此xls2xlsx 还有自动向深圳《上市公司列表》中
    追加上海交易所上市公司信息都是不可能的，只能先手动下载深圳《上市公司列表》，再手动另存为xlsx格式，然后抓取上海上市公司信息，然后追加到上述表格中'''
    
    # file absolute path
    filePath = u"d:\\A股上市公司列表.xlsx"
    
    # xlsx 标题
    __indexName = [u'公司代码', u'公司简称', u'公司全称', u'英文名称', u'注册地址', u'A股代码', u'A股简称', u'A股上市日期', u'A股总股本', u'A股流通股本',
                   u'B股代码', u'B股简称', u'B股上市日期', u'B股总股本', u'B股流通股本', u'地 区', u'省 份', u'城 市', u'所属行业', u'公司网址']
    
    def appendSSEStocks(self):
        """
        向表格中追加上交所上市公司信息
        """
        wb = load_workbook(self.filePath)
        sheet = wb.active
#         print sheet.max_row
        # 设置单元格所有框线
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))   
#         # 写标题
#         for i in range(self.__indexName.__len__()):
#             _ = sheet.cell(column=i + 1, row=1, value=self.__indexName[i])
        # 当前表格的信息行数
        row = sheet.max_row
        for i in self.__getAShareListCompanyCode():
            a = AchieveSSEStockInfo(i)
             
#             print a.getStatus()
            if not a.getStatus():
                continue
             
            for j in range(a.__public__.__len__()):
                m = a.__public__[j]
                f = getattr(a, m)
                print m
                print f()
                _ = sheet.cell(column=j + 1, row=row, value="%s" % f())
                sheet.cell(column=j + 1, row=row).border = thin_border
            row = row + 1
            
            if int(i) % 100 == 0:
                wb.save(self.filePath)
        wb.save(self.filePath)
            
    def downloadSZSEAShares(self):
        """
        下载深圳交易所上市公司信息.
        """
        dls = r"http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=EXCEL&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1"
        urllib.urlretrieve(dls, self.filePath)

        
    def xls2xlsx(self):
        """
        该方法目前不可用
        """
        # first open using xlrd
        book = xlrd.open_workbook(self.filePath)
        index = 0
        nrows, ncols = 0, 0
        while nrows * ncols == 0:
            sheet = book.sheet_by_index(index)
            nrows = sheet.nrows
            ncols = sheet.ncols
            index += 1
    
        # prepare a xlsx sheet
        book1 = xlrd.open_workbook()
        sheet1 = book1.active
    
        for row in xrange(1, nrows):
            for col in xrange(1, ncols):
                sheet1.cell(row=row, column=col).value = sheet.cell_value(row, col)
        
        book1.save(filename=u'd:\\A.xlsx')
        return book1
    
    def __mergeURL(self, pageNum, firstPage=True):
        """
        @param pageNum: 第几页
        @param firstPage:  是否是第一页，为true时，url不需要拼接endPage
        @return:    合成的url
        """
        return 'http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback53818&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=' + pageNum + '&pageHelp.pageSize=25' + (firstPage and '&pageHelp.endPage=' + pageNum + '1' or '') + '&pageHelp.pageNo=' + pageNum + '&_=1475850022386'
    
    def __getAShareListCompanyCode(self):
        """
        @return: 返回所有上市公司的股票代码
        """
        l = []
        referer = r'http://www.sse.com.cn/assortment/stock/list/share/'
#         第一次获取表格首页信息及总页数等信息
        jsonCallBackPythonObjData = MyUtil.getDatas(self.__mergeURL('1'), referer)
        if not jsonCallBackPythonObjData:
            return None
        else:
            # 总页数
            pageCount = jsonCallBackPythonObjData.pageHelp.pageCount
            # 每页多少条记录
            pageSize = jsonCallBackPythonObjData.pageHelp.pageSize
            # 总共多少上市公司
            total = jsonCallBackPythonObjData.pageHelp.total

        for i in range(1, pageCount + 1):
            # 获取第i页上市公司信息
            jsonCallBackPythonObjData = MyUtil.getDatas(self.__mergeURL(str(i), False), referer)
            for j in range(0, pageSize):
                datas = jsonCallBackPythonObjData.pageHelp.data[j]
                rsDict = dict((name, getattr(datas, name)) for name in dir(datas) if not name.startswith('__'))
                companyCode = rsDict.get('COMPANY_CODE').encode('utf-8')
                print companyCode
                l.append(companyCode)
        
        if len(l) != total:
            print 'The total does not match the actual'
        
        return l

if __name__ == '__main__':
    s = ASharesStocks()
#     s.downloadSZSEAShares()
    s.appendSSEStocks()
