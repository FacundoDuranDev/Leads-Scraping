import json
import requests
import yaml
import re
import time
from yaml.loader import SafeLoader
from utils.mongo import Mongo
from utils.async_requests import _async_requests
from utils.payload import Payload
from utils.colors import colors
from utils.private_keys import Private
from InstagramAPI import InstagramAPI


class Faire:
    def __init__(self,config,type,site):
        self.config = config['Sites']
        self.url = self.config[site]['url']
        self.created_at = time.strftime('%Y-%m-%d')
        self.site = site
        self.mongo = Mongo()
        self.test_mongo = Mongo('testing')
        self.session = requests.session()
        self.regex_time = re.compile(r'\d+\-\d+\-\d+')
        self.session.headers = {
        "cookie": "indigofair_session=eyJzZXNzaW9uX3Rva2VuIjoiNXIxZnd5Z2pld2VzNWQxd2x6Nnl6YmgwMDc0a3JzbTI0YnRzNmdjOThtcjZ4OHpoMDE1ODFoa3NubnhtYXNtYWJpa2psb3k3ZW45YWs3YTllaW03ajluN2kybjR5ajJ3dWViZiJ9--c1abc9583a014c005a5a1009bb2ef1ca9082080a3d2a753f69ebf4e6a1bd83582f9032e1605a134d41ebf818dd92d89ff67d324eff856e11265b715cd3477324; _ga=GA1.2.701631336.1628553791; _fbp=fb.1.1628553791262.465845606; _pin_unauth=dWlkPVpHRTJZVEUwTTJJdFlqRTJOUzAwTTJJekxUbG1abVV0Tm1Ga04yVmpOemhqWW1SaQ; _gcl_au=1.1.367746679.1628553792; hubspotutk=462d8801b9de513532c892b80fe20422; OptanonConsent=isIABGlobal=false&datestamp=Mon+Aug+16+2021+14%3A23%3A39+GMT-0300+(Argentina+Standard+Time)&version=6.17.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=AR%3BB; OptanonAlertBoxClosed=2021-08-16T17:23:39.651Z; _gid=GA1.2.65244427.1629134626; _gat_UA-90386801-1=1; _uetsid=b61c6480feb611ebbb8a31c3bf4e22b6; _uetvid=59dbebc0f96e11eb91d0cf6d2ec058f5; __hstc=62287155.462d8801b9de513532c892b80fe20422.1628553793504.1628730476917.1629134626519.7; __hssrc=1; __hssc=62287155.1.1629134626519"
        }
        self.API = InstagramAPI(Private.USER,Private.PASSWORD)
        self.API.login()
        self.scraped = self.mongo.query_field(field='Id',site=self.site,created_at=self.created_at)
        if type == "scraping":
            self._scraping()
        if type == "testing":
            self._scraping(testing=True)
        if type == "prescraping":
            self._pre_scraping()

        
    def _pre_scraping(self):
        token_list = self.get_brand_tokens()
        response_list = _async_requests(token_list,max_workers=1000,session=self.session)
        for response in response_list:
            self.test_mongo.InsertOne({
                    'response':response.json(),
                    "site": self.site,
                    'id':response.json()['brand']['token'],
                    'created_at':self.created_at
                    })
        pass
    def _scraping(self,testing=False):
        response_list = list(self.test_mongo.search({'site': "Faire"}))
        for response in response_list:
            if response['id'] not in self.scraped:
                payload = self.get_payload(response['response'])
                payload_dict = payload.payload_dict()
                if payload_dict['Id'] not in self.scraped:
                    print(f"{colors.OKGREEN}[Inserted {payload_dict['Name']} in DB] {colors.ENDC}")
                    self.mongo.InsertOne(payload.payload_dict())
                else:
                    print(f'{colors.WARNING} [{payload_dict["Name"]} already exists.] Skipping {colors.ENDC}')
    def get_brand_tokens(self):
        token_list = []
        list_brands = self.session.get('https://www.faire.com/api/brand/list-brands')
        brands_json = list_brands.json()
        
        for content in brands_json['brands']:
            if content['token'] not in self.scraped:
                token_list.append("https://www.faire.com/api/brand-view/"+content['token'])
        return token_list
    def get_payload(self,content_metadata):

        payload = Payload()
        payload.site = self.site
        payload.name = self.get_name(content_metadata)
        payload.country_code = self.get_country_code(content_metadata)
        payload.creation_year = self.get_creation_year(content_metadata)
        payload.city = self.get_city(content_metadata)
        payload.category = self.get_category(content_metadata)
        payload.description = self.get_description(content_metadata)
        payload.id = self.get_id(content_metadata)
        payload.images = self.get_images(content_metadata)
        payload.instagram = self.get_instagram(content_metadata)
        payload.likes = self.get_likes(content_metadata)
        payload.banner_image = self.get_banner_image(content_metadata)
        payload.facebook = self.get_facebook_handle(content_metadata)
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
        payload.created_at = self.created_at
        payload.currency = self.get_currency(content_metadata)
        return payload

    def get_currency(self,content_metadata):
        if "currency" in content_metadata['brand']:
            return content_metadata['brand']['currency']
    def get_country_code(self,content_metadata):
        if "based_in" in content_metadata['brand']:
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
        try:
            category_json = requests_category.json()
            if "category_name" in category_json:
                category_name = category_json['category_name']
                return category_name
        except Exception:
            return None

        pass
    def get_description(self,content_metadata):
        description = content_metadata['brand']['description'].strip()
        description = description.replace('\n','')
        return description
        pass
    def get_city(self,content_metadata):
        if "based_in_city" in content_metadata['brand']:
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
        if "story_image" in content_metadata['brand']:
            story_image = content_metadata['brand']['story_image']
            images.append(story_image['url'])
        return images
        pass
    def get_instagram(self,content_metadata,counter=0):
        if "instagram_handle" in content_metadata['brand']:
            instagram = content_metadata['brand']['instagram_handle']
            search_data = self.API.searchUsername(instagram)
            instagram_json = self.API.LastJson
            try:
                user = instagram_json['user']
                instagram_dict = {
                    "Username": user['username'],
                    'FullName': user['full_name'],
                    'ProfilePic': user['hd_profile_pic_url_info']['url'],
                    'Bio': user['biography'].replace('\n',''),
                    'ExternalUrl': user['external_url'] if 'external_url' in user else None,
                    "Followers": user['follower_count'],
                    "Following": user['following_count'],
                    "PublicEmail": user['public_email'] if 'public_email' in user else None,
                }
                print(instagram_dict)
                return instagram_dict
            except KeyError:
                if counter == 0:
                    self.API = InstagramAPI(Private.USER2,Private.PASSWORD2)
                    self.API.login()
                    return self.get_instagram(content_metadata,counter=1)
                else:
                    raise Exception("Instagram key expired, add a new accoumt or wait until "
                    + self.regex_time.search(instagram_json['feedback_message']).group())
                
    def get_name(self,content_metadata):
        name = content_metadata['brand']['name']
        return name
        pass
    def get_likes(self,content_metadata):
        if "likes" in content_metadata['brand']:
            likes = content_metadata['brand']['likes']
            return likes
        pass
    def get_banner_image(self,content_metadata):
        banner_image = content_metadata['brand']['banner_image']['url']
        return banner_image
        pass
    def get_facebook_followers(self,content_metadata):
        if "facebook_followers" in content_metadata['brand']:
            facebook_followers = content_metadata['brand']['facebook_followers']
            return facebook_followers
        pass
    def get_facebook_handle(self,content_metadata):
        if "facebook_handle" in content_metadata['brand']:
            facebook_handle = content_metadata['brand']['facebook_handle']
            return facebook_handle
        pass
    def get_owner_name(self,content_metadata):
        if "owner_first_name" in content_metadata['brand']:
            brand = content_metadata['brand']
            first_name = brand['owner_first_name']
            last_name = brand['owner_last_name']
            owner_name = first_name + " " + last_name
            return owner_name
    def get_hand_made(self,content_metadata):
        if "hand_made" in content_metadata['brand']:
            hand_made = content_metadata['brand']['hand_made']
            return hand_made
    def get_made_in(self,content_metadata):
        if "made_in" in content_metadata['brand']:
            made_in = content_metadata['brand']['made_in']
            return made_in
    def get_social_media_images(self,content_metadata):
        social_media_images = []
        if "social_media_images" in content_metadata['brand']:
            for dict_ in content_metadata['brand']['social_media_images']:
                social_media_images.append(dict_['url'])
        return social_media_images
    def get_sold_on_amazon(self,content_metadata):
        if "sold_on_amazon" in content_metadata['brand']:
            sold_on_amazon = content_metadata['brand']['sold_on_amazon']
            return sold_on_amazon     
    def get_url(self,content_metadata):
        if 'url' in content_metadata['brand']:
            url = content_metadata['brand']['url']
            return url
        pass
    def get_twitter_followers(self,content_metadata):
        if "twitter_followers" in content_metadata['brand']:
            twitter_followers = content_metadata['brand']['twitter_followers']
            return twitter_followers
    def get_videos(self,content_metadata):
        if "video_url" in content_metadata['brand']:
            video_url = content_metadata['brand']['video_url']
            return video_url
        pass
    def get_average_rating(self,content_metadata):
        if "average_rating" in content_metadata['brand']:
            average_rating = content_metadata['brand']['average_rating']
            return average_rating
        pass
    def get_active_products_count(self,content_metadata):
        if "active_products_count" in content_metadata['brand']:
            active_products = content_metadata['brand']['active_products_count']
            return active_products
        pass
    def get_logo(self,content_metadata):
        if "logo_image" in content_metadata['brand']:
            logo_image = content_metadata['brand']['logo_image']['url']
            return logo_image
        pass
    def get_phone_number(self,content_metadata):
        pass
    def get_email(self,content_metadata):
        pass