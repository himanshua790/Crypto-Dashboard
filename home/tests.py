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
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse HTML code for the entire site
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html

    gdp = soup.find_all("table", attrs={"data-test":"historical-prices"})
    #data-test="historical-prices"
    #print("Number of tables on site: ",len(gdp))

    # Lets go ahead and scrape first table with HTML code gdp[0]
    try:
        table1 = gdp[0]
    except IndexError as error:
        print(url)
        return None
    body = table1.find_all("tr")
    # Head values (Column names) are the first items of the body list
    head = body[0] # 0th item is the header row
    body_rows = body[1:] # All other items becomes the rest of the rows

    # Lets now iterate through the head HTML code and make list of clean headings

    # Declare empty list to keep Columns names
    headings = []
    for item in head.find_all("th"): # loop through all th elements
        # convert the th elements to text and strip "\n"
        item = (item.text).rstrip("\n")
        # append the clean column name to headings
        headings.append(item)

    all_rows = [] # will be a list for list for all rows
    for row_num in range(len(body_rows)): # A row at a time
        row = [] # this will old entries for one row
        for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
            # row_item.text removes the tags from the entries
            # the following regex is to remove \xa0 and \n and comma from row_item.text
            # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
            aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
            #append aa to row - note one row entry is being appended
            row.append(aa)
        # append one row to all_rows
        all_rows.append(row)
    # We can now use the data on all_rowsa and headings to make a table
    # all_rows becomes our data and headings the column names
    df = pd.DataFrame(data=all_rows,columns=headings)
    # return df[df.Date == 'May 20 2021'].to_dict(orient='records')
    try:
      data_to_get = df[df.Date == str(date_to_get)].to_dict(orient='records')[0]
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