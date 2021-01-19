# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
    添加user agent等
    """
    def __init__(self, user_agent=''):
        super().__init__(user_agent)
        self.user_agent = user_agent

    def process_request(self, request, spider):
        # 设置 user-agent
        ua = random.choice(self.user_agent_list)
        if ua:
            # 设置 user-agent
            request.headers.setdefault('User-Agent', ua)
        # print("Request Header:", request.headers)
        # print("Request Url:", request.url)

            # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape

    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        ]


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # Set the location of the proxy
        # request.meta['proxy'] = "http://58.67.159.50:80"
        pass

# 设置代理
# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
# import base64
#
#
# # Start your middleware class
# class ProxyMiddleware(object):
#     # overwrite process request
#     def process_request(self, request, spider):
#         # Set the location of the proxy
#         request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
#
#         # Use the following lines if your proxy requires authentication
#         proxy_user_pass = "USERNAME:PASSWORD"
#         # setup basic authentication for the proxy
#         encoded_user_pass = base64.encodestring(proxy_user_pass)
#         request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
#
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#     'pythontab.middlewares.ProxyMiddleware': 100,
# }
