# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

 
class ArticleItem(Item):
    
    db=Field()
    docid= Field()
    url =Field()
    calc_title = Field()
    creators = Field()
    calc_desc =Field()
    
    use_cases = Field()
    pearls_pitfalls=Field()
    why_use=Field()
    
    nextsteps=Field()
    evidence=Field()
    
    refs = Field()

    