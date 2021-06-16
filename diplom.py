import requests
import time
import json
from datetime import datetime
from pprint import pprint


class FileHandler:
    @staticmethod
    def add_log(file_name, file_size, log_file_path):
        with open(log_file_path, 'a+') as f:
            f.write(str({
                'upload_date': str(datetime.now()),
                'file_name': file_name,
                'file_size': file_size,
            }))
            f.write('\n')

    @staticmethod
    def get_file_type(url):
        return url[:url.find('?')].split('.')[-1]


class YandexDisc:
    YANDEX_UPLOAD_URI = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    TOKEN = "" # ЗДЕСЬ НУЖНО ЗАДАТЬ OAuth ТОКЕН ЯНДЕКС.ДИСКа

    def _get_headers(self):
        return {'Authorization': 'OAuth ' + self.TOKEN}

    def upload(self, download_url, upload_path, file_name):
        return requests.post(self.YANDEX_UPLOAD_URI, headers=self._get_headers(),
                             params={'url': download_url, 'path': upload_path + file_name}).json()

    def get_request(self, url):
        return requests.get(url, headers=self._get_headers())

    def upload_photos(self, photos_list, upload_path):
        likes_count = []
        for photo in photos_list:
            #pprint(photo)
            url = photo['sizes'][-1]['url']
            if photo['likes']['count'] in likes_count:
                name = str(photo['likes']['count']) + "_" + str(datetime.now()) + "." \
                       + FileHandler.get_file_type(url)
            else:
                name = str(photo['likes']['count']) + "." + FileHandler.get_file_type(url)
                likes_count.append(photo['likes']['count'])

            response = self.upload(url, upload_path, name)
            time.sleep(5)
            if self.success_upload(response):
                FileHandler.add_log(name, photo['sizes'][-1]['type'], 'from_vk_to_yadisc.json')

    def success_upload(self, response):
        return self.get_request(response['href']).json()['status'] == 'success'


class Vkontakte:
    ROOT_URI = "https://api.vk.com/method/"

    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version
        self.params = {
            "access_token": self.token,
            "v": self.api_version,
        }

    def __set_params(self, params):
        return {**params, **self.params}

    def get_user_id_by_user_code(self, code):
        params = {
            "user_ids": code
        }
        params = self.__set_params(params)

        return requests.get(self.ROOT_URI + "users.get", params=params).json()['response'][0]['id']

    def get_profile_photos(self, owner_id, count=5):
        params = {
            "extended": 1,
            "owner_id": owner_id,
            "album_id": "profile",
            "count": count,
        }
        params = self.__set_params(params)
        return requests.get(self.ROOT_URI + "photos.get", params=params).json()['response']['items']


vk = Vkontakte("958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008", "5.131")
user_id = vk.get_user_id_by_user_code("id18452")
photos = vk.get_profile_photos(user_id)

disc = YandexDisc()
disc.upload_photos(photos, 'disk:/netology/')
