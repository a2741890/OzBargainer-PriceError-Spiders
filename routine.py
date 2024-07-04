from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from ozBargainer.settings import TARGET_PRICE_ERROR
from ozBargainer.settings import TARGET_GOOD_DEAL
from ozBargainer.utility import Utility
from ozBargainer.spiders.ozBargainer import OzBargainerSpider
import datetime


sleep_interval = 120

def crawl_job():
    print('Start crawling...')
    print(datetime.datetime.now())
    settings = get_project_settings()
    print('Search for words: %s' % ", ".join(TARGET_PRICE_ERROR), ",", ", ".join(TARGET_GOOD_DEAL))
    runner = CrawlerRunner(settings)
    return runner.crawl(OzBargainerSpider)

def after_crawl(null):
    print('Crawling finished...')
    Utility.sendMailToUser()
    print('Waiting for next crawling...')
    reactor.callLater(sleep_interval, crawl)

def crawl():
    d = crawl_job()
    d.addCallback(after_crawl)
    d.addErrback(catch_error)

def catch_error(failure):
    print(failure.value)


if __name__ == "__main__":
    crawl()
    reactor.run()

