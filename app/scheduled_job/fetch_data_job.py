from app.utils import send_request
from app.services.product_service import update_products_using_data, update_categories_using_data
from app.services.client_service import update_clients_using_data
from app.services.price_type_service import update_price_types_using_data
from app.services.recommended_order_service import update_recommended_orders_using_data
from app.services.bonus_service import update_bonuses_using_data
from app.services.one_c_service import *


async def update_products():
    # get products data from one c
    request = OneCRequest(ApiMethods.products)
    products_list: dict = await request.send()

    # save data
    await update_products_using_data(products_list)

    # TASHKENT
    # get products data from one c
    request = OneCRequest(ApiMethods.products, region='tashkent')
    products_list: dict = await request.send()
    # save data
    await update_products_using_data(products_list, region='tashkent')


async def update_categories():
    # get categories data from one c
    request = OneCRequest(ApiMethods.categories)
    categories_list: dict = await request.send()

    # save data
    await update_categories_using_data(categories_list)

    # TASHKENT
    # get categories data from one c
    request = OneCRequest(ApiMethods.categories, region='tashkent')
    categories_list: dict = await request.send()

    # save data
    await update_categories_using_data(categories_list, region='tashkent')


async def update_clients():
    # get clients data from one c
    request = OneCRequest(ApiMethods.clients)
    clients_list: dict = await request.send()

    # save data
    await update_clients_using_data(clients_list)

    # TASHKENT
    # get clients data from one c
    request = OneCRequest(ApiMethods.clients, region='tashkent')
    clients_list: dict = await request.send()

    # save data
    await update_clients_using_data(clients_list, region='tashkent')


async def update_price_types():
    # get price types data from one c
    request = OneCRequest(ApiMethods.price_list)
    clients_list: dict = await request.send()

    # save data
    await update_price_types_using_data(clients_list)

    # TASHKENT
    # get price types data from one c
    request = OneCRequest(ApiMethods.price_list, region='tashkent')
    clients_list: dict = await request.send()

    # save data
    await update_price_types_using_data(clients_list, region='tashkent')


async def update_recommended_order():
    # get recommended orders from one c
    request = OneCRequest(ApiMethods.recommended_orders)
    recommended_orders: dict = await request.send()

    # save date
    await update_recommended_orders_using_data(recommended_orders)

    # TASHKENT
    # get recommended orders from one c
    request = OneCRequest(ApiMethods.recommended_orders, region='tashkent')
    recommended_orders: dict = await request.send()

    # save date
    await update_recommended_orders_using_data(recommended_orders, region='tashkent')


async def update_bonuses():
    # get recommended orders from one c
    request = OneCRequest(ApiMethods.product_bonus)
    bonuses: dict = await request.send()

    # save data
    await update_bonuses_using_data(bonuses)

    # TASHKENT
    # get recommended orders from one c
    request = OneCRequest(ApiMethods.product_bonus, region='tashkent')
    bonuses: dict = await request.send()

    # save data
    await update_bonuses_using_data(bonuses)