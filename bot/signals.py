from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from bot.models import Bot_user
from bot.services.redis_service import set_user_lang
from bot.control.updater import application
from asgiref.sync import async_to_sync
from bot.services.newsletter_service import send_alert_about_activation_notify


@receiver(post_save, sender=Bot_user)
def save_bot_user_lang_to_redis(sender, instance: Bot_user, created, **kwargs):
    """
    Save the 'lang' of a bot user in Redis when a new user is created
    """
    if created:
        if instance.user_id is not None:
            set_user_lang(instance.user_id, instance.lang)


@receiver(pre_save, sender=Bot_user)
def handle_lang_change(sender, instance: Bot_user, **kwargs):
    """
    Handle changes to the 'lang' field specifically and update Redis.
    """
    if instance.pk and 'lang' in instance.__dict__:  # Check if the instance already exists
        try:
            original_instance = Bot_user.objects.get(pk=instance.pk)
            if original_instance.lang != instance.lang:
                set_user_lang(instance.user_id, instance.lang)

        except Bot_user.DoesNotExist:
            # If the instance does not exist in the database yet, do nothing
            pass


@receiver(post_save, sender=Bot_user)
def notify_user_on_status_change(sender, instance, **kwargs):
    if 'is_active' in instance.__dict__:
        instance: Bot_user
        user_id = instance.user_id
        if instance.is_active:
            # send notification
            async_to_sync(
                application.job_queue.run_once(send_alert_about_activation_notify, when=0, user_id=user_id)
            )
