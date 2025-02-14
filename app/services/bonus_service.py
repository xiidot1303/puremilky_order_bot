from app.services import *
from app.models import Bonus, Product, Client


async def update_bonuses_using_data(data: dict):
    new_bonuses = []
    updated_bonuses = []

    product_uuids = {item["product_uuid"] for item in data}
    client_uuids = {item["client_uuid"] for item in data}

    existing_products = await sync_to_async(
        lambda: {str(p.uuid): p for p in Product.objects.filter(uuid__in=product_uuids)})()
    existing_clients = await sync_to_async(
        lambda: {str(c.uuid): c for c in Client.objects.filter(uuid__in=client_uuids)})()

    for item in data:
        existing_bonus = await Bonus.objects.filter(
            product__uuid=item["product_uuid"],
            client__uuid=item["client_uuid"],
        ).afirst()
        try:
            bonus = Bonus(
                product=existing_products[item["product_uuid"]],
                client=existing_clients[item["client_uuid"]],
                price=item["price"],
                available_free=item["available_free"],
                condition_no_less=item["condition_no_less"],
                percentage_amount=item["percentage_amount"],
                condition_no_less2=item["condition_no_less2"],
                percentage_amount2=item["percentage_amount2"],
                condition_no_less3=item["condition_no_less3"],
                percentage_amount3=item["percentage_amount3"],
                condition_no_less4=item["condition_no_less4"],
                percentage_amount4=item["percentage_amount4"],
                type_bonus=item["type_bonus"]
            )
        except:
            continue
        if existing_bonus:
            bonus.price = item["price"]
            bonus.available_free = item["available_free"]
            bonus.condition_no_less = item["condition_no_less"]
            bonus.percentage_amount = item["percentage_amount"]
            bonus.condition_no_less2 = item["condition_no_less2"]
            bonus.percentage_amount2 = item["percentage_amount2"]
            bonus.condition_no_less3 = item["condition_no_less3"]
            bonus.percentage_amount3 = item["percentage_amount3"]
            bonus.condition_no_less4 = item["condition_no_less4"]
            bonus.percentage_amount4 = item["percentage_amount4"]
            bonus.type_bonus = item["type_bonus"]
            updated_bonuses.append(existing_bonus)
        else:
            new_bonuses.append(bonus)

    # create objects
    if new_bonuses:
        await Bonus.objects.abulk_create(new_bonuses)
    else:
        await sync_to_async(Bonus.objects.bulk_update)(updated_bonuses, fields=[
            "price",
            "available_free",
            "condition_no_less",
            "percentage_amount",
            "condition_no_less2",
            "percentage_amount2",
            "condition_no_less3",
            "percentage_amount3",
            "condition_no_less4",
            "percentage_amount4",
            "type_bonus",
        ])
