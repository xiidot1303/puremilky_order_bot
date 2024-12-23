from app.services import *
from asgiref.sync import sync_to_async
from app.models import PriceType


async def update_price_types_using_data(data: list, region='samarkand'):
    new_price_types = []
    updated_price_types = []

    for item in data:
        existing_price_type = await PriceType.objects.filter(
            uuid=item['price_type_uuid'],
            product_uuid=item['product_uuid'],
            region=region
        ).afirst()
        price_type = PriceType(
            uuid=item['price_type_uuid'],
            product_uuid=item['product_uuid'],
            price=item['price'],
            region=region
        )
        if existing_price_type:
            existing_price_type.price = price_type.price
            updated_price_types.append(existing_price_type)
        else:
            new_price_types.append(price_type)

    # Create new price types if any
    if new_price_types:
        await PriceType.objects.abulk_create(new_price_types)

    # Update existing price types if any
    if updated_price_types:
        await sync_to_async(PriceType.objects.bulk_update)(updated_price_types, fields=['price'])
