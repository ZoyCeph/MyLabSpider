# -*- coding:utf-8 -*-

import scrapy
import re

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from MyLabSpider.items import BlogItem

def extract_data(pattern,datas):
    tmp=[]
    for data in datas:
        if re.search(pattern,data):
            data=re.sub(pattern,'',data)
            tmp.append(data)
    return(tmp)
    
def combine_url(prefix,url):
    return(prefix+url)

def extract_match(pattern,string):
    if re.search(pattern,string):
        return(re.search(pattern,string).group(0))     
    
class Myspider(CrawlSpider):
    name='homepage'
    allowed_domains=['weibo.cn','weibo.com','sina.com.cn']
    custom_settings = {
    'ITEM_PIPELINES':{'HomepageMongoPipeline': 300},
    }    
    
    def start_requests(self):
        start_url='https://weibo.cn'#/u/2308595135'
        cookie={
            '_T_WM':'836480f3c78ad70cac3ec62de233e2b5',
            'SCF':'AqmhC43QH0rxkNEoSLDKLDCA1W3i7ul_Ou7lmeepjtZdVZpkp1DDO_pplxkA6UrlOxTbkb6SHItyxc8sYxTBwtc.',
            'SUB':'_2A252W2QMDeRhGeBP61YU8C3OyT6IHXVVpAxErDV6PUJbktANLVnkkW1NRZcCslT3KPrS2cAoYsezLNMPUzTb70B2',
            'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFgKdD2UJ-MHF38PqLFprfH5JpX5K-hUgL.FoqpehBfeheEeoz2dJLoIEXLxKnL122L1-BLxK-LBKeLB-zLxKML1hBL1KMLxKnL1h5L1h2LxK.LB.eLBK5t',
            'SUHB':'0wn1QHwt00cJH7'}
        headers={
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
        yield Request(url=start_url,callback=self.parse,headers=headers,cookies=cookie)
        
    def parse(self,response):
        cookie={
            '_T_WM':'836480f3c78ad70cac3ec62de233e2b5',
            'SCF':'AqmhC43QH0rxkNEoSLDKLDCA1W3i7ul_Ou7lmeepjtZdVZpkp1DDO_pplxkA6UrlOxTbkb6SHItyxc8sYxTBwtc.',
            'SUB':'_2A252W2QMDeRhGeBP61YU8C3OyT6IHXVVpAxErDV6PUJbktANLVnkkW1NRZcCslT3KPrS2cAoYsezLNMPUzTb70B2',
            'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFgKdD2UJ-MHF38PqLFprfH5JpX5K-hUgL.FoqpehBfeheEeoz2dJLoIEXLxKnL122L1-BLxK-LBKeLB-zLxKML1hBL1KMLxKnL1h5L1h2LxK.LB.eLBK5t',
            'SUHB':'0wn1QHwt00cJH7'}
        headers={
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
        url_prefix='https://weibo.cn'
        sina=Selector(response)
        item=BlogItem()
        for data in response.xpath('//div[@class="c"]'):
            author=data.xpath('.//a[@class="nk"]/text()').extract()
            source=data.xpath('.//span[@class="ct"]/text()').extract()
            content=data.xpath('.//span[@class="ctt"]').extract()
            status=data.xpath('.//a/text()').extract()
            if (len(author) is not 0) and (len(status) is not 0):
                content=extract_data('<[^>]+>',content)
                content="".join(content)
                for element in status:
                    if re.search('^赞',element):
                        like=extract_match('[0-9]+',element)
                    elif re.search('^转发',element):
                        transfer=extract_match('[0-9]+',element)
                    elif re.search('^评论',element):
                        comment=extract_match('[0-9]+',element)            
                item['author']=author[0]
                item['source']=source[0]
                item['content']=content            
                item['like']=like
                item['transfer']=transfer
                item['comment']=comment
                yield item
        next_url=sina.xpath('//div[@id="pagelist"]/form/div/a/@href').extract_first()
        if next_url is not '':
            print('next_url is detected:'+next_url)
            if re.search('http.+',next_url):
                pass
            else:
                next_url=combine_url(url_prefix,next_url)   
                print('next_url is fixed:'+next_url)
            yield Request(url=next_url,callback=self.parse,headers=headers,cookies=cookie)



        