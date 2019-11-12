from bs4 import BeautifulSoup
import math,random,time
import re,os
import requests
from static_parameters import my_parameters
import json
from pro import *
#设立缓存，如果已经有期刊信息，则直接将影响因子复制即可
try:
    with open('Journal_Point.json','r') as f:
        Journal_Point = json.load(f)
except:
    Journal_Point = {}

GET_ARTICAL_DETAIL_URL = 'https://kns.cnki.net/KCMS/detail/detail.aspx?'


class GetPageInfo(object):
    def __init__(self):
        self.all_info = []
        self.count = 0  #用于递归计数
        

    def get_Impact_Factor(self,href):
        '''利用重定向获取页面'''
        bad_response = '<script>window.location.href=\'//www.cnki.net\'</script>'
        # time.sleep(0.3)
        source_url = 'https://kns.cnki.net' + href
        source = requests.get(source_url,stream=True)
        source_text = source.text
        print(source_text==bad_response)
        if source_text==bad_response:
            return self.get_Impact_Factor(href)
        partten_get_fuhe = re.compile(r'复合影响因子：.*?(\d\.\d+).*?')
        partten_get_zonghe = re.compile(r'综合影响因子：.*?(\d\.\d+).*?')
        #如果该期刊有影响因子，则找出它，如果没有，则返回空，类型均为str
        try:
            fuhe_impact_factor = re.search(partten_get_fuhe, source_text).group(1)
            zonghe_impact_factor = re.search(partten_get_zonghe, source_text).group(1)
            return str(fuhe_impact_factor), str(zonghe_impact_factor)
        except:
            return '',''


    def get_Impact_Factor2(self,parameters):
        '''获取到被访问页面的关键参数，直接请求该页面'''
        self.count += 1
        if self.count >20:
            self.count = 0
            print('无法请求到相应页面，请稍后或者更换网络再试。')
            return
        bad_response = '<script>window.location.href=\'//www.cnki.net\'</script>'
        # time.sleep(0.3)
        source_url = 'http://navi.cnki.net/KNavi/JournalDetail?'
        source = requests.get(source_url,headers=my_parameters.headers_navi,params=parameters)
        source_text = source.text
        if source_text==bad_response:
            return self.get_Impact_Factor2(parameters)
        partten_get_fuhe = re.compile(r'复合影响因子：.*?(\d\.\d+).*?')
        partten_get_zonghe = re.compile(r'综合影响因子：.*?(\d\.\d+).*?')
        #如果该期刊有影响因子，则找出它，如果没有，则返回空，类型均为str
        try:
            fuhe_impact_factor = re.search(partten_get_fuhe, source_text).group(1)
            zonghe_impact_factor = re.search(partten_get_zonghe, source_text).group(1)
            self.count = 0
            return str(fuhe_impact_factor), str(zonghe_impact_factor)
        except:
            self.count = 0
            return '',''



    def find_ajax(self,url,parameters):
        # time.sleep(0.1)
        #根据url和参数获取相应页面的信息
        info = []
        try:
            ajax_list_page = requests.get(url, params=parameters, headers=my_parameters.headers_kns)
            soup = BeautifulSoup(ajax_list_page.text, 'lxml')
            ajax_list = soup.find('div', attrs={'class': 'ebBd'}).find_all('li')
            for item in ajax_list:
                href = 'https://kns.cnki.net' + item.find('a')['href']
                text = item.text.strip(' \n\r')
                text = re.sub(r'(&nbsp&nbsp)','', text)
                text = re.sub(r'[\n\r\s]+', '', text)
                info.append(text)
                info.append(href)
        except:
            pass
        return info


    def get_artical_detail(self,artical_href,dict_artcical):
        # time.sleep(0.1)
        #获取文章详细内容的url，发现和href中的三个关键参数有关
        parameters = {
            'DbCode':'',
            'DbName':'',
            'FileName':'',
        }
        pattern_DbCode = re.compile(r'.*?[dD]b[cC]ode=\s?(.*?)&')
        pattern_DbName = re.compile(r'.*?[dD]b[nN]ame=\s?(.*?)&')
        pattern_FileName = re.compile(r'.*?[fF]ile[nN]ame=\s?(.*?)&')
        parameters['DbCode'] = re.search(pattern_DbCode,artical_href).group(1)
        parameters['DbName'] = re.search(pattern_DbName,artical_href).group(1)
        parameters['FileName'] = re.search(pattern_FileName,artical_href).group(1)
        print('FileName=' + parameters['FileName'])
        req = requests.get(GET_ARTICAL_DETAIL_URL,params=parameters,headers=my_parameters.headers_kns)
        #请求到文章详细内容的页面后，获取文章关键词
        soup = BeautifulSoup(req.text, 'lxml')
        keyword = []
        try:
            keyword_list = soup.find('label', attrs={'id': 'catalog_KEYWORD'}).parent.find_all('a')
            for item in keyword_list:
                keyword.append(item.text.strip(';\r\n\t '))
        except:
            pass
        #将获取的关键词保存为列表，插入到每个文章的信息中
        dict_artcical['关键词'] = keyword

        #查找摘要
        try:
            summary = soup.find('span',attrs={'id':'ChDivSummary'}).text
        except:
            summary="kong"
        dict_artcical['摘要'] = summary

        #查找相似文献
        parameters.update({
            'curdbcode': 'CJFQ',
            'reftype': '604',
            'catalogId': 'lcatalog_func604',
            'catalogName': '相似文献',
        })

        ajax_url = 'https://kns.cnki.net/kcms/detail/frame/asynlist.aspx?'
        dict_artcical['相似文献'] = self.find_ajax(ajax_url,parameters)
        #查找读者推荐
        parameters.update({
            'curdbcode': 'CJFQ',
            'reftype': '605',
            'catalogId': 'lcatalog_func605',
            'catalogName': '读者推荐',
        })
        dict_artcical['读者推荐'] = self.find_ajax(ajax_url, parameters)

        #获取复合影响因子、获取综合影响因子
        parameters_fators = {
            'pcode':'',
            'pykm':'',
        }
        infomation = soup.select('.sourinfo .title a')
        pattern = re.compile(r'.*?\(\'(.*?)\',\'(.*?)\',\'(.*?)\',\'(.*?)\'\);')
        parameters_fators['pcode'] = pattern.search(str(infomation)).group(2)
        parameters_fators['pykm'] = pattern.search(str(infomation)).group(4)
        if parameters_fators['pykm'] in Journal_Point.keys():
            dict_artcical['复合影响因子'], dict_artcical['综合影响因子'] = Journal_Point[parameters_fators['pykm']][0:2]
        else:
            try:
                dict_artcical['复合影响因子'], dict_artcical['综合影响因子'] = self.get_Impact_Factor2(parameters_fators)
            except:
                dict_artcical['复合影响因子'], dict_artcical['综合影响因子'] = 0,0
                print("没找到")

            #将期刊的代号插入到字典中
            if(dict_artcical['复合影响因子'], dict_artcical['综合影响因子'] != 0,0):
                Journal_Point[parameters_fators['pykm']] = [dict_artcical['复合影响因子'], dict_artcical['综合影响因子']]

    def get_Detail_Info(self,text,session):
        # time.sleep(0.1)
        '''
        从每个文章列表中提取出文章的相关信息
        '''
        soup = BeautifulSoup(text,'lxml')
        #将每个文章列表中的信息装在一个列表中
        dict_pre_page = []
        artical_list = soup.find('table',attrs={'class':'GridTableContent'}).find_all('tr')
        for i in range (1,len(artical_list)):#artical_list[0]是表头
            print('正在获取第' + str(i) + '条信息，',end='')
            dict_artcical = {'题名':'',
                             '作者':'',
                             '来源': '',
                             '发表时间': '',
                             '被引量': '',
                             '下载量': '',
                             '复合影响因子': '',
                             '综合影响因子': '',

            }
            # 获取题名
            dict_artcical['题名'] = artical_list[i].find('a',attrs={'class':'fz14'}).text
            artical_href = artical_list[i].find('a',attrs={'class':'fz14'})['href']
            self.get_artical_detail(artical_href,dict_artcical)
            # 获取作者
            dict_artcical['作者'] = artical_list[i].find('td',attrs={'class':'author_flag'}).text.strip('\n')#用strip函数去除字符串首尾的非法字符
            # 获取来源
            dict_artcical['来源'] = artical_list[i].find_all('a',attrs={'target':'_blank'})[1].text
            #获取复合影响因子、获取综合影响因子 !!!!!!此方法没有添加缓存
            # href = artical_list[i].find_all('a',attrs={'target':'_blank'})[1]['href']
            # dict_artcical['复合影响因子'],dict_artcical['综合影响因子'] = self.get_Impact_Factor(href)
            # 获取发表时间
            dict_artcical['发表时间'] = artical_list[i].find('td',attrs={'align':'center'}).text.strip('\r\n ')
            # 获取被引量
            try:
                dict_artcical['被引量'] = artical_list[i].find('td',attrs={'align':'right'}).text.strip('\n ')
            except:
                dict_artcical['被引量'] = '0'
            # 获取下载量
            try:
                dict_artcical['下载量'] = artical_list[i].find('span',attrs={'class':'downloadCount'}).text
            except:
                dict_artcical['下载量'] = '0'

            dict_pre_page.append(dict_artcical)

        #更新缓存表
        with open('Journal_Point.json', 'w') as f:
            json.dump(Journal_Point,f)

        #返回每一页信息的列表
        return dict_pre_page




get_page_info = GetPageInfo()
if __name__ == '__main__':
    pass