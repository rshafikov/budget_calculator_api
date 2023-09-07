import json
from variables import URL
import requests as r


class User:
    urls = {
        'auth': f'http://{URL}/auth/users/',
        'token': f'http://{URL}/auth/jwt/create/',
        'records': f'http://{URL}/records/',
        'total': f'http://{URL}/records/total-spend/',
        'categories': f'http://{URL}/categories/',
    }

    def __init__(self, update):
        self.headers = {'Content-Type': 'application/json'}
        self.id = update.effective_chat.id
        self.first_name = update.message.chat.first_name
        self.last_name = update.message.chat.last_name
        self.username = f'{self.first_name}_{self.last_name}'
        self.last_message = update.message.text
        self.last_summ = None
        self.last_category = None

    def get_auth(self):
        data = {
            'username': self.username,
            'password': f'{self.id}ZSe!1',
            'tg_id': f'{self.id}'
        }
        data = json.dumps(data)
        self.request_auth = r.post(
            url=self.urls['auth'],
            headers=self.headers,
            data=data
        )
        self.request_token = r.post(
            url=self.urls['token'],
            headers=self.headers,
            data=data
        )
        self.token = 'Bearer ' + self.request_token.json().get('access')
        self.headers.update({'Authorization': self.token})

    def make_record(self):
        if self.last_summ and self.last_category:
            data = {
                'category': self.last_category,
                'amount': str(self.last_summ)
            }
            data = json.dumps(data)
            self.request_record = r.post(
                url=self.urls['records'],
                headers=self.headers,
                data=data
            )

    def get_total(self):
        self.request_total = r.get(
            url=self.urls['total'],
            headers=self.headers,
        )

    def get_records_list(self):
        self.request_records_list = r.get(
            url=self.urls['records'],
            headers=self.headers,
        )

    def __str__(self):
        return f'{self.username} -- {self.last_category}: {self.last_summ}'
