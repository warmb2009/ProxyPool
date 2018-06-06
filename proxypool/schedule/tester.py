import asyncio
import aiohttp
from blessings import Terminal

class UsabilityTester(object):
    """检验器，负责检验给定代理的可用性。"""
    test_api = 'https://www.baidu.com'

    def __init__(self):
        self.raw_proxies = None
        self._usable_proxies = None
        self.t = Terminal()
        
    def set_raw_proxies(self, raw_proxies):
        self.raw_proxies = raw_proxies

        self._usable_proxies = []

    async def test_single_proxy(self, proxy):
        async with aiohttp.ClientSession() as session:
            try:
                real_proxy = 'http://' + proxy
                async with session.get(self.test_api, proxy=real_proxy, timeout=15) as resp:
                    self._usable_proxies.append(proxy)
                info_str = '%s 代理可用，加入代理池!' % (real_proxy)
                print(self.t.green(info_str))
            except Exception:
                waring_str = '错误，%s 代理不可用!' % (real_proxy)
                print(self.t.red(waring_str))
                # print(Exception.__name__)

    def test(self):
        system_str = 'Usability tester is working...[测试代理ip是否可用]'
        print(self.t.blue(system_str))
        loop = asyncio.get_event_loop()
        tasks = [self.test_single_proxy(proxy) for proxy in self.raw_proxies]
        loop.run_until_complete(asyncio.wait(tasks, loop=loop))

    @property
    def usable_proxies(self):
        return self._usable_proxies
