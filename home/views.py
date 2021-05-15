from django.http import HttpResponse
from django.shortcuts import render
import requests
from .models import Api_data

#List of Crypto Required
all_curr = ['bitcoin',"ethereum","litecoin","cardano","polkadot","dogecoin",'stellar',"chainlink","binance-coin","tether"]

def home(request):
    data = get_crypto_data()
    return render(request, "index.html", {'results':data})



# return the data received from api as json object
def get_crypto_data():
    data_list = []
    api_url = "https://api.coincap.io/v2/assets/"
    
    for curr in all_curr:
        try:
            data = requests.get(api_url+"/"+curr).json()
            data_list.append(data['data'])
        except Exception as e:
            print(e)
            data_list.append(data['data'])
    return data_list
