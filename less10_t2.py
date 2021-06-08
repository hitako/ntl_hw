import requests
from pprint import pprint


class YaUploader:
    YANDEX_UPLOAD_URI = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    TOKEN = "AQAAAAAzwg35AADLW50m66lrHEHBkBeQdKNSuhQ"

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _get_headers(self):
        return {'Authorization': 'OAuth ' + self.TOKEN}

    @staticmethod
    def _get_params(path):
        return {'path': path, 'overwrite': True}

    def _get_uploaded_path(self):
        return requests.get(self.YANDEX_UPLOAD_URI, headers=self._get_headers(),
                            params=self._get_params('text.txt')).json()['href']

    def upload(self):
        request = requests.put(self._get_uploaded_path(), data={'files': open(self.file_path, 'rb')})
        if request.status_code == 201:
            print("Файл успешно загружен")


uploader = YaUploader('C:\\Users\\g0dik\\PycharmProjects\\pythonProject\\text.txt')
uploader.upload()
