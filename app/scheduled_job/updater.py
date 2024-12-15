from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduled_job import fetch_data_job, orders_job
from asgiref.sync import async_to_sync


class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')

    scheduler.add_job(async_to_sync(
        fetch_data_job.update_products), 'interval', minutes=5)
    scheduler.add_job(async_to_sync(
        fetch_data_job.update_products), 'interval', minutes=120)

    scheduler.add_job(async_to_sync(
        orders_job.publish_orders_to_one_c), 'interval', minutes=5)
