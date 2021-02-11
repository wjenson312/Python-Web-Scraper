from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from StockList import list_tickers
import datetime
import re

reactid_prices = 183
date_number = 1
dates = []
earnings_close = []
earnings_close_before = []
change = []
percent_change = []

for ticker in list_tickers:

    url_yahoo = "https://finance.yahoo.com/quote/" + ticker + "/analysis?p=" + ticker
    client_yahoo = uReq(url_yahoo)
    page_yahoo = client_yahoo.read()
    soup_yahoo = BeautifulSoup(page_yahoo, "html.parser")

    for i in range(4):
        reactid_prices = str(reactid_prices)
        date = soup_yahoo.find("th", {"data-reactid": reactid_prices})
        if date is None:
            if(i == 3):
                dates.append("Invalid Date")
        elif date.get_text() == "Invalid Date":
            if(i == 3):
                dates.append("Invalid Date")
            else:
                pass
        else:
            if(i == 3):
                date = str(date.get_text())
                date = datetime.datetime.strptime(date, "%m/%d/%Y")
                date = datetime.datetime.strftime(date, "%b %d, %Y")
                dates.append(date)
            else:
                pass
        
        reactid_prices = int(reactid_prices[0:4])
        reactid_prices += 2
        i += 1
    
    reactid_prices = 183

num_elements = len(dates)
a_range = range(0, num_elements)

for symbol, i in zip(list_tickers, a_range):

    url = "https://finance.yahoo.com/quote/" + symbol + "/history?p=" + symbol
    client = uReq(url)
    page = client.read()
    soup = BeautifulSoup(page, "html.parser")
    
    a_date_1 = dates[i]

    if(a_date_1 == "Invalid Date"):
        earnings_close.append("N/A")
        earnings_close_before.append("N/A")
    
    else:

        a_date = soup.find("td", text = re.compile(a_date_1), attrs = {"class": "Py(10px) Ta(start) Pend(10px)"})
        
        if(a_date is None):
            a_date_1 = datetime.datetime.strptime(a_date_1, "%b %d, %Y")
            a_date_1 = a_date_1 + datetime.timedelta(1)
            a_date_2 = a_date_1 + datetime.timedelta(1)
            a_date_1 = datetime.datetime.strftime(a_date_1, "%b %d, %Y")
            a_date_2 = datetime.datetime.strftime(a_date_2, "%b %d, %Y")

            a_date = soup.find("td", text = re.compile(a_date_1), attrs = {"class": "Py(10px) Ta(start) Pend(10px)"})

            if(a_date is None):
                a_date = soup.find("td", text = re.compile(a_date_2), attrs = {"class": "Py(10px) Ta(start) Pend(10px)"})

                if(a_date is None):
                    pass
                else:
                    reactid = a_date.span["data-reactid"]
                    reactid = int(reactid[0:4])
                    reactid += 7
                    reactid = str(reactid)
                    price = soup.find("td", {"data-reactid": reactid})
        
                    if(price is not None):
                        earnings_close.append(price.text)
            else:
                reactid = a_date.span["data-reactid"]
                reactid = int(reactid[0:4])
                reactid += 7
                reactid = str(reactid)
                price = soup.find("td", {"data-reactid": reactid})
        
                if(price is not None):
                    earnings_close.append(price.text)
        
        else:
            reactid = a_date.span["data-reactid"]
            reactid = int(reactid[0:4])
            reactid += 7
            reactid = str(reactid)
            price = soup.find("td", {"data-reactid": reactid})
        
            if(price is not None):
                earnings_close.append(price.text)
    
        a_date_before = datetime.datetime.strptime(a_date_1, "%b %d, %Y")
        a_date_before = a_date_before + datetime.timedelta(-1)
        a_date_before = datetime.datetime.strftime(a_date_before, "%b %d, %Y")

        date_before = soup.find("td", text = re.compile(a_date_before), attrs = {"class": "Py(10px) Ta(start) Pend(10px)"})

        if(date_before is None):
            a_date_before = datetime.datetime.strptime(a_date_before, "%b %d, %Y")
            a_date_before = a_date_before + datetime.timedelta(-1)
            a_date_before = datetime.datetime.strftime(a_date_before, "%b %d, %Y")

            date_before = soup.find("td", text = re.compile(a_date_before), attrs = {"class": "Py(10px) Ta(start) Pend(10px)"})

            if(date_before is None):
                a_date_before = datetime.datetime.strptime(a_date_before, "%b %d, %Y")
                a_date_before = a_date_before + datetime.timedelta(-1)
                a_date_before = datetime.datetime.strftime(a_date_before, "%b %d, %Y")

                date_before = soup.find("td", text = re.compile(a_date_before), attrs = {"class": "Py(10px) Ta(start) Pend(10px)"})

                if(date_before is None):
                    pass
                else:
                    reactid_before = date_before.span["data-reactid"]
                    reactid_before = int(reactid_before[0:4])
                    reactid_before += 7
                    reactid_before = str(reactid_before)
                    price_before = soup.find("td", {"data-reactid": reactid_before})

                    if(price_before is not None):
                        earnings_close_before.append(price_before.text)
            else:
                reactid_before = date_before.span["data-reactid"]
                reactid_before = int(reactid_before[0:4])
                reactid_before += 7
                reactid_before = str(reactid_before)
                price_before = soup.find("td", {"data-reactid": reactid_before})

                if(price_before is not None):
                    earnings_close_before.append(price_before.text)
        else:
            reactid_before = date_before.span["data-reactid"]
            reactid_before = int(reactid_before[0:4])
            reactid_before += 7
            reactid_before = str(reactid_before)
            price_before = soup.find("td", {"data-reactid": reactid_before})

            if(price_before is not None):
                earnings_close_before.append(price_before.text)



for close, close_before in zip(earnings_close, earnings_close_before):
    if(close == "N/A" or close_before == "N/A"):
        change.append("N/A")
    else:

        close = float(close.replace(",", ""))
        close_before = float(close_before.replace(",", ""))
        a_change = close - close_before
        if(a_change >= 0):
            a_change = str(a_change)
            a_change = "+" + a_change
            change.append(a_change)
        else:
            a_change = str(a_change)
            change.append(a_change)