import requests
from urllib.parse import quote
from json import loads

from JS import JS

requests.packages.urllib3.disable_warnings()
class Searcher:
    url="https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    headers={
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Referer': 'https://music.163.com/search/',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    jsonStr="{\"hlpretag\":\"<span class=\\\"s-fc7\\\">\",\"hlposttag\":\"</span>\",\"s\":\"%s\",\"type\":\"1\",\"offset\":\"0\",\"total\":\"true\",\"limit\":\"%d\",\"csrf_token\":\"\"}"
    def __init__(self,keyword,proxies={},number=1,cookie=""):
        self.keyword=keyword
        self.proxies=proxies
        self.number=number
        self.headers['Cookie']=cookie

    def getData(self):
        s=self.jsonStr%(self.keyword,self.number)
        params,encSecKey=JS.d(s)
        data=f"""params={quote(params)}&encSecKey={quote(encSecKey)}"""
        try:
            r=requests.post(self.url,headers=self.headers,data=data,verify=False,timeout=10,proxies=self.proxies)
            if r.status_code==200:
                result=loads(r.content.decode())
                return result['result']['songs']
            return None
        except Exception as e:
            print(f'[!] {e}')
            return None