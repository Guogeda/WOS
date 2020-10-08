import time 


get_sid_url = 'http://www.webofknowledge.com/'

search_url = 'http://apps.webofknowledge.com/UA_AdvancedSearch.do'

search_url_redict = 'http://apps.webofknowledge.com/UA_AdvancedSearch_input.do;jsessionid={jse}?product=UA&search_mode=AdvancedSearch&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&SID={sid}&errorQid={qid}'

entry_url = 'http://apps.webofknowledge.com/summary.do;jsessionid={jse}?product=UA&doc=1&qid={qid}&SID={sid}&search_mode=AdvancedSearch&update_back2search_link_param=yes'

search_header= {
    'Origin': 'https://apps.webofknowledge.com',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-insecure-requests': str(1),
    # 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68',
    'Content-Type': 'application/x-www-form-urlencoded',
}

search_data = {
    'action': 'search',
    'product': 'UA',
    'search_mode': 'AdvancedSearch',
    'input_invalid_notice': r'检索错误: 请输入检索词。',
    'input_invalid_notice_limits':r' <br/>注意: 滚动框中显示的字段必须至少与一个其他检索字段相组配。',
    'SID':None,
    'formUpdated': 'true',
    'replaceSetId':'',
    'goToPageLoc':'SearchHistoryTableBanner',
    'value(input1)': None,
    "value(searchOp)": "search",
    'limitStatus': 'collapsed',
    'ss_lemmatization': 'On',
    'ss_spellchecking': 'Suggest',
    'SinceLastVisit_UTC': '',
    'SinceLastVisit_DATE': '',
    'period': 'Range Selection',
    'range': 'ALL',
    'startYear': '1900',
    'endYear': time.strftime('%Y'),
    # 'editions': ['CCR', 'SCI', 'ISTP', 'IC'],
    'editions':['WOS.CCR','WOS.SCI','WOS.ISTP','WOS.IC','CSCD.CSCD','CCC.CCCB','CCC.CCCA','CCC.CCCY','CCC.CCCT','CCC.CCCBC','CCC.CCCS','CCC.CCCEC','CCC.CCCP','CCC.CCCC','DIIDW.EDerwent','DIIDW.MDerwent','DIIDW.CDerwent','KJD.KJD','MEDLINE.MEDLINE','RSCI.RSCI','SCIELO.SCIELO'],
    'collections':['MEDLINE','SCIELO','WOS','CSCD','CCC','KJD','RSCI','SCIELO'],
    'update_back2search_link_param': 'yes',
    'ssStatus': 'display:none',
    'ss_showsuggestions': 'ON',
    'ss_query_language': 'auto',
    'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
}


export_url = 'http://apps.webofknowledge.com//OutboundService.do?action=go&&'

export_data = {
    "selectedIds": None,  # 选择指定页面下载
    "displayCitedRefs": "true",
    "displayTimesCited": "true",
    "displayUsageInfo": "true",
    "viewType": "summary",
    "product": "UA",
    "rurl": None,
    "mark_id": "UDB",
    "search_mode": "AdvancedSearch", # 
    "locale": "zh_CN",
    "view_name": "UA-summary", # 
    "sortBy": "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A",
    "mode": "OpenOutputService", # 
    "qid": None,
    "SID": None,
    "format": "saveToFile",
    "filters": "AUTHORSIDENTIFIERS ISSN_ISBN CITTIMES ABSTRACT SOURCE TITLE AUTHORS",
    "mark_to": None,
    "mark_from": None,
    "queryNatural": None,
    "count_new_items_marked": "0",
    "use_two_ets": "false",
    "IncitesEntitled": "no",
    "value(record_select_type)": "range", #
    "markFrom": None,
    "markTo": None,
    "fields_selection": "AUTHORSIDENTIFIERS ISSN_ISBN CITTIMES ABSTRACT SOURCE TITLE AUTHORS",
    "save_options": None,
}

paper_url = 'http://apps.webofknowledge.com/full_record.do;jsessionid={jse}?product=UA&search_mode=AdvancedSearch&qid={qid}&SID={sid}&page={page}&doc={doc}'

reference_url ='http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=CitedRefList&parentQid={parent_qid}&parentDoc={doc}&qid={qid}&SID={SID}&colName=WOS&page={page}'

base_url = 'http://apps.webofknowledge.com/'