from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SiteUser, SiteWallet
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        SiteWallet.objects.create(owner=instance)