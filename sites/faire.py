import json
import requests
import yaml
from yaml.loader import SafeLoader
import time
from utils.mongo import Mongo


class Faire:
    def __init__(self,config,type,site):
        self.config = config['Sites']
        self.url = self.config[site]['url']
        self.created_at = time.strftime('%Y-%m-%d')
        self.mongo = Mongo()
        self.headers = {
        'authority': 'www.faire.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
        'x-faire-timezone': 'America/Buenos_Aires',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'x-if-client-release': '9f117660:a43393e9:0',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'x-if-wsat': '5r1fwygjewes5d1wlz6yzbh0074krsm24bts6gc98mr6x8zh01581hksnnxmasmabikjloy7en9ak7a9eim7j9n7i2n4yj2wuebf',
        'dpr': '1',
        'x-accept-currency': 'USD',
        'x-if-app-identifier': 'web-retailer',
        'x-is-apparel': 'false',
        'origin': 'https://www.faire.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.faire.com/category/Top%20Sellers',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'cookie': 'indigofair_session=eyJzZXNzaW9uX3Rva2VuIjoiNXIxZnd5Z2pld2VzNWQxd2x6Nnl6YmgwMDc0a3JzbTI0YnRzNmdjOThtcjZ4OHpoMDE1ODFoa3NubnhtYXNtYWJpa2psb3k3ZW45YWs3YTllaW03ajluN2kybjR5ajJ3dWViZiJ9--c1abc9583a014c005a5a1009bb2ef1ca9082080a3d2a753f69ebf4e6a1bd83582f9032e1605a134d41ebf818dd92d89ff67d324eff856e11265b715cd3477324; _ga=GA1.2.701631336.1628553791; _gid=GA1.2.571553506.1628553791; _fbp=fb.1.1628553791262.465845606; _pin_unauth=dWlkPVpHRTJZVEUwTTJJdFlqRTJOUzAwTTJJekxUbG1abVV0Tm1Ga04yVmpOemhqWW1SaQ; _gcl_au=1.1.367746679.1628553792; __hstc=62287155.462d8801b9de513532c892b80fe20422.1628553793504.1628553793504.1628553793504.1; hubspotutk=462d8801b9de513532c892b80fe20422; __hssrc=1; OptanonAlertBoxClosed=2021-08-10T00:03:47.336Z; OptanonConsent=isIABGlobal=false&datestamp=Mon+Aug+09+2021+21%3A03%3A47+GMT-0300+(Argentina+Standard+Time)&version=6.17.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false; _uetsid=59dbafb0f96e11eb97849f7a3e4dbb25; _uetvid=59dbebc0f96e11eb91d0cf6d2ec058f5; __hssc=62287155.2.1628553793506; _gat_UA-90386801-1=1',
}
        if type == "scraping":
            self._scraping()
        if type == "testing":
            self._scraping(testing=True)
        
    def _scraping(self,testing=False):
        data = {
            "pagination_data":{
                "page_number":1,
                "page_size":37
            },
            "container_name":"marketplace_maker_grid",
            "max_products_per_brand":4,
            "category":"Top Sellers",
            "return_filter_sections":True,
            "filter_keys":[
            ],
            "simplified_result_counts":True,
            "is_initial_request":False,
            "return_only_new_brands":False
        }
        data = json.dumps(data)
        rq_ = requests.post(self.url,data=data,headers=self.headers)
        json_ = rq_.json()
        for content in json_['brands']:
            print(content['name'])
        pass
