from django.db import models

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import (
post_save
)
User=settings.AUTH_USER_MODEL