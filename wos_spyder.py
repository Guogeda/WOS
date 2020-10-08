import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
import time
import os

from __parameters__ import *

class enter_wos():
    def  __init__(self, search_expression):
        super().__init__()
        self._init_session()
        self.sid = self._get_sid(self.request.url)
        self.jse = self._get_jessionid(self.request.headers['Set-Cookie'])

        self.search_data = search_data
        self.search_expression = search_expression
        
        self.AdvancedSearch()

    def AdvancedSearch(self):

        self.search_data['SID'] = self.sid
        self.search_data['value(input1)'] = self.search_expression
        
        adsearch_response = self.session.post(url=search_url,data=self.search_data,headers=search_header,allow_redirects=False)
        
        self.qid = self._get_qid(adsearch_response.headers['Location'])

        full_entry_url=entry_url.format(jse=self.jse,qid=self.qid,sid=self.sid)
        # print(full_entry_url)

        self.entry_response = self.session.get(url=full_entry_url,headers=search_header)
        self.entry_response.encoding = self.entry_response.apparent_encoding
        with open('entry_response.txt', 'w', encoding='utf-8') as file:
            file.write(self.entry_response.text)

    def _init_session(self):
        self.session = requests.Session()
        self.request = self.session.get(url=get_sid_url, headers=search_header)
        self.cookie = requests.utils.dict_from_cookiejar(self.request.cookies)

    def _get_sid(self, sid_str):
        sid_pattern = r'SID=(\w+)&'
        return  re.findall(sid_pattern, sid_str)[0].replace('SID=', '').replace('&', '')
        
    def _get_db(self):
        soup = BeautifulSoup(self.request.text, 'lxml')
        db_str = str(soup.find('select', attrs={'id': 'ss_showsuggestions'}).get('onchange'))
        db_pattern = r'WOS\.(\w+)'
        pattern = re.compile(db_pattern)
        result = pattern.findall(db_str)
        if result is not None:
            print('已购买的数据库为：',result)
            self.db_list = result

    def _get_qid(self, qid_str):
        qid_pattern = r'Qid=(\d+)'
        return re.findall(qid_pattern, qid_str)[0]

    def _get_jessionid(self, jsessionid_str):
        jsessionid_pattern = r'JSESSIONID=(\w+)'
        return re.findall(jsessionid_pattern, jsessionid_str)[0] 
    
class export_paper(enter_wos):

    def __init__(self, search_expression, export_start, export_end, file_name, file_type='fieldtagged', select_id=''):
        super().__init__(search_expression=search_expression)
        self.export_start = export_start
        self.export_end = export_end
        self.file_name = file_name
        self.file_type = file_type
        self.export_data = export_data
        self.select_id = select_id

    def download(self):
        soup = BeautifulSoup(self.entry_response.text, 'lxml')
        self.paper_num = int(soup.find('span', attrs={'id': 'footer_formatted_count'}).get_text().replace(',', ''))
        print('now we found {paper_num} articles'.format(paper_num = self.paper_num))

        self.export_data['selectedIds'] = self.select_id
        self.export_data['rurl'] = self.entry_response.url
        self.export_data['qid'] = str(self.qid)
        self.export_data['SID'] = str(self.sid)
        self.export_data['queryNatural'] = self.search_expression

        self.export_end = self.export_end if self.export_end < self.paper_num else self.paper_num

        span = 500
        iter_num = self.paper_num // span + 1
        start_index = self.export_start // 500 
        end_index = self.export_end // 500

        start = self.export_start

        for  i in range(iter_num):
            if start_index == i and end_index >= i:
                end = self.export_end if self.export_end < (i+1) * span else (i+1) * span
                print ('{start} to {end} start export, filetype is {filetype}'.format(
                    start = start , end = end , filetype = self.file_type
                ))
                self.export_data['mark_to'] = end
                self.export_data['mark_from'] = start
                self.export_data['markFrom'] = start
                self.export_data['markTo'] = end 
                self.export_data['save_options'] = self.file_type
                
                export_response = self.session.post(data=self.export_data,url=export_url,headers=search_header,allow_redirects=False)
                export_response.encoding = export_response.apparent_encoding

                download_url = export_response.headers['Location']
                download_response = self.session.get(url=download_url, headers = search_header)

                start_index += 1
                start = (i+1) * span + 1 

                yield download_response.text
                time.sleep(10)   # 等10s继续获取，道德

    def save(self):
        contents = self.download()
        file_name = '{}.txt'.format(self.file_name)
        with open(file_name,'w',encoding='utf-8') as f:
            for content in contents:
                f.write(content)
                f.write('\n')
        print('save ok')

