import json
import requests as r
from requests import Response
from variables import PASSWORD, URL, logging

logger = logging.getLogger(__name__)


class User:
    urls = {
        'auth': f'http://{URL}/auth/users/',
        'token': f'http://{URL}/auth/jwt/create/',
        'records': f'http://{URL}/records/',
        'currency': f'http://{URL}/users/my_currency/',
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
        self._currency = None
        self.is_authenticated = self.get_auth()

    def get_auth(self) -> bool:
        # TODO: fix case when User token is expired
        # TODO: add exception handling for every HTTP request

        data = json.dumps({
            'username': self.username,
            'password': f'{self.id}{PASSWORD}',
        })
        req = r.post(
            url=self.urls['auth'],
            headers=self.headers,
            data=data
        )
        if not hasattr(self, 'token'):
            request_token_resp = r.post(
                url=self.urls['token'],
                headers=self.headers,
                data=data
            )
            self.token = 'Bearer ' + request_token_resp.json().get('access')
            self.headers.update({'Authorization': self.token})
        return True

    @property
    def currency(self) -> str:
        if self._currency is None:
            self._currency = self.request_my_currency(
                ).json()['currency']
        return self._currency

    @currency.setter
    def currency(self, cur) -> None:
        data = self.request_my_currency(cur, 'POST').json()
        self._currency = data['currency']

    @property
    def categories(self) -> list:
        default_categories = ['NEW CATEGORY', '⚙️Меню']
        req = self.request_category()
        if hasattr(req, 'text'):
            return [*set(
                c['category_name'] for c in req.json())] + default_categories
        return default_categories

    def request_my_currency(
            self, currency=None, method: str = 'GET') -> Response:
        data = None
        if method == 'POST' and currency:
            data = json.dumps({
                'currency': currency
            })
        req = r.request(
            url=self.urls['currency'],
            method=method,
            headers=self.headers,
            data=data)
        return req

    def request_make_record(self) -> Response:
        if self.last_summ and self.last_category:
            data = json.dumps({
                'category': self.last_category,
                'amount': str(self.last_summ)
            })
            req = r.post(
                url=self.urls['records'],
                headers=self.headers,
                data=data
            )
            return req

    def request_category(
        self,
        category_name: str = None,
        action: str = None
    ) -> Response:
        if not category_name:
            return r.get(
                url=self.urls['categories'],
                headers=self.headers,
            )
        else:
            data = json.dumps({
                'category_name': category_name,
            })
            if action == 'POST':
                return r.post(
                    url=self.urls['categories'],
                    headers=self.headers,
                    data=data
                )
            elif action == 'PATCH':
                pass
            elif action == 'DELETE':
                pass

    def request_get_total(self, period) -> Response:
        return r.get(
            url=self.urls['total'] + period,
            headers=self.headers,
        )

    def request_get_records_list(self) -> Response:
        return r.get(
            url=self.urls['records'],
            headers=self.headers,
        )

    # def __str__(self):
    #     return f'{self.username} -- {self.last_category}: {self.last_summ}'
