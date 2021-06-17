
from django.db.models import query
import requests
import datetime

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
    yesterday = (dt.strptime(str(dt.today().date()), '%Y-%m-%d').replace(
        tzinfo=datetime.timezone.utc)-datetime.timedelta(days=1)).isoformat()
    return yesterday


def compare(x, y):
    return float("{:.2f}".format((x-y)/x))


# List of Crypto Required
all_curr = ['bitcoin', "ethereum", "litecoin", "cardano", "polkadot",
            "dogecoin", 'stellar', "chainlink", "binance-coin", "tether"]
test_curr = ['bitcoin']
Curr_urls = {
    "bitcoin": "https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD",
    "ethereum": "https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD",
    "litecoin": "https://finance.yahoo.com/quote/LTC-USD/history?p=LTC-USD",
    "cardano": "https://finance.yahoo.com/quote/ADA-USD/history?p=ADA-USD",
    "polkadot": "https://finance.yahoo.com/quote/DOT1-USD/history?p=DOT1-USD",
    "dogecoin": "https://in.finance.yahoo.com/quote/DOGE-USD/history?p=DOGE-USD",
    "stellar": "https://finance.yahoo.com/quote/XLM-USD/history?p=XLM-USD",
    "chainlink": "https://finance.yahoo.com/quote/LINK-USD/history?p=LINK-USD",
    "binance-coin": "https://finance.yahoo.com/quote/BNB-USD/history?p=BNB-USD",
    "tether": "https://finance.yahoo.com/quote/USDT-USD/history?p=USDT-USD"
}

# API Url
api_url = "https://api.coincap.io/v2/assets/"


def home(request):
    data = get_crypto_data()
    print(data)
    return render(request, "index.html", {'results': data})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com',
                          ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("home")

    form = ContactForm()
    return render(request, "contact.html", {'form': form})


def about(request):
    return render(request, "about.html")


def get_crypto_data():
    data_list = []
    for currency in all_curr:
        try:
            data = requests.get(api_url+"/"+currency).json()
        except Exception as e:
            data = {"error": f"exception occured in get_crypto_data {e}"}
            print(e)

        data_list.append(data['data'])
    print("this is data list ", data_list)
    return data_list


def dashboard(request, currency):
    e, f = None, None

    changePercent24Hr = None
    try:
        data = requests.get(api_url+str(currency)).json()
    except Exception as e:
        data = {"error": f"exception occured in API Requests {e}"}
        print(e)

    try:
        query = Crypto_data.objects.filter(
            Name=str(currency), Date=yesterday()).order_by('-Date').values()[0]
        print(f'query is:{query["Volume"]}')
        changePercent24Hr = compare(
            float(data['data']['volumeUsd24Hr']), float(query['Volume']))
    except Exception as f:
        print(f'query except triggered for {f}')
        query = None
    return render(request, "dashboard.html", {'data': data["data"], 'query': query, 'profile': currency, 'error': e, 'changePercent24Hr': changePercent24Hr})


def check_updates(request):
    operation_logs=[]
    for currency in all_curr:
        #query = give_query(currency)

        dates = dates_to_update(currency)
        if len(dates) >=1: 
            final_data = extract_date(Curr_urls[currency], dates)

            print(f'Data Updated on {currency}\n\n', final_data)
            try:
                list_to_model_update(Crypto_data, final_data, currency)
                query = f'Data Updated! {currency} \n'
            except Exception as e:
                print(f'Unable to update data for {currency} \n',e)
                query = f'Unable to update data for {currency} \n' +e

        else:
            print('Data is already up to date')
            query = 'Data is already up to date!'

        operation_logs.append(query)
    return render(request, 'test.html', {'query': operation_logs})


def give_query(currency, delta=0):
    day = iso_date(delta)
    try:
        query = Crypto_data.objects.filter(Name=str(currency), Date=day)
        if not query.exists():
            raise ValueError('Query Not found')
        print('data found')
    except Exception as f:
        print(f'query except triggered for {f}')
        query = None
    print(f' Query:{query}')
    return query


def iso_date(delta=0):
    return (dt.now(timezone.utc)-timedelta(days=delta)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()


def simp_date(delta=0):
    datetime_obj = dt.today() - timedelta(days=delta)
    return dt.strftime(datetime_obj, '%b %d %Y')


def dates_to_update(currency):
    last_date = Crypto_data.objects.filter(
        Name=str(currency)).order_by('-Date').values()[0]['Date']
    date_diff = ((dt.now(timezone.utc)).replace(
        hour=0, minute=0, second=0, microsecond=0) - last_date).days
    dates = []
    if date_diff ==1:
        return []
    for i in range(1, date_diff+1):
        dates.append(simp_date(i))
    # print('date_to_update',dates)
    return dates


def list_to_model_update(model, data_list, name):
    for obj in data_list:
        Crypto_data.objects.create(
            Name=name,
            Date=date_to_iso_date(obj['Date']),
            Close=obj['Close*'],
            High=obj['High'],
            Low=obj['Low'],
            Open=obj['Open'],
            Volume=obj['Volume']
        )
    #print(f'Updated data to {name}')
def date_to_iso_date(date):
    return dt.strptime(date, '%b %d %Y').replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
