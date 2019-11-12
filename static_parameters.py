import time
class Parameters(object):
    def __init__(self):
        self.cnkiUserKey = '3cf841c8-ec7f-50cb-a8f1-c7010190d461'
        self.headers_kns = {
            'Host': 'kns.cnki.net',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Sec-Fetch-Mode': 'nested-navigate',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            # 'Referer': 'https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&isinEn=1&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDB.xml&research=off&t=1571652866593&keyValue=&S=1&sorttype=(%e8%a2%ab%e5%bc%95%e9%a2%91%e6%ac%a1%2c%27INTEGER%27)+desc',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'Ecp_notFirstLogin=Ki1irP; Ecp_ClientId=2191022142301941917; RsPerPage=20; cnkiUserKey=aee81f08-74a9-dffa-ecf2-e0653b126cb7; _pk_ses=*; LID=WEEvREcwSlJHSldRa1FhdXNXaEhobnVscjNJemtOS1ZDemUxYUpJVFhMWT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; ASP.NET_SessionId=2nwpbhvkkawimm2budmq3l0d; SID_kns=123124; Ecp_session=1; SID_klogin=125142; Ecp_LoginStuts=%7B%22IsAutoLogin%22%3Afalse%2C%22UserName%22%3A%22K10054%22%2C%22ShowName%22%3A%22%25E5%258C%2597%25E4%25BA%25AC%25E9%2582%25AE%25E7%2594%25B5%25E5%25A4%25A7%25E5%25AD%25A6%22%2C%22UserType%22%3A%22bk%22%2C%22r%22%3A%22Ki1irP%22%7D; KNS_SortType=SCDB%21%28%25e8%25a2%25ab%25e5%25bc%2595%25e9%25a2%2591%25e6%25ac%25a1%252c%2527INTEGER%2527%29+desc c_m_LinID=LinID=WEEvREcwSlJHSldRa1FhdXNXaEhobnVscjNJemtOS1ZDemUxYUpJVFhMWT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=10/29/2019 11:59:48; c_m_expire=2019-10-29 11:59:48; SID_krsnew=125134;',
        }
        self.headers_acad = {
            'Host': 'acad.cnki.net',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.headers_navi ={
            'Host':'navi.cnki.net',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
        }

        self.headers_post = {
            'Host':'ishufang.cnki.net',
            'Connection':'keep-alive',
            'Content-Length':'1542',
            'Sec-Fetch-Mode':'cors',
            'Origin':'https://kns.cnki.net',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded;',
            'Accept':'*/*',
            'Sec-Fetch-Site':'same-site',
            # 'Referer':'https://kns.cnki.net/kns/brief/brief.aspx?curpage=2&RecordsPerPage=20&QueryID=5&ID=&turnpage=1&tpagemode=L&dbPrefix=CJFQ&Fields=&DisplayMode=listmode&SortType=(%e8%a2%ab%e5%bc%95%e9%a2%91%e6%ac%a1%2c%27INTEGER%27)+desc&PageName=ASP.brief_result_aspx&isinEn=1&',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
        }

        self.paramters = {
            'curpage':'2',###
            'RecordsPerPage':'20',
            'QueryID':'1',###
            'ID':'',
            'turnpage':'1',
            'tpagemode':'L',
            'dbPrefix':'CJFQ',###
            'Fields':'',
            'DisplayMode':'listmode',
            'SortType':'(被引频次,\'INTEGER\') desc',
            'PageName':'ASP.brief_result_aspx',
            'isinEn':'1',
        }

        self.static_post_data = {
            'action': '',
            'NaviCode': 'I135',#查找的类别（此处为互联网技术）
            'ua': '1.21',
            'isinEn': '1',
            'PageName': 'ASP.brief_result_aspx',
            'DbPrefix': 'CJFQ',##
            'DbCatalog': '中国学术期刊网络出版总库',
            'ConfigFile': 'CJFQ.xml',##
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',  # 搜索类别（CNKI右侧的）
            'db_value': '中国学术期刊网络出版总库',
            'year_type': 'echar',
            'his': '0',
            'db_cjfqview': '中国学术期刊网络出版总库,WWJD',
            'db_cflqview': '中国学术期刊网络出版总库',
            '__': time.asctime(time.localtime()) + ' GMT+0800 (中国标准时间)'
        }

my_parameters = Parameters()