class get_references(enter_wos):
    def __init__(self, search_expression, file_name, file_type='fieldtagged'):
        super().__init__(search_expression=search_expression)
        if 'no_doi.txt' in os.listdir('.'):
            os.remove('no_doi.txt') 
        self.file_name = file_name
        self.file_type = file_type
        self.export_data = export_data
        self.no_doi = []


    def get_main(self):
        # 进入论文详情页
        exact_url = paper_url.format(jse=self.jse,qid=self.qid,sid = self.sid, page=str(1), doc=str(1))
        paper_response = self.session.get(url=exact_url,headers=search_header)
        paper_soup = BeautifulSoup(paper_response.text, 'lxml')
        
        self.num = self._get_nums(paper_soup)  # 获取参考论文数量
        self.name = self._get_paper_name(paper_soup)  # 获取论文名字
        self.page = int(self.num) // 30  + 1   # 获取页面数目
        self.base_references_url = self._get_all_references_url(paper_soup)  # 获取每个页面的url
    
        self.save() # 保存

    def export(self):
        print('we need to export {num} papers'.format(num=self.num))
        print('we find paper name is {}'.format(self.name))
        
        self.export_data['SID'] = str(self.sid)
        self.export_data['queryNatural'] = '<b>从:</b>  '+self.name
        self.export_data['mark_to'] = ''
        self.export_data['mark_from'] = ''
        self.export_data['markFrom'] = ''
        self.export_data['markTo'] = '' 
        self.export_data['colName'] = 'WOS'
        self.export_data['search_mode'] = 'CitedRefList'
        self.export_data['view_name'] = 'UA-CitedRefList-summary'
        self.export_data['mode'] = 'CitedRefList-OpenOutputService'
        self.export_data['value(record_select_type)'] = 'pagerecords'
        self.export_data['sortBy'] = 'CAU.A;CW.A;CY.D;CV.D;CG.A'
        self.export_data['save_options'] = self.file_type

        for i in range(self.page):

            print('now  we export page of {}, total has {}'.format(i+1,self.page))

            #获得进入“查看引用”界面，每个页面有30个参考文献
            references_url = self.base_references_url + str(i+1)
            reference_response = self.session.get(url=references_url,headers=search_header)
            
            # 获取son_qid
            self.son_qid = self._get_son_qid(reference_response.url)
            reference_soup = BeautifulSoup(reference_response.text, 'lxml')

            self.select_id = self._filter(reference_soup, i) # 有的参考文献不会导出
            self.export_data['qid'] = str(self.son_qid)
            self.export_data['selectedIds'] = ';'.join(i for i in self.select_id)
            self.export_data['rurl'] = reference_response.url
            # 获取导出标记的url
            new_export_url = export_url 
            export_response = self.session.post(data=self.export_data,url=new_export_url,headers=search_header,allow_redirects=False)
            # 获得下载 'txt‘ 文件的下载地址
            download_url = export_response.headers['Location']
            download_response = self.session.get(url=download_url, headers = search_header)
            
            yield download_response.text

    def save(self):
        contents = self.export()
        file_name = '{}.txt'.format(self.file_name)
        with open(file_name,'w',encoding='utf-8') as f:
            for content in contents:
                f.write(content)
                f.write('\n')
        print('we found {} have no doi'.format(self.no_doi))
        print('save ok')

    def _filter(self, soup, i):
        has_doi = []
        check_boxs = soup.findAll(name='div',attrs={'class':'search-results-checkbox-align'})
        for index,check_box in  enumerate(check_boxs):
            try:
                has_doi.append(check_box.input['value'])
            except KeyError  as e:
                paper_id = str(index + 1 + 30 * i)
                self.no_doi.append(paper_id)
                self._save_no_doi(soup, index, paper_id)
        return has_doi 

    def _save_no_doi(self,soup,index,paper_id):
        data_info = soup.findAll(name='div',attrs={'class':'reference-item-non-ar'})[index]
        try:
            title, press,*page_num, year = [i.get_text() for i in data_info.findAll(name='value')]
        except ValueError as e:
            title = 'no title'
            press, *page_num, year = [i.get_text() for i in data_info.findAll(name='value')]
        try:
            author = data_info.a.get_text()
        except AttributeError as e:
            author = 'nopoeple'

        with open('no_doi.txt', 'a') as f:
            f.write('{paper_id},{title},{author},{press},{year}'.format(
               paper_id = paper_id, title = title, author = author, press = press, year = year
            ))
            f.write('\n')

    def _get_son_qid(self,son_qid_str):
        son_qid_pattern = r'qid=(\d+)'
        return re.findall(son_qid_pattern, son_qid_str)[0]

    def _get_paper_name(self, soup):
        name = soup.find(name='div',attrs={'class':'title'}).value.get_text()
        return name

    def _get_nums(self, soup):
        num_str = soup.find(name='div',attrs={'class':'cited-ref-separator'}).h2.get_text()
        num_pattern = r'\d+'
        return re.findall(num_pattern, num_str)[0]

    def _get_all_references_url(self, soup):
        url_str = soup.find(name='div',attrs={'class':'cited-ref-separator'}).a['href']
        # return base_url + url_str[:10] + ';jsessionid={}'.format(self.jse) + url_str[10:-1]
        return base_url + url_str[:-1]


if __name__ == "__main__":
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


    aim = 'TS=LNOI AND PY=2020 AND DO=10.1515/nanoph-2020-0013'
    file_name = 'LNOI'
    file_type = 'fieldtagged'
    aim_paper = get_references(search_expression=aim, file_name=file_name, file_type=file_type)
    aim_paper.get_main()

    # 导出 参考文献 txt
    # test = 'TS=LN AND PY=(2018-2020)' # 检索式一定要有两个条件以上 
    # test_start = 1
    # test_end = 501
    # file_type = 'fieldtagged'
    # demo = export_paper(search_expression=test, export_start=test_start, 
    #                     export_end= test_end,file_name='LNOI',file_type=file_type)
    # demo.save()


    


    
