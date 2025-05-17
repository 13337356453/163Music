from json import loads
from urllib.parse import quote

import requests

from JS import JS

requests.packages.urllib3.disable_warnings()
class Musicer:
    url='https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    headers={
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Referer': 'https://music.163.com/search/',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    jsonStr='{"ids":"[%s]","level":"exhigh","encodeType":"aac","csrf_token":""}'
    def __init__(self,musicid,cookie,name,proxies={}):
        self.musicid=str(musicid)
        self.headers['Cookie']=cookie
        self.proxies=proxies
        self.name=name

    def getDownloadUrl(self):
        s=self.jsonStr%self.musicid
        params,encSecKey=JS.d(s)
        data=f"""params={quote(params)}&encSecKey={quote(encSecKey)}"""
        try:
            r=requests.post(self.url,headers=self.headers,data=data,verify=False,timeout=10,proxies=self.proxies)
            if r.status_code==200:
                return loads(r.content.decode())['data'][0]['url']
            return None
        except Exception as e:
            print(e)
            return None
    def download(self):
        url=self.getDownloadUrl()
        try:
            r=requests.get(url,proxies=self.proxies,verify=False,timeout=10)
            if r.status_code==200:
                with open(f'{self.name}.mp3','wb') as f:
                    f.write(r.content)
                    print(f"[+] {self.name}.mp3 已保存")
        except Exception as e:
            print(f'[!] {e}')