from django.test import TestCase
# Import necessary packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import lxml

def extract_date(url,dates_to_get):
  
  iter_count = 0
  data_to_get={'date': None}
  all_keys =[]
  
  #while data_to_get['Date'] !=dates_to_get and iter_count <15:
  while all_keys !=dates_to_get and iter_count <15:
    
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")

    gdp = soup.find_all("table", attrs={"data-test":"historical-prices"})

    try:
        table1 = gdp[0]
    except IndexError as error:
        print(f'Index error in Extract Data with url: {url} \n\nReturning None to Data fetch!')
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
      data_to_get = df[df.Date.isin(dates_to_get)].to_dict(orient='records')
      # print(f' Try: data_to_get:{data_to_get}')
      all_keys = [ x['Date'] for x in data_to_get]
    except IndexError as error:
      pass
    iter_count+=1
  #print(f'Extracted Data {url}\n\n {data_to_get}')
  return data_to_get

#print(extract_date("https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD",'May 01 2021'))
#"https://finance.yahoo.com/quote/BTC-USD/"
