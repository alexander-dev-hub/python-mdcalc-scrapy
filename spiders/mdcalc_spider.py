from scrapy.spiders import Spider

from scrapy.selector import Selector
from scrapy.http import Request
import requests
from mdcalc_scrapy.items import  ArticleItem
import re
import codecs
import json
import pprint
import logging
from clint.textui import colored
from scrapy.utils.log import configure_logging
from mdcalc_scrapy.common import Common
from bs4 import BeautifulSoup as bs


class MdcalcSpider(Spider):
    name = "mdcalc_scrapy"
    allowed_domains = ["mdcalc.com"]
    
    logfile='mdcalc_scrapty.log'
   
    BASE_URL="https://www.mdcalc.com"

    user_agent=''
    #####################################################
    def __init__(self, *args, **kwargs):
        
        #Common.init_log(self.logfile)
        
           
        super().__init__(*args, **kwargs)
    #####################################################
    def start_requests(self):
        self.user_agent = Common.get_random_useraget()
        
        init_url = '%s#all' % (self.BASE_URL)
        yield Request(init_url, callback=self.parse , headers={"User-Agent": self.user_agent})
    #####################################################         
    def parse(self, response):
        
        arts = response.css('a.index_all_calcItem::attr(href)').extract()
        
        for art in arts:
            
            docid= art[1:]
           
            #if not Common.exist_in_json(docid):
            yield response.follow(art, callback=self.parse_article, meta={'docid': docid }) 

    #####################################################
    def extract_info_tag(self, tag, info_list_divs):
        info_list=[]
        if info_list_divs:
            for info_list_div in info_list_divs:
                parent_div_class= info_list_div.xpath(".//parent::div/@class").extract_first()
                if parent_div_class and 'btn' in parent_div_class:
                    continue
                
                info_list_lis =info_list_div.css("ul li").extract()
                for info_list_li in info_list_lis: 
                    li_pp_str =bs(info_list_li,"lxml")
                    info_list.append(li_pp_str.text.strip())
                if not info_list_lis:
                    info_list_ps= info_list_div.css("p").extract()
                    for info_list_p in info_list_ps: 
                        li_pp_str =bs(info_list_p,"lxml")
                        info_list.append(li_pp_str.text.strip())
                
        return info_list
    #####################################################
    def extract_next_dic_tag(self, tag, info_list_divs):
        info_list={}
        if info_list_divs:
            for info_list_div in info_list_divs:
                parent_div_class= info_list_div.xpath(".//parent::div/@class").extract_first()
                if parent_div_class and 'btn' in parent_div_class:
                    continue
                
                info_list_in_divs =info_list_div.xpath("div") 
                for info_list_in_div in info_list_in_divs:
                    # Advice
                    head2= info_list_in_div.css('h2::text').extract_first()
                    divs = info_list_in_div.xpath('div')
                    # first paragraps
                    nextparas=[]
                    for div in divs:
                        paras = div.css('p').extract()
                        if paras:
                            for para in paras: 
                                nextparas.append(bs(para,"lxml").text.strip())
                        paras = div.css('ul li').extract()
                        if paras:
                            for para in paras: 
                                nextparas.append(bs(para,"lxml").text.strip())
                    if  nextparas:               
                        info_list[head2] = nextparas
                
        return info_list    
    #####################################################
    def extract_evidence_dic_tag(self, tag, info_list_divs):
        info_list={}
        if info_list_divs:
            for info_list_div in info_list_divs:
                parent_div_class= info_list_div.xpath(".//parent::div/@class").extract_first()
                if parent_div_class and 'btn' in parent_div_class:
                    continue

                for sub_info_div in info_list_div.xpath('div'):

                    info_head = sub_info_div.css('h2::text').extract_first()
                    if 'Literature' in info_head:
                        break
                    subinfodiv = sub_info_div.xpath('div').extract()
                    subinfohtm= subinfodiv[0]
                    subinfo_str= bs(subinfohtm,"lxml").text.strip()
                    info_list[info_head]=subinfo_str
                
                '''
                #Fact & Figures
                #fact_firs={}
                sub_info_div = info_list_div.xpath("div[h2[contains(.,'Figures')]]") 
                if sub_info_div:
                    info_head = sub_info_div.css('h2::text').extract_first()
                    subinfodiv = sub_info_div.xpath('div').extract()
                    subinfohtm= subinfodiv[0]
                    subinfo_str= bs(subinfohtm,"lxml").text
                    info_list[info_head]=subinfo_str

                '''
                # Literature
                info_lite_div = info_list_div.xpath("div[h2[contains(.,'Literature')]]") 

                if not info_lite_div:
                    continue

                
                subinfos={}
                lit_head= info_lite_div.css('h2::text').extract_first()
                litedivs = info_lite_div.xpath('div')
                for litediv in litedivs:
                    links=[]
                    lit_head2= litediv.css('h3::text').extract_first()
                    alinks = litediv.css('a.resource')
                    for alink in alinks:
                        href= alink.xpath('@href').extract_first()
                        desc=alink.xpath('@data-reactid').extract_first()
                        spos=desc.rfind(":$")
                        desc= desc[spos+2:].replace('=',':')
                        links.append({'url':href, 'desc':desc.strip()})
                    subinfos[lit_head2]=links
                info_list[lit_head]=subinfos

        return info_list  
     
    #####################################################
    def extract_creator_dic_tag(self, tag, info_list_divs):
        info_list=[]
        if info_list_divs:
            for info_list_div in info_list_divs:
                parent_div_class= info_list_div.xpath(".//parent::div/@class").extract_first()
                if parent_div_class and 'btn' in parent_div_class:
                    continue
                
                info_list_in_divs =info_list_div.xpath("div") 
                for next_div in info_list_in_divs:
                    # name, img
                    faceimg= next_div.css('div.resource--author img::attr(src)').extract_first()
                    if not faceimg: faceimg=''
                    authorname = next_div.css('div.resource--author div.resource__text strong::text').extract_first()

                    # info
                    authordesc = next_div.css('div:nth-child(2) > div p::text').extract_first()
                    if not  authordesc: authordesc=''
                    infosrc = next_div.css('div:nth-child(2) p  a::attr(href)').extract_first()
                    if not infosrc: infosrc=''
                    info_list.append({'authorname':authorname, 'faceimg':faceimg, 'authordesc':authordesc, 'infosrc':infosrc })
               
        return info_list
    
    
    #####################################################
    def extract_refs_list_tag(self, tag, info_list_divs):
        info_list=[]
        if info_list_divs:
            lis = info_list_divs[0].xpath('.//li')
            for next_div in lis:
                # ref info
                link= next_div.css('a::attr(href)').extract_first()
                if not link: url=''
                else: url = self.BASE_URL+ link
                docid = next_div.css('a::text').extract_first()
                if not  docid: docid=''
                
                info_list.append({'docid':docid, 'url':url})
                    
               
        return info_list    
    #####################################################
    def parse_article(self, response):

        item =  ArticleItem() 
        docid=response.meta['docid']
        item['docid'] =docid
        item['db']='mdcalc'
        item['url'] =response.url

        item['calc_title']=  response.css('div.calc__header h1.calc__title span::text').extract_first()

        calc_desc = response.css('div.calc__desc::text').extract_first()    
        if not calc_desc:
            calc_desc = response.css('div.calc__desc span::text').extract_first()
        if calc_desc:
            item['calc_desc']=calc_desc
            
        use_cases_divs = response.css("div[data-content='use-cases']")
        use_cases =self.extract_info_tag('use-cases',use_cases_divs )
        item['use_cases']=use_cases
            
        pearls_pitfalls_divs= response.css("div[data-content='pearls-pitfalls']")
        pearls_pitfalls=self.extract_info_tag('pearls-pitfalls',pearls_pitfalls_divs )
        
        item['pearls_pitfalls']=pearls_pitfalls
        #json.dumps
    
        why_use_divs= response.css("div[data-content='why-use']")
        why_use=self.extract_info_tag('why-use',why_use_divs )
        item['why_use']= why_use
       
        next_steps_divs= response.css("div[data-content='next-steps']")
        nextsteps=self.extract_next_dic_tag('next-steps',next_steps_divs )
        item['nextsteps'] =  nextsteps
        
        evidence_divs= response.css("div[data-content='evidence']")
        evidence=self.extract_evidence_dic_tag ('evidence',evidence_divs )
        item['evidence'] =  evidence

        creator_insights_divs= response.css("div[data-content='creator-insights']")
        creator_insights= self.extract_creator_dic_tag('creator-insights', creator_insights_divs)
        item['creators'] =  creator_insights

        refs_divs= response.xpath("//dt[contains(.,'Related Calcs')]/../dd")
        refs= self.extract_refs_list_tag('creator-insights', refs_divs)
        item['refs'] =  refs

        pprint.pprint(item)
        yield  item
