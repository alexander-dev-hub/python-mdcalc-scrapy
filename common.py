import pprint
import logging
from scrapy.utils.log import configure_logging
import pymysql
import random
import json
import codecs
import os

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 8.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 7; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 8.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 8.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 8.1)',
    'Mozilla/5.0 (Windows NT 8.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 8.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 8.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 8.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 8.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 8.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 8.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 7; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
class Common:
    dbconfig = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'mdcalc',
            'charset': 'utf8',
            'use_unicode': 'true',
            'cursorclass': pymysql.cursors.DictCursor
        }
    jsonfile='mdcalc.json'
    @staticmethod
    def init_log( logfile):
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            handlers=[logging.FileHandler(logfile, 'w', 'utf-8')],
            level=logging.INFO
        )
        #logger = logging.getLogger('scrapy.middleware')
        #logger.setLevel(logging.ERROR)
  
    @staticmethod
    def check_db_exist( url):

        connection = pymysql.connect(**Common.dbconfig)
        with connection.cursor() as cursor:
            try:
                cursor.execute("select * from nasa where docid = %s", url)
                result = cursor.fetchone()
                if result:
                    print("check already exist")
                    return True

            except Exception  as e:
                print("Error : ", ','.join(e.args))

            finally:
                connection.close()
        return False

    @staticmethod
    def get_random_useraget():
        return random.choice(user_agent_list)

    @staticmethod
    def exist_in_json(docid):
        if not os.path.isfile(Common.jsonfile):
            return False
        with codecs.open(Common.jsonfile, 'r', encoding='utf-8') as fp:
            while True:
                line = fp.readline()
                
                if not line: 
                    break
                oneitem= json.loads(line)
                if oneitem['docid'] == docid:
                    print('exist:', docid)
                    return True
                
        return False
