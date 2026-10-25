import threading

import requests

from util.CookieManager import CookieManager


class CppRequest:
    def __init__(self, headers=None, cookies_config_path="", timeout=3):
        self.session = requests.Session()
        self.cookieManager = CookieManager(cookies_config_path)
        # 超时默认 3 秒，原 1 秒在高频抢票下极易无谓超时失败
        self.timeout = timeout
        # cookie 字符串缓存 + 锁：避免多线程并发读 TinyDB 文件导致 JSON 竞争
        self._cookie_lock = threading.Lock()
        self._cookie_str = None
        self.headers = headers or {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4',
            'cookie': "",
            'origin': 'https://cp.allcpp.cn',
            'priority': 'u=1, i',
            'referer': 'https://cp.allcpp.cn/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
        }

    def get_cookies_str(self):
        """带缓存与锁的 cookie 读取，线程安全"""
        with self._cookie_lock:
            if self._cookie_str is None:
                self._cookie_str = self.cookieManager.get_cookies_str()
            return self._cookie_str

    def refresh_cookies(self):
        """登录/切换账号后调用，刷新 cookie 缓存"""
        with self._cookie_lock:
            self._cookie_str = self.cookieManager.get_cookies_str()
        return self._cookie_str

    def get(self, url, params=None):
        self.headers["cookie"] = self.get_cookies_str()
        response = self.session.get(url, params=params, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response

    def post(self, url, data=None, json=None):
        self.headers["cookie"] = self.get_cookies_str()
        response = self.session.post(url, data=data, json=json, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response

    def get_request_name(self):
        try:
            if not self.cookieManager.have_cookies():
                return "未登录"
            result = self.get("https://www.allcpp.cn/allcpp/circle/getCircleMannage.do").json()
            return result["result"]["joinCircleList"][0]["nickname"]
        except Exception as e:
            return "未登录"


if __name__ == "__main__":
    test_request = CppRequest(cookies_config_path="cookies.json")
    res = test_request.get("https://www.allcpp.cn/api/tk/getList.do?type=1&sort=0&index=1&size=10")
    print(res.headers)
    print(res.text)
