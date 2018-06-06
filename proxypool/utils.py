from .conf import HEADERS, HOST, WEB_PORT
from .webapi import get_conn
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp


def get_page(url):
    """将网页解析为 BeautifulSoup 对象并返回
    :param url: web url
    :return: BeautifulSoup
    """

    USE_PROXY_TO_GET_PROXY = False

    r = None

    if USE_PROXY_TO_GET_PROXY is True:
        count_url = 'http://' + str(HOST) + ':' + str(WEB_PORT) + '/count'
        size = int(requests.get(count_url).text)
        
        if size is not 0 :

            proxy_url = 'http://' + str(HOST) + ':' + str(WEB_PORT) + '/get'
            proxys_str = 'http://' + str(requests.get(proxy_url).text)
            proxies = {
                'http' : proxys_str,
            }
            r = requests.get(url, headers=HEADERS, proxys=proxies)
        else:
            r = requests.get(url, headers=HEADERS)
    else:
        r = requests.get(url, headers=HEADERS)
        
    try:
        soup = BeautifulSoup(r.content.decode("utf-8"), 'lxml')
    except UnicodeDecodeError:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup


class Downloader(object):
    """
    一个异步下载器，可以用该类代替`get_page`函数。
    由于下载速度过快，爬虫很容易被BAN。
    """

    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls
