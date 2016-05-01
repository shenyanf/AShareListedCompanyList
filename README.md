简介
  这是一个会抓取所有上交所上市公司信息的python工程。你问我深交所上市公司信息列表，我只能告诉你代码中有一个方法是下载深交所上市公司列表的。

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
2.执行
  下载全部代码后，导入eclipse，设置syf.ashareslistedcompanieslist.py storeASharesListedCompanies2XLS参数lastStockNumber为最后一个上市公司的代码（目前最大的上市公司代码为603999），执行 syf.store2xls就会在默认路径（D盘）下生成《上证所A股上市公司列表.xlsx》
