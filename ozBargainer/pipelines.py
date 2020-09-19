# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import os
from ast import literal_eval
from ozBargainer.settings import TARGET_PRICE_ERROR
from ozBargainer.settings import NON_TARGET
from ozBargainer.settings import TARGET_GOOD_DEAL

class OzbargainerPipeline(object):

    filename = os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(os.getcwd())), 'output.txt')

    def open_spider(self, spider):
        self.file = open(self.filename, 'a', encoding='UTF-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        total_texts = " ".join(item['post']) + " " + " ".join(item['content']) + " ".join((item['title'])).lower()
        price_error_included = []
        good_deal_included = []
        target_avoided = []
        for target in TARGET_PRICE_ERROR:
            price_error_included.append(target in total_texts)

        price_error_included = True in price_error_included

        for target in TARGET_GOOD_DEAL:
            good_deal_included.append(target in total_texts)

        good_deal_included = True in good_deal_included

        for non_target in NON_TARGET:
            target_avoided.append(non_target in total_texts)

        target_avoided = True in target_avoided

        with open(self.filename, 'r') as f:
            lines = f.readlines()
            list_read = []
            for line in lines:
                list_read.append(literal_eval(line))

        if target_avoided:
            return item

        if not any(str(d['node']) == str(item['node']) for d in list_read) and price_error_included:
            print('Match found...')
            line = json.dumps(dict(item)).replace('\\u', '/') + "\n"
            self.file.write(line)
            return item

        if not any(str(d['node']) == str(item['node']) for d in list_read) and good_deal_included:
            print('Match found...')
            line = json.dumps(dict(item)).replace('\\u', '/') + "\n"
            self.file.write(line)
            return item


