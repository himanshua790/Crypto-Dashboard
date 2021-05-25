
from django.db.models import query
import requests, datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .models import Api_data, Crypto_data
from .forms import ContactForm
import datetime
from datetime import date, timedelta, timezone
from datetime import datetime as dt
from .tests import extract_date
def yesterday():
    yesterday = (dt.strptime(str(dt.today().date()), '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)-datetime.timedelta(days=1)).isoformat()
    return yesterday
def compare(x,y):
    return float("{:.2f}".format((x-y)/x))

#List of Crypto Required
all_curr = ['bitcoin',"ethereum","litecoin","cardano","polkadot","dogecoin",'stellar',"chainlink","binance-coin","tether"]
test_curr=['bitcoin']
Curr_urls= {
  "bitcoin": "https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD",
  "ethereum" : "https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD",
  "litecoin": "https://finance.yahoo.com/quote/LTC-USD/history?p=LTC-USD",
  "cardano": "https://finance.yahoo.com/quote/ADA-USD/history?p=ADA-USD",
  "polkadot": "https://finance.yahoo.com/quote/DOT1-USD/history?p=DOT1-USD",
  "dogecoin": "https://in.finance.yahoo.com/quote/DOGE-INR/history?p=DOGE-INR",
  "stellar": "https://finance.yahoo.com/quote/XLM-USD/history?p=XLM-USD",
  "chainlink": "https://finance.yahoo.com/quote/LINK-USD/history?p=LINK-USD",
  "binance-coin": "https://finance.yahoo.com/quote/BNB-USD/history?p=BNB-USD",
  "tether": "https://finance.yahoo.com/quote/USDT-USD/history?p=USDT-USD"
}

#API Url
api_url = "https://api.coincap.io/v2/assets/"

def home(request):
    data = get_crypto_data()
    print(data)
    return render(request, "index.html", {'results':data})

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'full_name': form.cleaned_data['full_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("home")
      
	form = ContactForm()
	return render(request, "contact.html", {'form':form})

def about(request):
    return render(request, "about.html")

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
    e ,f = None, None

    changePercent24Hr = None
    try:
        data = requests.get(api_url+str(currency)).json()
    except Exception as e:
        data={"error":f"exception occured in API Requests {e}"}
        print(e)
    
    try:
        query = Crypto_data.objects.filter(Name = str(currency),Date = yesterday()).order_by('-Date').values()[0]
        print(f'query is:{query["Volume"]}')
        changePercent24Hr = compare(float(data['data']['volumeUsd24Hr']),float(query['Volume']))
    except Exception as f:
        print(f'query except triggered for {f}')
        query = None
    return render(request, "dashboard.html", {'data':data["data"],'query':query,'profile':currency,'error':e,'changePercent24Hr':changePercent24Hr})

def check_updates(request):
    for currency in all_curr:
        give_query(currency)

    return render(request,'test.html')

def give_query(currency,delta =0):
    day = iso_date(delta)
    try:
        query = Crypto_data.objects.filter(Name = str(currency),Date = day)
        if not query.exists():
            raise ValueError ('Query Not found')
        print('data found')
    except Exception as f:
        print(f'query except triggered for {f}')
        query = None
    print(f' Query:{query}')
    return query

def iso_date(delta=0):
    return (dt.now(timezone.utc)-timedelta(days=delta)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

def simp_date(delta =0):
    datetime_obj = dt.today() - timedelta(days= delta)
    return dt.strftime(datetime_obj,'%b %d %Y')

def dates_to_update(currency):
    last_date = Crypto_data.objects.filter(Name = str(currency)).order_by('-Date').values()[0]['Date']
    date_diff = ((dt.now(timezone.utc)).replace(hour=0, minute=0, second=0, microsecond=0)- last_date).days
    dates = []
    for i in range(1,date_diff+1):
        dates.append(simp_date(i))
    return dates
