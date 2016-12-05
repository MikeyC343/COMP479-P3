import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
try:
    import json
except ImportError:
    import simplejson as json
import os




class QuotesSpider(scrapy.Spider):
    name = "biology"
    allowed_domains = ['concordia.ca']


    def __init__(self):
        self.urlCounter = 0

    def start_requests(self):
        urls = [
            # 'http://www.concordia.ca/artsci/biology.html'
            # 'http://www.concordia.ca/artsci/chemistry.html'
            'http://www.concordia.ca/artsci/exercise-science.html'
            # 'http://www.concordia.ca/artsci/geography-planning-environment.html'
            # 'http://www.concordia.ca/artsci/math-stats.html'
            # 'http://www.concordia.ca/artsci/physics.html'
            # 'http://www.concordia.ca/artsci/psychology.html'
            # 'http://www.concordia.ca/artsci/science-college.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.replace('.html','').replace('/', '-').replace(':', '')
        filename = '%s.json' % page

        self.urlCounter += 1
        
        # if self.urlCounter < 100:
        with open('project3/corpus/exercise-science/' + filename, 'wb') as theFile:
            postingsList = {}
            postingsList[str(response.url)] = {}
            postingsList[str(response.url)] = (
                response.xpath('//p/text()').extract(),
                response.xpath('//span/text()').extract(),
                response.xpath('//span/text()').extract(),
                response.xpath('//a/text()').extract(),
                response.xpath('//h1/text()').extract(),
                response.xpath('//h2/text()').extract(),
                response.xpath('//h3/text()').extract(),
                response.xpath('//h4/text()').extract(),
                response.xpath('//h5/text()').extract(),
                response.xpath('//h6/text()').extract())
            json.dump(postingsList, theFile)
        # else:
        #     raise CloseSpider('At the upper limit')

        for url in response.xpath('//a[contains(@href, "exercise-science")]/@href').extract():
            if url.endswith('.html'):
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parse)
            else:
                continue










