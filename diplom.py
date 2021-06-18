import requests
import time
import os.path
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

    @staticmethod
    def get_file_line(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            return f.readline().strip()

    @staticmethod
    def file_exist(file_path):
        return os.path.isfile(file_path)

    @staticmethod
    def show_error_non_exist_file(file_path, service_name=""):
        if os.path.dirname(file_path) != "":
            dir_name_text = " в директории " + os.path.dirname(file_path) + " относительно расположения файла-скрипта"
        else:
            dir_name_text = " в той же директории где находится файл-скрипт"

        print("Файл не найден. Пожалуйста, создайте файл " + os.path.basename(file_path) + dir_name_text
              + ", чтобы воспользоваться сервисом " + service_name)


class YandexDisc:
    YANDEX_UPLOAD_URI = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN_PATH = "tokens/yandex_disc.txt"

    def __init__(self):
        self.token = self.__get_token()

    def __get_token(self):
        if not FileHandler.file_exist(self.TOKEN_PATH):
            FileHandler.show_error_non_exist_file(self.TOKEN_PATH, "API Яндекс.Диск")
            raise SystemExit
        else:
            return FileHandler.get_file_line(self.TOKEN_PATH)

    def _get_headers(self):
        return {'Authorization': 'OAuth ' + self.token}

    def upload(self, download_url, upload_path, file_name):
        return requests.post(self.YANDEX_UPLOAD_URI + "/upload", headers=self._get_headers(),
                             params={'url': download_url, 'path': upload_path + file_name}).json()

    def get_request(self, url):
        return requests.get(url, headers=self._get_headers())

    #def show_upload_error(self, error_code, error_text):

    def upload_photos(self, photos_list, upload_path):
        likes_count = []
        for photo in photos_list:
            # pprint(photo)
            url = photo['sizes'][-1]['url']
            if photo['likes']['count'] in likes_count:
                name = str(photo['likes']['count']) + "_" + str(datetime.now()) + "." \
                       + FileHandler.get_file_type(url)
            else:
                name = str(photo['likes']['count']) + "." + FileHandler.get_file_type(url)
                likes_count.append(photo['likes']['count'])

            response = self.upload(url, upload_path, name)
            if 'error' in response:
                if response['error'] == 'DiskPathDoesntExistsError':
                    response_cd = self.create_dir(upload_path)
                    if 'error' in response_cd:
                        print(response_cd['message'])
                        continue
                    else:
                        response = self.upload(url, upload_path, name)
                else:
                    print(response['error'])
                    continue

            time.sleep(5)
            if self.success_upload(response['href']):
                FileHandler.add_log(name, photo['sizes'][-1]['type'], 'from_vk_to_ya_disc.json')

    def success_upload(self, response):
        return self.get_request(response).json()['status'] == 'success'

    def create_dir(self, dir_name):
        return requests.put(self.YANDEX_UPLOAD_URI, headers=self._get_headers(), params={'path': dir_name}).json()


class Vkontakte:
    ROOT_URI = "https://api.vk.com/method/"
    TOKEN_PATH = "tokens/vkontakte.txt"

    def __init__(self, api_version):
        self.token = self.__get_token()
        self.api_version = api_version
        self.params = {
            "access_token": self.token,
            "v": self.api_version,
        }

    def __get_token(self):
        if not FileHandler.file_exist(self.TOKEN_PATH):
            FileHandler.show_error_non_exist_file(self.TOKEN_PATH, "API Vkontakte")
            raise SystemExit
        else:
            return FileHandler.get_file_line(self.TOKEN_PATH)

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


vk = Vkontakte("5.131")
user_id = vk.get_user_id_by_user_code("id18452")
photos = vk.get_profile_photos(user_id)

disc = YandexDisc()
disc.upload_photos(photos, 'disk:/netology/')
