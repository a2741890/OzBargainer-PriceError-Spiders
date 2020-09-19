import scrapy
import time
from ozBargainer.items import OzbargainerItem
from ozBargainer.settings import CRAWL_LENGTH


class OzBargainerSpider(scrapy.Spider):
    name = 'priceError'
    allowed_domains = ['ozbargain.com.au']
    start_urls = ['https://www.ozbargain.com.au/deals']

    def parse(self, response):
        target = response.css('div#main.main')

        for tag in target:
            try:
                first_post = tag.css('h2.title a::attr(href)').extract_first().replace('/node/', '')

            except IndexError:
                pass

            continue

        for i in range(CRAWL_LENGTH):
            time.sleep(1)
            url = 'https://www.ozbargain.com.au/node/' + str(int(first_post) - i)
            yield scrapy.Request(url, callback=self.parse_comment, meta={'url': url, 'node': str(int(first_post) - i)})

    def parse_comment(self, response):
        target = response.css('div#main.main')
        item = OzbargainerItem()
        url = response.meta.get('url')
        node = response.meta.get('node')

        for tag in target:
            try:
                item['node'] = node
                item['title'] = tag.css('div#main.main h1::attr(data-title)').extract_first()
                item['post'] = tag.css('div.node.node-ozbdeal div.content p::text').extract()
                item['content'] = tag.css('div.comment div.n-right div.content p::text').extract()
                item['date'] = tag.css('div.meta div.submitted a:nth-child(n+2):nth-child(-n+3)::text').extract()
                item['url'] = url
                item['time'] = time.time()

                yield item

            except IndexError:
                pass

            continue


