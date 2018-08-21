# -*- coding: utf-8 -*-
import re
import pymongo

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
#from scrapy.selector import Selector
from MyLabSpider.items import CommentItem

global collection_name

def extract_match(pattern,string):#return every matched element of input string
    if re.search(pattern,string):
        return(re.search(pattern,string).group(0))
        
        
class MySpider(CrawlSpider):
    name='comment'
    allowed_domains=['weibo.cn','weibo.com','sina.com.cn']
    custom_settings = {
    'ITEM_PIPELINES':{'MyLabSpider.pipelines.CommentMongoPipeline': 300},
    }
    
#    cookie={
#    '_T_WM':'836480f3c78ad70cac3ec62de233e2b5',
#    'SCF':'AqmhC43QH0rxkNEoSLDKLDCA1W3i7ul_Ou7lmeepjtZdVZpkp1DDO_pplxkA6UrlOxTbkb6SHItyxc8sYxTBwtc.',
#    'SUB':'_2A252W2QMDeRhGeBP61YU8C3OyT6IHXVVpAxErDV6PUJbktANLVnkkW1NRZcCslT3KPrS2cAoYsezLNMPUzTb70B2',
#    'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFgKdD2UJ-MHF38PqLFprfH5JpX5K-hUgL.FoqpehBfeheEeoz2dJLoIEXLxKnL122L1-BLxK-LBKeLB-zLxKML1hBL1KMLxKnL1h5L1h2LxK.LB.eLBK5t',
#    'SUHB':'0wn1QHwt00cJH7'}
    
    def start_requests(self):
        client = pymongo.MongoClient('localhost',27017)
        db_name = 'Sina'
        db = client[db_name]
        collection_set01 = db['UrlsQueue']
        datas=list(collection_set01.find({},{'_id':0,'url':1,'status':1}))
        for data in datas:
            if data.get('status') == 'pending':
                url=data.get('url')
                pattern='(?<=/)([0-9a-zA-Z]{9})(?=\?)'
                if re.search(pattern,url):
                    collection_name=re.search(pattern,url).group(0)
                start_url='https://weibo.cn/comment/'+collection_name+'?ckAll=1'
                collection_set01.update({'url':url},{'$set':{'status':'proccessing'}})                
                break
            else:
                pass
        client.close()
#        start_url='https://weibo.cn/comment/GtFG1pgEZ?ckAll=1'
        cookie={
            '_T_WM':'836480f3c78ad70cac3ec62de233e2b5',
            'SCF':'AqmhC43QH0rxkNEoSLDKLDCA1W3i7ul_Ou7lmeepjtZdVZpkp1DDO_pplxkA6UrlOxTbkb6SHItyxc8sYxTBwtc.',
            'SUB':'_2A252W2QMDeRhGeBP61YU8C3OyT6IHXVVpAxErDV6PUJbktANLVnkkW1NRZcCslT3KPrS2cAoYsezLNMPUzTb70B2',
            'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFgKdD2UJ-MHF38PqLFprfH5JpX5K-hUgL.FoqpehBfeheEeoz2dJLoIEXLxKnL122L1-BLxK-LBKeLB-zLxKML1hBL1KMLxKnL1h5L1h2LxK.LB.eLBK5t',
            'SUHB':'0wn1QHwt00cJH7'}
#        headers={
#            'Connection':'keep-alive',
#            'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
        yield Request(url=start_url,callback=self.parse, cookies=cookie, meta={'collection_name':collection_name})

    def parse(self,response):
#        headers={
#            'Connection':'keep-alive',
#            'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
#        sina=Selector(response)
        item=CommentItem()
        author=[]
        reply=[]
        content=[]
        like=[]
        source=[]
        tmp=[]#append parsed 'like' data
        collection_name=response.meta['collection_name']
        for data in response.xpath('//div[contains(@id,"C_")]'):
            author.append(data.xpath('./a/text()').extract_first())
            reply.append(data.xpath('./span[@class="ctt"]/a/text()').extract_first())
            content.append(data.xpath('./span[@class="ctt"]//text()').extract())
            like.append(data.xpath('./span[@class="cc"]//text()').extract())
            source.append(data.xpath('./span[@class="ct"]//text()').extract_first())
        content=[''.join(data) for data in content]
        for data in like:
            for element in data:
                if re.search('^赞',element):
                    tmp.append(extract_match('[0-9]+',element))
        for i in range(0,len(author)):
            item['author']=author[i]
            item['reply']=reply[i]
            item['content']=content[i]
            item['like']=tmp[i]
            item['source']=source[i]
            item['collection_name']=collection_name
            yield item
        