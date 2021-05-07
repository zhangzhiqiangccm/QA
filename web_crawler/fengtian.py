import scrapy
import re
import logging
import json
# 创建一个爬虫类，继承了scrapy.Spider
class FengtianSpider(scrapy.Spider):
    name = 'fengtian' # 爬虫的名称
    allowed_domains = ['wwww.che168.com']   # 爬虫允许进入的域，限定爬虫范围
    start_urls = ['https://www.che168.com/china/fengtian/#pvareaid=104649/']    # 启动爬虫的初始链接，也就是爬虫的起点URL


# 拿到起始URL请求的相应（response）后，传入parse函数（此函数名称不能改）
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

            # print(f"型号：{model}， 里程数：{dist}万公里， 所在地：{city}， 日期：{date}， 价格：{price}")
            detail_path = item.xpath('./a/@href').extract_first()
            detail_url = f'https://www.che168.com{detail_path}'

            info_dic = {'车辆型号': model, '车辆里程数': dist + '万公里',
                        '车辆所在地': city, '上架日期': date, '车辆价格': price}
            yield scrapy.Request(detail_url, callback=self.parse_detail_page, meta=info_dic)

            # 获取下一页的url
        next_url = response.xpath('//a[@class="page-item-next"]/@href').extract_first()
        if next_url:
            full_nextlink = 'https://www.che168.com/' + next_url
            logging.info(f'next page: {full_nextlink}')
            yield scrapy.Request(full_nextlink, callback=self.parse)

    def parse_detail_page(self, response):
        seller_info = re.findall(
            '<span class="manger-name">(.*?)</span>', response.text)[0]
        seller_location = re.findall(
            '<div class="protarit-adress">(.*?)</div>', response.text)[0]
        info_dic = response.meta
        print(f"{info_dic}，商家/个人信息：{seller_info}，商家/个人详细地址：{seller_location}")