import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
try:
    import json
except ImportError:
    import simplejson as json
import os




class QuotesSpider(scrapy.Spider):
    name = "biology"
    allowed_domains = ['concordia.ca']

    def start_requests(self):
        urls = [
            'http://www.concordia.ca/artsci/biology.html'
            # 'http://www.concordia.ca/artsci/chemistry.html',
            # 'http://www.concordia.ca/artsci/exercise-science.html',
            # 'http://www.concordia.ca/artsci/geography-planning-environment.html',
            # 'http://www.concordia.ca/artsci/math-stats.html',
            # 'http://www.concordia.ca/artsci/physics.html',
            # 'http://www.concordia.ca/artsci/psychology.html',
            # 'http://www.concordia.ca/artsci/science-college.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.replace('.html','').replace('/', '-').replace(':', '')
        filename = 'biology-%s.json' % page
        with open('project3/corpus/' + filename, 'wb') as theFile:
            postingsList = {}
            postingsList[str(response.url)] = []
            postingsList[str(response.url)].extend((
                response.xpath('//p/text()').extract(),
                response.xpath('//span/text()').extract(),
                response.xpath('//span/text()').extract(),
                response.xpath('//a/text()').extract(),
                response.xpath('//h1/text()').extract(),
                response.xpath('//h2/text()').extract(),
                response.xpath('//h3/text()').extract(),
                response.xpath('//h4/text()').extract(),
                response.xpath('//h5/text()').extract(),
                response.xpath('//h6/text()').extract()))
            json.dump(postingsList, theFile)
        for url in response.xpath('//a[contains(@href, "biology")]/@href').extract():
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse)

    # def removeRN(self, tag ,response):
    #     clean = response.xpath('//' + tag + '/text()').extract()
    #     for obj in clean:
    #         preClean = obj.split('\r\n')
    #         preClean[0] = preClean[0].strip()
    #         clean.append(preClean[0])
    #     return clean
