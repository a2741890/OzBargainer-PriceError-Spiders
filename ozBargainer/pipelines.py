# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import os
from ast import literal_eval
from ozBargainer.settings import TARGET_WORDS


class OzbargainerPipeline(object):

    filename = os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(os.getcwd())), 'output.txt')

    def open_spider(self, spider):
        self.file = open(self.filename, 'a', encoding='UTF-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        total_texts = " ".join(item['post']) + " " + " ".join(item['content']) + " ".join((item['title']))
        target_included = []
        for target in TARGET_WORDS:
            target_included.append(target in total_texts)

        target_included = True in target_included

        with open(self.filename, 'r') as f:
            lines = f.readlines()
            list_read = []
            for line in lines:
                list_read.append(literal_eval(line))

        if not any(d['title'] == item['title'] for d in list_read) and target_included:
            print('Match found...')
            line = json.dumps(dict(item)).replace('\\u', '/') + "\n"
        else:
            line = ''

        self.file.write(line)
        return item
