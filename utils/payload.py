from datetime import datetime


class Payload:
    def __init__(
        self,
        site=None,
        country_code=None,
        city=None,
        currency=None,
        _id=None,
        description=None,
        name=None,
        likes=None,
        banner_image=None,
        creation_year=None,
        instagram_followers=None,
        instagram=None,
        facebook_followers=None,
        facebook_handle=None,
        owner_name=None,
        hand_made=None,
        made_in=None,
        social_media_images=None,
        sold_on_amazon=None,
        url=None,
        twitter_followers=None,
        videos=None,
        images=None,
        average_rating=None,
        number_of_reviews=None,
        active_products_count=None,
        logo=None,
        category=None,
        phone_number=None,
        email=None,
        CreatedAt=None
                    ):
        self._site = site
        self._country_code = country_code
        self._city = city
        self._currency = currency
        self._id = _id
        self._description = description
        self._name = name
        self._likes = likes
        self._banner_image = banner_image
        self._creation_year = creation_year
        self._instagram_followers = instagram_followers
        self._instagram = instagram
        self._facebook_followers = facebook_followers
        self._facebook_handle = facebook_handle
        self._owner_name = owner_name
        self._hand_made = hand_made
        self._made_in = made_in
        self._social_media_images = social_media_images
        self._sold_on_amazon = sold_on_amazon
        self._url = url
        self._twitter_followers = twitter_followers
        self._videos = videos
        self._images = images
        self._average_rating = average_rating
        self._number_of_reviews = number_of_reviews
        self._active_products_count = active_products_count
        self._logo = logo
        self._category = category
        self._phone_number = phone_number
        self._email = email
        self._created_at = CreatedAt

    @property
    def country_code(self):
        return self._country_code
    
    @country_code.setter
    def country_code(self, new_country):
        self._country_code = new_country
    
    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, new_city):
        self._city = new_city
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id):
        self._id = new_id
    
    @property
    def currency(self):
        return self._currency
    
    @currency.setter
    def currency(self, new_currency):
        self._currency = new_currency
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, new_description):
        self._description = new_description
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def likes(self):
        return self._likes
    
    @likes.setter
    def likes(self, new_likes):
        self._likes = new_likes
    @property
    def banner_image(self):
        return self._banner_image
    
    @banner_image.setter
    def banner_image(self, new_banner_image):
        self._banner_image = new_banner_image
    @property
    def creation_year(self):
        return self._creation_year
    
    @creation_year.setter
    def creation_year(self, new_creation_year):
        self._creation_year = new_creation_year
    @property
    def instagram_followers(self):
        return self._instagram_followers
    
    @instagram_followers.setter
    def instagram_followers(self, new_instagram_followers):
        self._instagram_followers = new_instagram_followers
    @property
    def instagram(self):
        return self._instagram
    
    @instagram.setter
    def instagram(self, new_instagram):
        self._instagram = new_instagram
    @property
    def facebook_followers(self):
        return self._facebook_followers
    
    @facebook_followers.setter
    def facebook_followers(self, new_facebook_followers):
        self._facebook_followers = new_facebook_followers
    @property
    def owner_name(self):
        return self._owner_name
    
    @owner_name.setter
    def owner_name(self, new_owner_name):
        self._owner_name = new_owner_name
    @property
    def hand_made(self):
        return self._hand_made
    
    @hand_made.setter
    def hand_made(self, new_hand_made):
        self._hand_made = new_hand_made

    @property
    def made_in(self):
        return self._made_in
    
    @made_in.setter
    def made_in(self, new_made_in):
        self._made_in = new_made_in

    @property
    def social_media_images(self):
        return self._social_media_images
    
    @social_media_images.setter
    def social_media_images(self, new_social_media_images):
        self._social_media_images = new_social_media_images

    @property
    def sold_on_amazon(self):
        return self._sold_on_amazon
    
    @sold_on_amazon.setter
    def sold_on_amazon(self, new_sold_on_amazon):
        self._sold_on_amazon = new_sold_on_amazon

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, new_url):
        self._url = new_url

    @property
    def twitter_followers(self):
        return self._twitter_followers
    
    @twitter_followers.setter
    def twitter_followers(self, new_twitter_followers):
        self._twitter_followers = new_twitter_followers

    @property
    def videos(self):
        return self._videos
    
    @videos.setter
    def videos(self, new_videos):
        self._videos = new_videos

    @property
    def images(self):
        return self._images
    
    @images.setter
    def images(self, new_images):
        self._images = new_images

    @property
    def average_rating(self):
        return self._average_rating
    
    @average_rating.setter
    def average_rating(self, new_average_rating):
        self._average_rating = new_average_rating

    @property
    def number_of_reviews(self):
        return self._number_of_reviews
    
    @number_of_reviews.setter
    def number_of_reviews(self, new_number_of_reviews):
        self._number_of_reviews = new_number_of_reviews

    @property
    def active_products_count(self):
        return self._active_products_count
    
    @active_products_count.setter
    def active_products_count(self, new_active_products_count):
        self._active_products_count = new_active_products_count

    @property
    def logo(self):
        return self._logo
    
    @logo.setter
    def logo(self, new_logo):
        self._logo = new_logo

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        self._category = new_category

    @property
    def phone_number(self):
        return self._phone_number
    
    @phone_number.setter
    def phone_number(self, new_phone_number):
        self._phone_number = new_phone_number

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, new_email):
        self._email = new_email
    
    @property
    def facebook_handle(self):
        return self._facebook_handle
    
    @facebook_handle.setter
    def facebook_handle(self, new_facebook_handle):
        self._facebook_handle = new_facebook_handle

    @property
    def site(self):
        return self._site
    
    @site.setter
    def site(self, new_site):
        self._site = new_site

    @property
    def created_at(self):
        return self._created_at
    
    @created_at.setter
    def created_at(self, new_created_at):
        self._created_at = new_created_at
    def payload_dict(self):
        return{
        "Site":self._site,
        "CountryCode" : self._country_code,
        "City" : self._city,
        "Currency" : self._currency,
        "Id" : self._id,
        "Description" : self._description,
        "Name" : self._name,
        "Likes" : self._likes,
        "BannerImage" : self._banner_image,
        "CreationYear" : self._creation_year,
        "InstagramFollowers" : self._instagram_followers,
        "Instagram" : self._instagram,
        "FacebookFollowers" : self._facebook_followers,
        "FacebookHandle" : self._facebook_handle,
        "OwnerName" : self._owner_name,
        "HandMade" : self._hand_made,
        "MadeIn" : self._made_in,
        "SocialMediaImages" : self._social_media_images,
        "SoldOnAmazon" : self._sold_on_amazon,
        "Url" : self._url,
        "TwitterFollowers" : self._twitter_followers,
        "Videos" : self._videos,
        "Images" : self._images,
        "AverageRating" : self._average_rating,
        "NumberOfReviews" : self._number_of_reviews,
        "ActiveProductsCount" : self._active_products_count,
        "Logo" : self._logo,
        "Category" : self._category,
        "PhoneNumber" : self._phone_number,
        "Email" : self._email,
        'CreatedAt': self._created_at
        }