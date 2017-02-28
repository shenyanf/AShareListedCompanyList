# -*- coding:utf-8 -*-
'''
Created on 2016年11月22日

@author: 58
'''
import sys
from syf.myutil import MyUtil
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
            h[allIndex[0]] = l
        
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
        print 'get the SSE companyCode that has been stored in the database'
        
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
        
        print 'get the SZSE companyCode that has been stored in the database'
        
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
