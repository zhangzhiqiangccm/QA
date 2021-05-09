import scrapy
import re
import logging
import json

class LaosilaisiSpider(scrapy.Spider):
    name = 'laosilaisi'
    allowed_domains = ['www.che168.com']
    start_urls = [
        'https://www.che168.com/china/laosilaisi/#pvareaid=105866#listfilterstart']

    def parse(self, response):
        item_list = response.xpath(
            '//ul[@class="viewlist_ul"]/li[@name="lazyloadcpc"]')

        for item in item_list:
            # 型号
            model = item.xpath('./a/div[2]/h4/text()').extract_first()
            # 价格
            price = item.xpath('.//span[@class = "pirce"]//text()').extract_first()

            # 描述：2.4万公里／2020-05／武汉／3年会员商家
            desc = item.xpath('./a/div[2]/p/text()').extract_first()
            # 用正则提取里程，日期和城市
            dist = ''.join(re.findall('.*万公里', desc))
            date = ''.join(re.findall('\d{4}-\d{2}', desc))
            city = ''.join(re.findall('.*万公里／.*／(.*)／', desc))

            # info_dic = {'车辆型号': model, '车辆里程数': dist + '万公里',
            #             '车辆所在地': city, '上架日期': date, '车辆价格': price}
            # print(info_dic)
            info_dic = {'车辆型号': model, '车辆里程数': dist + '万公里',
                        '车辆所在地': city, '上架日期': date, '车辆价格': price}
            # print(info_dic)
            yield info_dic

# 获取下一页的url
        next_url = response.xpath('//a[@class="page-item-next"]/@href').extract_first()
        if next_url:
            full_nextlink = 'https://www.che168.com/' + next_url
            logging.info(f'next page: {full_nextlink}')
            yield scrapy.Request(full_nextlink, callback=self.parse)