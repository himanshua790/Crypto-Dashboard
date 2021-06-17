from django.test import TestCase
# Import necessary packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import lxml
import datetime as dt
fmts = ('%Y', '%b %d %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y',
            '%m/%d/%Y', '%m/%d/%y', '%b %Y', '%B%Y', '%b %d,%Y',
            '%B-%d-%Y','%m-%d-%Y', '%m-%d-%y', '%b-%Y', '%B%Y', '%b-%d-%Y','%d-%b-%Y')

def check_datetime_format(value):
  
    for fmt in fmts:
        try:
            t = dt.datetime.strptime(value, fmt)
            print(f'Date format of {value} : {fmt}')
            return fmt
            break
        except ValueError as err:
            pass
    print(f'Value is not a Date!\nUnable to detect format for {value}')
    return None

def extract_date(url, dates_to_get):

    iter_count = 0
    data_to_get = {'date': None}
    all_keys = []

    # while data_to_get['Date'] !=dates_to_get and iter_count <15:
    while all_keys != dates_to_get and iter_count < 10:
        if all_keys != dates_to_get:
            print(f'All keys: {all_keys}\ndates to get: {dates_to_get}\n\n\n')
        print('iter_count:', iter_count)

        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, "lxml")

        gdp = soup.find_all("table", attrs={"data-test": "historical-prices"})

        try:
            table1 = gdp[0]
        except IndexError as error:
            print(
                f'Index error in Extract Data with url: {url} \n\nReturning None to Data fetch!')
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

                aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)

                row.append(aa)

            all_rows.append(row)
        #print("ALl ROWS \n", all_rows)
        df = pd.DataFrame(data=all_rows, columns=headings)

        try:
            data_to_get = df[df.Date.isin(dates_to_get)].to_dict(
                orient='records')
            #print(f' Try: data_to_get:{data_to_get}')
            all_keys = [x['Date'] for x in data_to_get]
        except IndexError as error:
            pass
        iter_count += 1
    print(f'Extracted Data {url}\n\n {data_to_get}')
    if len(all_keys) == 0:
        print(f'len of all_keys is zero! retrying fuction with new date format...')
        new_format = check_datetime_format(all_rows[0][0])
        current_format = check_datetime_format(dates_to_get[0])
        print(f'Current Date format is: {current_format}\nNew Date format is: {new_format}')
        # converting format of date:
        new_dates =[]
        for date in dates_to_get:
          datetimeobject = dt.datetime.strptime(date,current_format)
          new_dates.append(datetimeobject.strftime(new_format))
        print('Updated dates are:',new_dates)
        data_to_get = extract_date(url,new_dates)

        for i in range(len(data_to_get)):
          date = data_to_get[i]['Date']
          datetimeobject = dt.datetime.strptime(date,new_format)
          data_to_get[i]['Date'] = datetimeobject.strftime(current_format)

    return data_to_get
