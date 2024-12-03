from app.services import *
from config import *
import base64

URL = ONE_C_URL


class ApiMethods:
    products = "products"
    categories = "categories"


class OneCRequest:
    def __init__(self, method: ApiMethods):
        # make credentials for base Distribution
        url = URL + f'/Distribution/hs/tg_bot/{method}'
        username = ONE_C_DISTRIBUTION_LOGIN
        password = ONE_C_DISTRIBUTION_PASSWORD
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(
            credentials.encode('utf-8')).decode('utf-8')
        # create auth by username and password
        basic_auth_token = f"Basic {encoded_credentials}"
        headers = {
            'Authorization': basic_auth_token,
            'Content-Type': 'application/json'
        }
        request_body = {
            "username": "tg_bot",
            "token": ONE_C_DISTRIBUTION_API_TOKEN,
            "version": "3.0.0"
        }
        self.url = url
        self.headers = headers
        self.body = request_body

    async def send(self):
        response = await send_request(
            self.url, self.body,
            self.headers, type='post'
        )
        return response['results'] if 'results' in response else response
