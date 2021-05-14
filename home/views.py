from django.http import HttpResponse
from django.shortcuts import render
import requests


def home(request):
    data = {}
    data["crypto_data"] = get_crypto_data()
    return render(request, "index.html", data)


# return the data received from api as json object
def get_crypto_data():
    api_url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"

    try:
        data = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=10").json()
    except Exception as e:
        print(e)
        data = dict()
        temp_variable = data

    return data


