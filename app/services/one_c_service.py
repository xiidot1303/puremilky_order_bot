from app.services import *
from config import *
import base64


class ApiMethods:
    products = "products"
    categories = "categories"
    clients = "clients"
    price_list = "price_list"
    act_sverki = "act_sverki_pdf"
    create_order = "post_orders"
    recommended_orders = "recommended_order"


class OneCRequest:
    def __init__(self, method: ApiMethods, params={}, region='samarkand'):
        # make credentials for base Distribution
        if region == 'samarkand':
            url = ONE_C_URL + f'/Distribution/hs/tg_bot/{method}'
            username = ONE_C_DISTRIBUTION_LOGIN
            password = ONE_C_DISTRIBUTION_PASSWORD
            credentials = f"{username}:{password}"
        elif region == 'tashkent':
            url = ONE_C_URL_TASHKENT + f'/Dist/hs/tg_bot/{method}'
            username = ONE_C_DISTRIBUTION_LOGIN_TASHKENT
            password = ONE_C_DISTRIBUTION_PASSWORD_TASHKENT
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
        request_body.update(params)
        self.url = url
        self.headers = headers
        self.body = request_body

    async def send(self):
        response = await send_request(
            self.url, self.body,
            self.headers, type='post'
        )
        return response['results'] if 'results' in response else response


async def get_act_sverki(client_uuid, start_period, end_period, region='samarkand'):
    params = {
        "client": client_uuid,
        "start_period": start_period,
        "end_period": end_period
    }
    request = OneCRequest(ApiMethods.act_sverki, params, region=region)
    return await request.send()


async def create_order_api(
    date_shipping: datetime, client_uuid: str, order_details: list, region='samarkand'
):
    """
    attr order_details: \n
    [
        {
            "product_uuid": product_uuid,
            "price": price,
            "quantity": count
        }
    ]

    """
    now: datetime = await datetime_now()
    params = {
        "results": [
            {
                "is_van": False,
                "date_shipping": date_shipping.strftime("%Y-%m-%d"),
                "date_creation": now.strftime("%Y-%m-%d"),
                "client_uuid": client_uuid,
                "date": date_shipping.strftime("%Y-%m-%d"),
                "comment": ".",
                "details": order_details
            }
        ]
    }
    request = OneCRequest(ApiMethods.create_order, params, region=region)
    return await request.send()
