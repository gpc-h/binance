#! /usr/bin/env python
# coding=UTF8

import requests
from lxml import html as HTML

class a():
    def start(self, url):
        headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        }
        req = requests.session()
        doc = req.get(url, headers=headers, verify=False)
        try:
            html = HTML.fromstring(doc.decode('utf-8'))
        except Exception, e:
            print str(e)
        return html

    def parse_oen(self, doc):
        try:
            html = HTML.fromstring(doc.decode('utf-8'))
        except Exception, e:
            print str(e)
        title = html.xpath('//header[@class="article-header"]/h1/text()')
        time = html.xpath('//li[@class="meta-data"]//@datetime')
        info = html.xpath('//div[@class="article-body"]//text()')
        print title, time, info
        return title, time, info

    def parse_page(self, html):
        url_base = 'https://support.binance.com'
        hrefs = html.xpath('//li[@class="article-list-item"]/a/@href')
        for one in hrefs:
            url = url_base + one
            doc_t = self.start(url)
            self.parse_oen(doc_t)

    def parse_first(self, url):
        html = self.start(url)
        pages = html.xpath('//li[@class="pagination-last"]//@href')
        max_pages = pages.split('=')[1][0]

        for i in max_pages:
            url_oher = 'https://support.binance.com/hc/zh-cn/sections/115000106672?page=%s#articles' % i
            html = self.start(url_oher)
            self.parse_page(html)

if __name__ == '__main__':
    url = 'https://support.binance.com/hc/zh-cn/sections/115000106672-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF'
    a =a()
    a.parse_first(url)

