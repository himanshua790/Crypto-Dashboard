from django.test import TestCase
# Import necessary packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import lxml

def extract_date(url,date_to_get):
  iter_count = 0
  data_to_get={'Date':None}
  while data_to_get['Date'] !=date_to_get and iter_count <15:
    
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")

    gdp = soup.find_all("table", attrs={"data-test":"historical-prices"})

    try:
        table1 = gdp[0]
    except IndexError as error:
        print(url)
        return None
    body = table1.find_all("tr")

    head = body[0] 
    body_rows = body[1:]


    headings = []
    for item in head.find_all("th"): 
 
        item = (item.text).rstrip("\n")
        headings.append(item)

    all_rows = []
    for row_num in range(len(body_rows)): 
        row = []
        for row_item in body_rows[row_num].find_all("td"): 
           
            aa = re.sub("(\xa0)|(\n)|,","",row_item.text)

            row.append(aa)

        all_rows.append(row)
  
    df = pd.DataFrame(data=all_rows,columns=headings)


    try:
      data_to_get = df[df.Date.isin(date_to_get)].to_dict(orient='records')
    except IndexError as error:
      pass
    iter_count+=1
  return data_to_get

#print(extract_date("https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD",'May 01 2021'))
#"https://finance.yahoo.com/quote/BTC-USD/"

'''
%load_ext autoreload
%autoreload 2
from home.models import *
from home.models import Crypto_data as cd
from home. views import *
import datetime
from datetime import datetime as dt

 (dt.now(timezone.utc)-timedelta(days=10)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
'''