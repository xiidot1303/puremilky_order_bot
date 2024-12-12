from app.models import Product, Category, PriceType
from asgiref.sync import sync_to_async
from django.db.models import OuterRef, Subquery


@sync_to_async
def filter_products_by_category_and_by_client(category_id, price_type_uuid):
    query = Product.objects.filter(remainder__gt = 0, category__id=category_id).annotate(
        price_for_client=Subquery(
            PriceType.objects.filter(
                product_uuid=OuterRef('uuid'),
                uuid=price_type_uuid
            ).values('price')[:1]
        )
    )
    return query


@sync_to_async
def filter_products_by_title(title, price_type_uuid):
    query = Product.objects.filter(remainder__gt = 0, title__icontains=title).annotate(
        price_for_client=Subquery(
            PriceType.objects.filter(
                product_uuid=OuterRef('uuid'),
                uuid=price_type_uuid
            ).values('price')[:1]
        )
    )
    return query


async def update_categories_using_data(data: dict):
    new_categories = []
    updated_categories = []
    for item in data:
        if item['show_in_tgbot']:
            existing_category = await Category.objects.filter(uuid=item['uuid']).afirst()

            category = Category(
                uuid=item['uuid'],
                title=item['name']
            )

            if existing_category:
                existing_category.title = category.title
                updated_categories.append(existing_category)
            else:
                new_categories.append(category)

    # create objects
    if new_categories:
        await Category.objects.abulk_create(new_categories)
    else:
        await sync_to_async(Product.objects.bulk_update)(updated_categories, fields=['title'])


async def update_products_using_data(data: dict):
    # Prepare for region and category uuid
    region = "samarkand"
    # List to store new and updated Product objects
    new_products = []
    updated_products = []

    # Loop over results in the API response
    for item in data:
        try:
            category = await Category.objects.aget(uuid=item['category_uuid'])
        except Exception as ex:
            continue

        # Check if the product with the same uuid exists
        existing_product = await Product.objects.filter(uuid=item['uuid']).afirst()

        product = Product(
            uuid=item['uuid'],
            region=region,
            category=category,
            title=item['name'],
            measurement=item['measurement'],
            weight=item['weight'],
            quantity_per_pack=item['quantity_per_pack'],
            price=item['price'],
            remainder=item['remainder']
        )

        if existing_product:
            # Update the fields if the product already exists
            # existing_product.region = product.region
            # existing_product.category = product.category
            existing_product.title = product.title
            existing_product.measurement = product.measurement
            existing_product.weight = product.weight
            existing_product.quantity_per_pack = product.quantity_per_pack
            existing_product.price = product.price
            existing_product.remainder = product.remainder
            updated_products.append(existing_product)
        else:
            # Add the new product to the new_products list
            new_products.append(product)

    # create objects
    if new_products:
        await Product.objects.abulk_create(new_products)
    if updated_products:
        await sync_to_async(Product.objects.bulk_update)(updated_products, fields=[
            'region', 'category', 'title', 'measurement', 'weight',
            'quantity_per_pack', 'price', 'remainder'
        ])
