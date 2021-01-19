# codding: utf-8
# python 3.6+
import traceback
import urllib
import urllib.request
import urllib.parse
import time
from urllib import request

import requests

proxy_ips = [
#    '92.124.195.22:3128',
#   '182.48.88.178:8080',
]

cookie = '''bid=85fPMeGjPgk; viewed="2275112"; gr_user_id=20d26b9c-4c2b-4295-ad50-8d36a1d6fcbc; ll="118123"; ps=y; ue="szhkai@126.com"; dbcl2="81196518:uhkeSzyyOjY"; ap=1; ct=y; _vwo_uuid_v2=D9F935522A9C08EEDEAD590B2A4D8034|d0ab446b5d78650218f468438e5e004e; ck=S7Gq; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1497865071%2C%22https%3A%2F%2Fsite.douban.com%2F235619%2Fwidget%2Fnotes%2F16593178%2Fnote%2F622017606%2F%22%5D; _pk_id.100001.8cb4=f8d0227b2fb8903b.1494571674.21.1497865071.1497257692.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utmt=1; __utma=30149280.1886096184.1494571675.1497344804.1497865071.27; __utmb=30149280.2.10.1497865071; __utmc=30149280; __utmz=30149280.1497254139.25.8.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E4%B9%A6%E5%8D%95; __utmv=30149280.8119'''


class ProxyManager(object):

    @staticmethod
    def reload_ips():
        # 下载代理ip
        # ips = ''
        # ips = str(HtmlDownloader.download('http://api.xicidaili.com/free2016.txt', delay=0, use_proxy=False), encoding='utf-8')
        ips = str(
            HtmlDownloader.download('http://tvp.daxiangdaili.com/ip/?tid=555709422560593&num=1', use_proxy=False),
            encoding='utf-8')
        with open('proxy-use', 'a') as f:
            f.write(ips + '\n')
        print("重新装载代理IP:", ips)
        for ip in ips.split():
            proxy_ips.append(ip)

    @staticmethod
    def get_proxy_ip():
        if len(proxy_ips) == 0:
            ProxyManager.reload_ips()
        if len(proxy_ips) != 0:
            ip = proxy_ips.pop(0)
            proxy_ips.append(ip)
            return ip
        else:
            return None

    @staticmethod
    def remove_ip(ip):
        try:
            if len(proxy_ips) == 0:
                ProxyManager.reload_ips()

            proxy_ips.remove(ip)
            print("删除了代理:", ip)

            if len(proxy_ips) == 0:
                ProxyManager.reload_ips()
        except Exception as e:
            traceback.print_exc()
            print(e)


class HtmlDownloader(object):

    @staticmethod
    def download(url, data=None, delay=0, use_proxy=True):
        if use_proxy:
            for _i in range(10):
                _proxy_ip = ProxyManager.get_proxy_ip()
                try:
                    return HtmlDownloader.download_solve(url, data, delay, _proxy_ip)
                except Exception as e:
                    # traceback.print_exc()
                    print('下载出错:', e)
                    print('尝试更换代理')
                    ProxyManager.remove_ip(_proxy_ip)
        else:
            return HtmlDownloader.download_solve(url, data=data, delay=delay, proxy_ip=None)

    @staticmethod
    def download_solve(url, data=None, delay=15, proxy_ip=None, timeout=10):
        """下载页面"""
        if url is None:
            return None

        if delay:
            try:
                print('sleep ', delay, ' seconds')
                delay = int(delay)
                time.sleep(delay)
                print('sleep over')
            except Exception as e:
                print(e)
                traceback.print_exc()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/31.0.1650.63 Safari/537.36',
        }

        # proxy_ip = "socks5://localhost:9050"
        if proxy_ip and not str(proxy_ip).startswith("http"):
            proxy_ip = "http://" + str(proxy_ip)
        proxies = {
            "http": proxy_ip,
            "https": proxy_ip,
            "socks5": proxy_ip,
        }

        if proxy_ip:
            # proxies = {'http': "http://" + proxy_ip}
            print("使用代理IP:", proxies)
            res = requests.get(url, params=data, headers=headers, proxies=proxies, timeout=timeout)
            return res.content
        else:
            return requests.get(url, params=data, headers=headers, timeout=timeout).content

    # @staticmethod
    # def download_response(url, data=None, delay=None, use_proxy=False):
    #     """
    #     下载页面
    #     :param url:
    #     :param data:
    #     :param delay: 下载延迟, 单位: 秒
    #     :return:
    #     """
    #     if url is None:
    #         return None
    #
    #     if delay:
    #         try:
    #             print('sleep ', delay, ' seconds')
    #             delay = int(delay)
    #             time.sleep(delay)
    #             print('sleep over')
    #         except Exception as e:
    #             print(e)
    #             traceback.print_exc()
    #
    #     if data is not None:
    #         data = urllib.parse.urlencode(data).encode(encoding="utf-8")
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                       'Chrome/31.0.1650.63 Safari/537.36'}
    #     if use_proxy:
    #         proxy_handler = urllib.request.ProxyHandler({'http': ProxyManager.get_proxy_ip()})
    #         req = urllib.request.Request(url, data, headers, proxy_handler)
    #     else:
    #         req = urllib.request.Request(url, data, headers)
    #     res = urllib.request.urlopen(req, timeout=15)
    #     if res.getcode() != 200:
    #         print("下载页面 %s 失败." % res.url)
    #         return None
    #     print("下载页面 %s 成功." % res.url)
    #     return res


if __name__ == "__main__":
    # print(str(HtmlDownloader.download('http://tvp.daxiangdaili.com/ip/?tid=555709422560593&num=10', use_proxy=False), encoding='utf-8'))
    # print(str(HtmlDownloader.download('http://tvp.daxiangdaili.com/ip/?tid=555709422560593&num=10', use_proxy=False), encoding='utf-8'))
    print(HtmlDownloader.download('http://book.szhkai.win/your-ip/', delay=0, use_proxy=True))
    # for i in range(100):
    #     print(ProxyManager.get_proxy_ip())
    # downloader = HtmlDownloader()
    # print(str(downloader.download("http://toutiao.io/"), encoding='utf8'))
    # print(str(HtmlDownloader.download('http://api.xicidaili.com/free2016.txt', use_proxy=False, delay=0), encoding='utf-8'))
    pass
