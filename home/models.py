from django.db import models as djmodel
from django.db.models.base import Model
from djongo import models
# Create your models here.


class Api_data(models.Model):
    crypto_id = models.CharField(max_length=50)
    rank = models.IntegerField()
    symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    supply = models.BigIntegerField()
    maxSupply =  models.BigIntegerField()
    marketCapUsd =  models.BigIntegerField()
    volumeUsd24Hr =  models.BigIntegerField()
    priceUsd = models.DecimalField(decimal_places=4,max_digits=20)
    changePercent24Hr = models.DecimalField(decimal_places=2,max_digits=20)
    vwap24Hr = models.DecimalField(decimal_places=2,max_digits=20)


class Crypto_data(models.Model):
    _id = models.ObjectIdField()
    Name = models.CharField(max_length=50)
    Date = models.DateTimeField()
    Close = models.DecimalField(decimal_places=4,max_digits=20)
    High = models.DecimalField(decimal_places=4,max_digits=20)
    Low = models.DecimalField(decimal_places=4,max_digits=20)
    Open = models.DecimalField(decimal_places=4,max_digits=20)
    Volume = models.BigIntegerField()