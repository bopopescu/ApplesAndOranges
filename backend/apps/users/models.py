# CPatrick Zhang 
# All Rights Reserved
import os, hashlib, random
from datetime import datetime, date
from decimal import Decimal, ROUND_DOWN
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.functional import cached_property
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres.fields import HStoreField
from django.conf import settings
from django.contrib.auth import get_user_model
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill
from _commons.models.mixins import CreationModificationMixin
from _commons import utils
from _commons.datetime import calculate_age
from _commons.notifications import PushNotification

# Solution to avoid unique_together for email
AbstractUser._meta.get_field('email')._unique = True


class AppUser(AbstractUser):
    """
    Custom user model for the application
    blank=True means Empty values allowed from the backend, if blank=False, then the field will be required in backend

    """

    _ROLE = (('V', 'Venue'), ('S', 'Show'), )

    role = models.CharField(max_length=1,
                              blank=True,
                              null=True,
                              choices=_SEX)
    is_email_verified = models.BooleanField(verbose_name='email verified', 
                                            help_text='Designates whether this user has verified email',
                                            default=False)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username',
                       'phone']
    CUSTOM_FIELDS = ('role', 'address1', 'address2', 'city', 'state', 'zip_code', 'country')

    # for serializer hack
    READ_ONLY_FIELDS = ('')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    @property
    def full_name(self):
        return "{} {}".format(self.first_name.capitalize(),
                              self.last_name.capitalize())


# ----------------------------------------------------------------------------------------------------------------------
# Signals
# ----------------------------------------------------------------------------------------------------------------------


@receiver(pre_save, sender=AppUser)
def new_user_created(sender, instance, *args, **kwargs):
    """
    Sets new phone code and email code and SMS / Emails them
    """
    if instance.is_superuser:
        return

    if instance.is_superuser:
        return
    if not instance.id:
        '''
        instance.is_email_verified = False means user needs to verified their email before login.
        instance.is_active = True means user by default is active(not suspended).
        '''
        instance.is_email_verified = False
        instance.is_active = True
