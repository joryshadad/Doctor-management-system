from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_welcome_email
from .models import Booking, Notification

User = get_user_model()


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """ترسل البريد وتنشئ إشعارًا ترحيبيًا بعد إنشاء حساب جديد."""
    if not created:
        return

    def after_commit():
        send_welcome_email(instance)
        Notification.objects.create(
            recipient=instance,
            message="مرحبًا بك في نظام إدارة العيادة.",
            link="/home/",
        )

    transaction.on_commit(after_commit)


@receiver(post_save, sender=Booking)
def booking_created(sender, instance, created, **kwargs):
    """تنشئ إشعارًا للمستخدم الذي أجرى حجزًا جديدًا."""
    if not created or not instance.created_by_id:
        return
    transaction.on_commit(
        lambda: Notification.objects.create(
            recipient=instance.created_by,
            message=f"تم إنشاء حجز جديد للمريض {instance.patient}.",
            link="/booking/",
        )
    )
