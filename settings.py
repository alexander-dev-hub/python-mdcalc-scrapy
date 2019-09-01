# Scrapy settings for sciencedirect project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mdcalc_scrapy'

SPIDER_MODULES = ['mdcalc_scrapy.spiders']
NEWSPIDER_MODULE = 'mdcalc_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Windows 10 x86_64; ) Gecko/20100101 Chrme/60.2'
#LOG_FILE='scrapy.log'
#LOG_ENABLED = True
#LOG_LEVEL = logging.ERROR
#DOWNLOAD_DELAY = 3
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 0.3
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0


#DUPEFILTER_CLASS='scrapy.dupefilters.BaseDupeFilter'
#DUPEFILTER_CLASS = 'scraper.custom_filters.SeenURLFilter'
ITEM_PIPELINES = {

       'mdcalc_scrapy.pipelines.ScrapyMysqlPipeline': 300,
       
       #'mdcalc_scrapy.pipelines.ScrapyJsonPipeline': 100
}

MEDIA_ALLOW_REDIRECTS = True




