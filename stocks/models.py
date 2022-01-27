from django.db import models
from core.models import TimeStampModel
from profiles.models import Profile


class Symbol(TimeStampModel):
    slug = models.SlugField(max_length=225, unique=True)
    symbol = models.CharField(max_length=20, blank=False)
    description = models.CharField(max_length=100, blank=False)
    currency = models.CharField(max_length=10, blank=True)
    symbol_type = models.CharField(max_length=50, blank=True)
    exchange = models.CharField(max_length=100, blank=True)
    # mic = models.ForeignKey()
    vender = models.CharField(max_length=3, blank=False)
    voters = models.ManyToManyField(Profile, related_name="like")

    def __str__(self):
        return f'{self.symbol} of {self.vender}'