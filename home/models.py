from django.db import models
from django.db.models.base import Model

# Create your models here.
class Api_data(models.Model):
    crypto_id = models.CharField(max_length=50)
    rank = models.IntegerField()
    symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    supply = models.CharField(max_length=50)
    maxSupply = models.CharField(max_length=50)
    marketCapUsd = models.CharField(max_length=50)
    volumeUsd24Hr = models.CharField(max_length=50)
    priceUsd = models.CharField(max_length=50)
    changePercent24Hr = models.CharField(max_length=50)
    vwap24Hr = models.CharField(max_length=50)
    explorer = models.CharField(max_length=50)
    timestamp =models.CharField(max_length=50)

