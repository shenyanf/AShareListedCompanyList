	====================================== 2018-06-11 更新 ================================================
	new：
		1.下载深交所上市公司信息使用pandas保存为xlsx格式
		2.解决模拟jsonp回调方法失败的问题
		3.其他优化
		
		另：上交所上市公司列表可以直接下载，URL：http://www.sse.com.cn/assortment/stock/list/share/
	====================================== 2018-06-11 更新 ================================================
	
	====================================== 2017-11-23 更新 ================================================
```
深交所：首页>市场数据>交易品种>股票(xlsx)  
巨潮：巨潮资讯官网>新版公测>数据Data>选股器（csv，两市）  
这里可以直接下A股。
```
转载 CSDN用户 garbageceo 的回复~

	====================================== 2017-11-23 更新 ================================================

简介  
  这是一个会抓取所有A股上市公司信息的python工程，可以保存到mysql中。数据库中的数据可以导出到excel中。

使用方法：  
1.安装依赖组件：  
	
	1.1下载并安装pip   
		https://pypi.python.org/pypi/pip#downloads  
		setup.py install  
  
	1.2.安装openpyxl  
		pip install openpyx  


	1.3.下载并安装xlrd  
		https://pypi.python.org/pypi/xlrd  
		setup.py install 
	
	1.4.下载安装pands
		pip install pandas
		
2.执行
	主要入口在asharelistcompany.py
	
	2.1下载全部代码后，导入eclipse
  
	2.2下载深圳交易所上市公司信息,需要手动打开并另存为xlsx
		s.downloadSZSEAShares()
  
	2.3再手动打开<A股上市公司列表.xls>,再手动另存为<A股上市公司列表.xlsx>
  
	2.4 获取上交所上市公司并入库
		s.sseCompanyStore2DB()

	2.5 获取深交所上市公司并入库
		s.szseCompanyStore2DB()
    
	2.6 数据库中数据保存到xlsx中
		s.store2xlsx()

上市公司列表每月更新地址：https://my.oschina.net/sshen11111/blog/755201

觉得好了，记得给个赞哦
