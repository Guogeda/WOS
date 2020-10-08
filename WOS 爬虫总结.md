## WOS 爬虫总结

### 目的

* 快速获得文献背景：出版年份，被引频次，作者，DOI，文献类型，引用的参考文献
* 获得参考文献的下载链接，实现文献的批量化下载

### 条件

* 所处机构或者学校**购买WOS的数据库**，并且将爬虫**置于校园网环境中**。
* 如果要实现后期的文献下载需要**购买**所需文献的**数据库**。
* 后期有时间会完善用账号密码校外访问数据库。

### 使用方法

##### 1. 所需要安装的python3+包

```py
pip install requests
pip install lxml
pip install bs4
```

##### 2. 测试例子(没有将程序打包，所以需要将程序下载使用)

* 导出所有的检索结果

  ```python
  test = 'TS=LN AND PY=(2018-2020)' # 检索式一定要有两个条件以上 
  test_start = 1  # 导出起始页码
  test_end = 501  # 导出终止页码
  file_name='LNOI' # 保存文件的名称，默认为 .txt 文件，如果想要保存其他格式，那是不可能的！
  file_type = 'fieldtagged'
  demo = export_paper(search_expression=test, export_start=test_start, 
                           export_end= test_end,file_name='LNOI',file_type=file_type)
  demo.save()
  ```

* 导出所有的参考文献

  ```python
  # 运行结束会生成两个txt文件，一个是'file_name.txt'为所选需要的文献，一个是'no_doi.txt' 用于存储没有DOI的文献信息
  aim = 'TS=LNOI AND PY=2020 AND DO=10.1515/nanoph-2020-0013' # 建议用DOI搜索，这样保证搜索结果的唯一性
  file_name = 'LNOI'
  aim_paper = get_references(search_expression=aim, file_name=file_name)
  aim_paper.get_main() # 接口和上一个有点不一样，两个爬取逻辑有点小差异
  ```

* WOS 检索式参考 

  ```python
  # ''' 高级检索参考 ：
  # 布尔运算符: AND、OR、NOT、SAME、NEAR
  # 字段标识:
  #         TS= 主题
  #         TI= 标题
  #         AU= 作者 [索引]
  #         AI= 作者识别号
  #         GP= 团体作者 [索引]
  #         ED= 编者
  #         AB= 摘要
  #         AK= 作者关键词
  #         KP= Keyword Plus ®
  #         SO= 出版物名称 [索引]
  #         DO= DOI
  #         PY= 出版年
  #         AD= 地址
  #         SU= 研究方向
  #         IS= ISSN/ISBN
  # '''
  ```

### 爬虫细节分享

#### 参考资料 

* 主要参考[博主](https://blog.csdn.net/tomleung1996/article/details/86627443)的思路,博主的代码[仓库地址](https://github.com/tomleung1996/wos_crawler)

#### 需要的关于爬虫的基础知识

* [爬虫原理与cookies，session](https://blog.csdn.net/hfutzhouyonghang/article/details/81009760)
* python [Requests 基础使用](https://blog.csdn.net/shanzhizi/article/details/50903748)
* [关于异步加载和异步传输的概念](https://blog.csdn.net/liaoningxinmin/article/details/80794774)
* [爬虫问题的重定向302错误](https://blog.csdn.net/xc_zhou/article/details/80952208)
* [BeautifulSoup 模块使用指南](https://www.jianshu.com/p/2b783f7914c6)
* [python 正则 re 表达式](https://www.cnblogs.com/CYHISTW/p/11363209.html)



#### 操作爬虫时的好用的工具

* [在线解析工具](https://www.sojson.com/jshtml.html)
* 新建txt文档

#### 爬取逻辑
* 参考总结pdf文件，git放图好累


### 遇到的奇葩问题总结

1. 使用`print(response.text())`发现控制台(我的IDE为VSCODE)的显示内容与在网页端的查看源代码显示不同，可能是VSCODE后台省略了，可以保存为 txt 文件或者用bs4解码，看看是否已经获取到了想要的界面。
2. 获取到的源码，没有中文，中文显示都是`...`这个问题我百度了好久，都没有解决，后来脑子一抽，修改了一下`headers`的`'Accept-Language': 'zh-CN,zh;q=0.9',`居然就成功了， 我很开心，哈哈哈！
3. 在获取所有的参考文献的时候出了点一点意外，无法成功导出文献，原因是提交的 `form_data` 出问题了，需要仔细检查！
