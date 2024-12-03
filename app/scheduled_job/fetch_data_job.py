from app.utils import send_request
from app.services.product_service import update_products_using_data, update_categories_using_data
from app.services.one_c_service import *


async def update_products():
    # get products data from one c
    request = OneCRequest(ApiMethods.products)
    products_list: dict = await request.send()

    # save data
    await update_products_using_data(products_list)


async def update_categories():
    # get categories data from one c
    request = OneCRequest(ApiMethods.categories)
    categories_list: dict = await request.send()

    # save data
    await update_categories_using_data(categories_list)
