# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import codecs
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings
from mdcalc_scrapy.items import   ArticleItem
from mdcalc_scrapy.common import Common
import pymysql
import re
import os


class ScrapyMysqlPipeline(object):
    def getConnection(self):
        
        connection = pymysql.connect(**Common.dbconfig)
        return connection

 
    def process_item(self, item, spider):
        connection = self.getConnection()
        try:
            with connection.cursor() as cursor:
                if isinstance(item, ArticleItem):
                    #  check art exsist
                    cursor.execute("select * from mdcalc where docid = %s", (item['docid']))
                    result = cursor.fetchone()
                    if result:
                            print("art already exist")        
                    else:
                            calc_desc = json.dumps(item['calc_desc'])

                            use_cases_json = item['use_cases']
                            use_cases=''
                            if use_cases_json : 
                                use_cases = json.dumps(use_cases_json)
                            
                            pearls_pitfalls_json=item['pearls_pitfalls']
                            pearls_pitfalls = ''
                            if pearls_pitfalls_json:   
                                pearls_pitfalls = json.dumps(pearls_pitfalls_json)
                            
                            why_use_json = item['why_use']
                            why_use = ''
                            if why_use_json: 
                                why_use = json.dumps(why_use_json)
                            
                            nextsteps = item['nextsteps']
                            if 'Advice' in nextsteps:
                                nextsteps_Advice= json.dumps(nextsteps['Advice'])
                            else:
                                nextsteps_Advice=''
                            if 'Management' in nextsteps:
                                nextsteps_Management= json.dumps(nextsteps['Management'])
                            else:
                                nextsteps_Management=''
                            if 'Critical Actions' in nextsteps:
                                nextsteps_Critical_Actions= json.dumps(nextsteps['Critical Actions'])
                            else:
                                nextsteps_Critical_Actions=''
                            
                            
                            evidence = item['evidence']
                            
                            if 'Formula' in evidence:
                                evidence_Formula = json.dumps(evidence['Formula'])
                            else:
                                evidence_Formula = ''
                            
                            if 'Facts & Figures' in evidence:
                                evidence_Facts_Figures= json.dumps( evidence['Facts & Figures'])
                            else:
                                evidence_Facts_Figures = ''
                            
                            if 'Facts & Figures' in evidence:
                                evidence_Facts_Figures= json.dumps( evidence['Facts & Figures'])
                            else:
                                evidence_Facts_Figures = ''
                            
                            if 'Evidence Appraisal' in evidence:
                                evidence_Evidence_Appraisal= json.dumps( evidence['Evidence Appraisal'])
                            else:
                                evidence_Evidence_Appraisal = ''
                            
                            if 'Literature' in evidence:
                                evidence_Literature= json.dumps( evidence['Literature'])
                            else:
                                evidence_Literature = ''
                            
                            creators = json.dumps( item['creators'])
                            refs = json.dumps( item['refs'])

                            sql = """insert into mdcalc(  docid, db, url, calc_title, calc_desc, use_cases, pearls_pitfalls, why_use, 
                                        nextsteps_Advice, nextsteps_Management, nextsteps_Critical_Actions,
                                        evidence_Formula, evidence_Facts_Figures, evidence_Evidence_Appraisal,evidence_Literature,
                                        creators,refs )  
                                    values(%s, %s, %s, %s,%s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)
                                """
                            params = ( item["docid"], item["db"], item["url"], item["calc_title"], 
                                       calc_desc, use_cases, pearls_pitfalls, why_use, 
                                        nextsteps_Advice, nextsteps_Management, nextsteps_Critical_Actions,
                                        evidence_Formula, evidence_Facts_Figures, evidence_Evidence_Appraisal,evidence_Literature,
                                        creators,refs )
                            cursor.execute(sql, params)
                            connection.commit()
                        
                
        except pymysql.IntegrityError as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
                 
        except pymysql.InternalError as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
               
        except Exception  as e:
                print ("Error : " ,','.join(e.args))
                
        finally:
            connection.close()



class ScrapyJsonPipeline(object):
    def __init__(self):
        self.filename = Common.jsonfile
        
    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
                with codecs.open(self.filename, 'a', encoding='utf-8') as file:
                    line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                    file.write(line)
                return item
        
        else:
                pass
    
  
