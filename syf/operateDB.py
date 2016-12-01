# -*- coding:utf-8 -*-
'''
Created on 2016年11月22日

@author: 58
'''
from syf.myutil import MyUtil
from achievestockinfo import AchieveSSEStockInfo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class OperateDB():
    '''
    操作数据库相关，保存到数据库，修改，查询等
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def addCompany(self, sql, values):
        '''
        add company to dataase
        @param sql: which will execute
        @param values: tuple type, insert values
        @return: add company status, True or False
        '''
        # get connection
        cnx = MyUtil.getConnection()
        # get cursor
        cursor = cnx.cursor()
        print sql
        print values
        try:
            # execute sql
            cursor.execute(sql, values)
        except Exception, e:
            print e
            res = False
        else:
            # commit
            cnx.commit()
            # close resources
            cursor.close()
            MyUtil.closeConn(cnx)
            res = True
            print 'add company  success'
        return res

    def selectFromCompany(self, sql):
        '''
        select some values from database
        @param sql: which will execute
        @return: dict, return all result 
        '''
        cnx = MyUtil.getConnection()
        cursor = cnx.cursor()
        cursor.execute(sql)
        h = {}
        for allIndex in cursor:
            l = []
#             print  allIndex
            # add value to list l
            for i in range(len(allIndex)):
                l.append(allIndex[i].encode('utf-8'))
            # add l to dict h
            h[len(h)] = l
        
        cursor.close()
#         for i in range(len(h)):
#             for j in range(len(h[i])):
#                 print h[i][j]
        MyUtil.closeConn(cnx)
        return h
        
    def selectSSEAllCompanyCode(self):
        '''
        get all sse company code from database
        @return: list
        '''
        sql = MyUtil.selectSSECompanyCode
        resMap = self.selectFromCompany(sql)
        l = []
        for m in resMap:
            l.append(resMap[m][0])
        return l
        
    def selectSZSEAllCompanyCode(self):
        '''
        get all szse company code from database
        @return: list
        '''
        sql = MyUtil.selectSZSECompanyCode
        resMap = self.selectFromCompany(sql)
        l = []
        for m in resMap:
            l.append(resMap[m][0])
        return l
    
if __name__ == '__main__':
    a = OperateDB()
#     a.selectFromCompany(MyUtil.selectComany.replace('%s', MyUtil.indexs))
    print a.selectSZSEAllCompanyCode()
#     b = AchieveSSEStockInfo(600054)
#     l = ""
#     for j in range(b.__public__.__len__()):
#         m = b.__public__[j]
#         f = getattr(b, m)
#         if True:
#             print m, f()
#             if not f():
#                 l += 'NULL'
#             try:
#                 l += f().strip() 
#             except:
#                 l += repr(f()).strip()
#             print l
#             if j != b.__public__.__len__() - 1:
#                 l += '|'
#         print l
#     a.addCompany(MyUtil.addCompany, tuple(item for item in l.split('|')))
