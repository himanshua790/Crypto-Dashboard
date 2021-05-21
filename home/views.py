from django.http import HttpResponse
from django.shortcuts import render
import requests
from .models import Api_data

#List of Crypto Required
all_curr = ['bitcoin',"ethereum","litecoin","cardano","polkadot","dogecoin",'stellar',"chainlink","binance-coin","tether"]
test_curr=['bitcoin']

#API Url
api_url = "https://api.coincap.io/v2/assets/"

def home(request):
    data = get_crypto_data()
    print(data)
    return render(request, "index.html", {'results':data})

######################################################

# return the data received from api as json object
def get_crypto_data():
    data_list = []
    for currency in all_curr:
        try:
            data = requests.get(api_url+"/"+currency).json()
        except Exception as e:
            data={"error":f"exception occured in get_crypto_data {e}"}
            print(e)
            
        data_list.append(data['data'])
    print("this is data list ",data_list)
    return data_list


def dashboard(request,currency):
    e = None
    try:
        data = requests.get(api_url+str(currency)).json()
    except Exception as e:
        data={"error":f"exception occured in get_crypto_data {e}"}
        print(e)
    return render(request, "dashboard.html", {'data':data,'profile':currency,'error':e})