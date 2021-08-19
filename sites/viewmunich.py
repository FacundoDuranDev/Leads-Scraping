import json
import requests
import yaml
import time
import re
from utils.mongo import Mongo
from utils.async_requests import _async_requests
from utils.payload import Payload
from utils.colors import colors
from bs4 import BeautifulSoup
from yaml.loader import SafeLoader

class ViewMunich:
    def __init__(self,config,type,site):
        self.config = config['Sites']
        self.url = self.config[site]['url']
        self.created_at = "2021-08-12" #time.strftime('%Y-%m-%d')
        self.site = site
        self.mongo = Mongo()
        self.test_mongo = Mongo('testing')
        self.session = requests.session()
        self.scraped = self.mongo.query_field(field='Id',site=self.site,created_at=self.created_at)

        self.email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        self.phone_regex = re.compile('(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]‌​)\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)([2-9]1[02-9]‌​|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})\s*(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+)\s*)?$')
        if type == "scraping":
            self._scraping()
        if type == "testing":
            self._scraping(testing=True)
    def get_ids(self):
        id_list = []
        for counter in range(1,6):
            api_request = requests.get(self.url.format(counter))
            html_api = api_request.text
            soup = BeautifulSoup(html_api,'html.parser')
            input_list = soup.findAll('input',{'type':'hidden'})
            for input_ in input_list:
                value = input_.get('value')
                if value not in id_list:
                    id_list.append(value)
        return id_list

    def request_ids(self,id_list):
        for id in id_list:
            api_request = requests.get('https://exhibitor.munichfabricstart.com/de/api/detailview/{}'.format(id))
            html_ = api_request.text
            soup_ = BeautifulSoup(html_,'html.parser')
            if id not in self.scraped:
                payload = self.get_payload(soup_,id)
                self.mongo.InsertOne(payload)            
    def _scraping(self,testing=False):
        id_list = self.get_ids()
        self.request_ids(id_list)
    def get_payload(self,content_metadata,id):
        payload = {}
        payload['Site'] = self.site
        payload['Name'] = self.get_name(content_metadata)
        payload['Description'] = self.get_description(content_metadata)
        payload['Address'] = self.get_address(content_metadata)
        payload['CountryCode'] = self.country_ # defined in get_adress
        payload['Id'] = id
        payload['Url'] = self.get_url(content_metadata) 
        payload['Logo'] = self.get_logo(content_metadata)
        payload['PhoneNumber']= self.get_phone_number(content_metadata) #
        payload['Email'] = self.get_email(content_metadata) #
        payload['CreatedAt'] = self.created_at
        payload['Collection']= self.get_collection(content_metadata)
        return payload
    
    def get_address(self,content_metadata):
        """
        Creates the global variable of country_ that contains the iso2 code of the country
        """
        break_lines = content_metadata.findAll('br')
        address = break_lines[0].next.replace('\n','').strip()
        country = break_lines[1].next.replace('\n','').strip()
        self.country_ = country[0:2]
        return [address,country]
    def get_collection(self,content_metadata):
        collection = []
        collection_list = content_metadata.findAll('table','collection-table')
        collection_name_list = content_metadata.findAll('div','row py-3')
        list_ = []
        image_list = []
        for name in collection_name_list:
            if name.find('h6'):
                list_.append(name.find('h6'))
            if name.find('img'):
                image_list.append(name.find('img').get('src'))

        for table_, name, image in zip(collection_list,list_,image_list):
            dict_ = {'name': name.text,
            "image":image}
            for value in table_:
                if value != "\n":
                    for row in value.findAll('tr'):
                        dict_[row.find('th').text] = row.find('td').text
            collection.append(dict_)
        return collection
    def get_description(self,content_metadata):
        description_state = content_metadata.find('p')
        if description_state:
            description = description_state.text.strip().replace('\n','')
            return description
        pass
    def get_name(self,content_metadata):
        name = content_metadata.find('b').text
        return name
        
    def get_url(self,content_metadata):
        links = content_metadata.findAll('a')
        urls = []
        for link in links:
            if not "@" in link.text:
                if link.text not in urls:
                    urls.append(link.text.strip())

        print(urls)
        return  urls

    def get_logo(self,content_metadata):
       
        logo_exists = content_metadata.find('img')
        if logo_exists:
            return logo_exists.get('src')
       
    def get_phone_number(self,content_metadata):
        table_ = content_metadata.find('table','contact-table')
        phone_numbers = []
        row_ = table_.findAll('tr')
        for row in row_:
            phone_number = row.findAll('td')[1].text
            if self.phone_regex.search(phone_number):
                phone_numbers.append(phone_number)
        print(phone_numbers)
        return phone_numbers

        pass
    def get_email(self,content_metadata):
        links = content_metadata.findAll('a')
        emails = []
        for link in links:
            data_ = link.text.strip()
            if "@" in data_:
                if data_ not in emails:
                    emails.append(data_)

        print(emails)
        return emails
        #kg@agenturkarengerke.de kg@agenturkarengerke.de