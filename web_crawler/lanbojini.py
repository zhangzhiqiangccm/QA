import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LanbojiniSpider(CrawlSpider):
    name = 'lanbojini'
    # allowed_domains = ['https://www.che168.com/']
    start_urls = ['https://www.che168.com/china/lanbojini/?pvareaid=101025']

    link_extractor = LinkExtractor(
        allow=r'/china/lanbojini/a0_0msdgscncgpi1ltocsp\d+exx0/\?pvareaid=102179#currengpostion')

    rule = Rule(link_extractor, callback='parse_item', follow=True)
    rules = (
        rule,
    )

    def parse_item(self, response):
        print(response.text)
