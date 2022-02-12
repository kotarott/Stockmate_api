import uuid as uuid_lib

from django.db import models
from core.models import TimeStampModel
from stocks.models import Symbol

# Create your models here.
class Portfolio(TimeStampModel):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description =models.TextField()
    image = models.ImageField(null=False, blank=False, upload_to='portfolios')

    def __str__(self):
        return self.name


class Feature(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    holdings = models.PositiveSmallIntegerField()
    change = models.FloatField()
    cap = models.BigIntegerField()
    peRatio = models.FloatField()
    opGrowth = models.FloatField()
    roe = models.FloatField()
    deRation = models.FloatField()
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.portfolio.name


class Transaction(TimeStampModel):
    slug = models.SlugField(max_length=225, unique=True)
    symbol = models.ForeignKey(Symbol, on_delete=models.PROTECT)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    position = models.CharField(max_length=3)
    quantity = model.PositiveIntegerField()
    totalCost = models.PositiveIntegerField()
    perCost = models.PositiveIntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.slug
