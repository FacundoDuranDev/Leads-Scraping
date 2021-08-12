import json
import requests
import yaml
from yaml.loader import SafeLoader
import time
from utils.mongo import Mongo
from utils.async_requests import _async_requests
from utils.payload import Payload


class Faire:
    def __init__(self,config,type,site):
        self.config = config['Sites']
        self.url = self.config[site]['url']
        self.created_at = time.strftime('%Y-%m-%d')
        self.site = site
        self.mongo = Mongo()
        self.test_mongo = Mongo('testing')
        self.session = requests.session()
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
        if type == "prescraping":
            self._pre_scraping()
            self.pre_scraping = True
            self.scraping()
    def _pre_scraping(self):
        token_list = self.get_brand_tokens()
        response_list = _async_requests(token_list,max_workers=1000)
        for response in response_list:
            self.test_mongo.InsertOne({'Response':response.json(), "Site": self.site})
        pass
    def _scraping(self,testing=False):
        response_list = self.test_mongo.search({'Site': "Faire"})
        response_list = list(response_list)
        for response in response_list:
            payload = self.get_payload(response['Reponse'])
            print(payload.payload_dict())        
            # data = {
        #     "pagination_data":{
        #         "page_number":37,
        #         "page_size":37
        #     },
        #     "container_name":"marketplace_maker_grid",
        #     "max_products_per_brand":10,
        #     "category":"Top Sellers",
        #     "return_filter_sections":True,
        #     "filter_keys":[
        #     ],
        #     "simplified_result_counts":True,
        #     "is_initial_request":False,
        #     "return_only_new_brands":False
        # }
        # data = json.dumps(data)
        # rq_ = requests.post(self.url,data=data,headers=self.headers)
        # json_ = rq_.json()
        # if json_['brands']:
        #     for content in json_['brands']:
        #         print(content['name'])
    
    def get_brand_tokens(self):
        token_list = []
        list_brands = self.session.get('https://www.faire.com/api/brand/list-brands')
        brands_json = list_brands.json()
        for content in brands_json['brands']:
            token_list.append("https://www.faire.com/api/brand-view/"+content['token'])
        return token_list
        pass
    def get_data(self,page,category):
        {
            "pagination_data":{
                "page_number":page,
                "page_size":37
            },
            "container_name":"marketplace_maker_grid",
            "max_products_per_brand":10,
            "category":category,
            "return_filter_sections":True,
            "filter_keys":[
            ],
            "simplified_result_counts":True,
            "is_initial_request":False,
            "return_only_new_brands":False
        }
        pass

    def get_headers(self):
        pass
    def get_payload(self,content_metadata):

        payload = Payload()

        payload.name = self.get_name(content_metadata)
        payload.country_code = self.get_country_code(content_metadata)
        payload.creation_year = self.get_creation_year(content_metadata)
        payload.city = self.get_city(content_metadata)
        payload.category = self.get_category(content_metadata)
        payload.description = self.get_description(content_metadata)
        payload.id = self.get_id(content_metadata)
        payload.images = self.get_images(content_metadata)
        payload.instagram = self.get_instagram(content_metadata)
        payload.instagram_followers = self.get_instagram_followers(content_metadata)
        payload.likes = self.get_likes(content_metadata)
        payload.banner_image = self.get_banner_image(content_metadata)
        payload.facebook_followers = self.get_facebook_followers(content_metadata)
        payload.facebook_handle = self.get_facebook_handle(content_metadata)
        payload.owner_name = self.get_owner_name(content_metadata)
        payload.hand_made = self.get_hand_made(content_metadata)
        payload.made_in = self.get_made_in(content_metadata)
        payload.social_media_images = self.get_social_media_images(content_metadata)
        payload.sold_on_amazon = self.get_sold_on_amazon(content_metadata)
        payload.url = self.get_url(content_metadata)
        payload.twitter_followers = self.get_twitter_followers(content_metadata)
        payload.videos = self.get_videos(content_metadata)
        payload.average_rating = self.get_average_rating(content_metadata)
        payload.active_products_count = self.get_active_products_count(content_metadata)
        payload.logo = self.get_logo(content_metadata)
        payload.phone_number = self.get_phone_number(content_metadata)
        payload.email = self.get_email(content_metadata)

        return payload
    def get_country_code(self,content_metadata):
        if "based_in" in content_metadata:
            country_code = content_metadata['brand']['based_in']
            return country_code
    def get_creation_year(self,content_metadata):
        if "creation_year" not in content_metadata:
            try:
                creation_year = content_metadata['brand']['creation_year']
                return creation_year
            except:
                return None
    def get_category(self,content_metadata):
        requests_category = self.session.get(
            'https://www.faire.com/api/brand/{}/top-category'.format(
                content_metadata['brand']['token']
            )
        )
        category_json = requests_category.json()
        if "category_name" in category_json:
            category_name = category_json['category_name']
            return category_name

        pass
    def get_description(self,content_metadata):
        description = content_metadata['brand']['description']
        return description
        pass
    def get_city(self,content_metadata):
        if "based_in_city" in content_metadata:
            city = content_metadata['brand']['based_in_city']
            return city
        pass
    def get_id(self,content_metadata):
        id = content_metadata['brand']['token']
        return id
        pass
    def get_images(self,content_metadata):
        images = []
        images_list = content_metadata['brand']['images']
        for content in images_list:
            images.append(content['url'])
        if "story_image" in content_metadata:
            story_image = content_metadata['story_image']
            images.append(story_image['url'])
        return images
        pass
    def get_instagram(self,content_metadata):
        if "instagram_handle" in content_metadata:
            instagram = content_metadata['brand']['instagram_handle']
            return "@"+instagram
    def get_instagram_followers(self,content_metadata):
        if "instagram_followers" in content_metadata:
            instagram_followers = content_metadata['brand']['instagram_followers']
            return instagram_followers
        pass
    def get_name(self,content_metadata):
        name = content_metadata['brand']['name']
        return name
        pass
    def get_likes(self,content_metadata):
        if "likes" in content_metadata:
            likes = content_metadata['brand']['likes']
            return likes
        pass
    def get_banner_image(self,content_metadata):
        banner_image = content_metadata['brand']['banner_image']['url']
        return banner_image
        pass
    def get_facebook_followers(self,content_metadata):
        if "facebook_followers" in content_metadata:
            facebook_followers = content_metadata['brand']['facebook_followers']
            return facebook_followers
        pass
    def get_facebook_handle(self,content_metadata):
        if "facebook_handle" in content_metadata:
            facebook_handle = content_metadata['brand']['facebook_handle']
            return facebook_handle
        pass
    def get_owner_name(self,content_metadata):
        pass
    def get_hand_made(self,content_metadata):
        pass
    def get_made_in(self,content_metadata):
        pass
    def get_social_media_images(self,content_metadata):
        pass
    def get_sold_on_amazon(self,content_metadata):
        pass
    def get_url(self,content_metadata):
        pass
    def get_twitter_followers(self,content_metadata):
        pass
    def get_videos(self,content_metadata):
        pass
    def get_average_rating(self,content_metadata):
        pass
    def get_active_products_count(self,content_metadata):
        pass
    def get_logo(self,content_metadata):
        pass
    def get_phone_number(self,content_metadata):
        pass
    def get_email(self,content_metadata):
        pass