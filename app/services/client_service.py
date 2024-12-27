from app.models import Client
from bot.models import Bot_user
from asgiref.sync import sync_to_async


async def get_client_by_uuid(uuid):
    obj = await Client.objects.filter(uuid=uuid).afirst()
    return obj


async def get_bot_user_of_client(client: Client) -> Bot_user:
    obj = await Bot_user.objects.filter(client=client).afirst()
    return obj


async def update_clients_using_data(data: dict, region='samarkand'):
    new_clients = []
    updated_clients = []
    for item in data:
        if not item['isAgent'] and item['price_type_uuid'] != "00000000-0000-0000-0000-000000000000":
            existing_client = await Client.objects.filter(uuid=item['uuid']).afirst()

            client = Client(
                uuid=item['uuid'],
                name=item['name'],
                address=item['address'],
                inn=item['inn'],
                branch_uuid=item['branch_uuid'],
                price_type_uuid=item['price_type_uuid'],
                days_of_the_week=item['days_of_the_week'],
                phone=item['phone'],
                debt=item['debt'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                date_last_visit=item['date_last_visit'],
                region=region
            )

            if existing_client:
                existing_client.name = client.name
                existing_client.address = client.address
                existing_client.inn = client.inn
                existing_client.branch_uuid = client.branch_uuid
                existing_client.price_type_uuid = client.price_type_uuid
                existing_client.days_of_the_week = client.days_of_the_week
                existing_client.phone = client.phone
                existing_client.debt = client.debt
                existing_client.latitude = client.latitude
                existing_client.longitude = client.longitude
                existing_client.date_last_visit = client.date_last_visit
                existing_client.region = client.region
                updated_clients.append(existing_client)
            else:
                new_clients.append(client)

    # create objects
    if new_clients:
        for r in range(0, len(new_clients), 500):
            await Client.objects.abulk_create(new_clients[r:r+500])
    else:
        for r in range(0, len(updated_clients), 500):
            await sync_to_async(Client.objects.bulk_update)(
                updated_clients[r:r+500],
                fields=[
                    'name', 'address', 'inn', 'branch_uuid',
                    'price_type_uuid', 'days_of_the_week', 'phone',
                    'debt', 'latitude', 'longitude', 'date_last_visit', 'region'
                ])
