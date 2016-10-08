简介  
  这是一个会抓取所有A股上市公司信息的python工程。

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
  2.1下载全部代码后，导入eclipse
  2.2先执行downloadSZSEAShares()
  2.3再手动打开<A股上市公司列表。xls>,再手动另存为<A股上市公司列表.xlsx>
  2.4然后执行appendSSEStocks()
