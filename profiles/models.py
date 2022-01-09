import uuid as uuid_lib

from django.db import models
from django.conf import settings
from core.models import TimeStampModel


# Create your models here.
class Profile(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.user.username


class FavoStock(TimeStampModel):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
    symbol = models.CharField(max_length=20, blank=False)
    isin = models.CharField(max_length=12, blank=True)
    is_fmp = models.BooleanField(default=False)
    is_eod = models.BooleanField(default=False)
    is_fh = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.symbol