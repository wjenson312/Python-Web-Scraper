from bs4 import BeautifulSoup
from urllib.request import urlopen as Req
from StockList import list_tickers
from StockPrices import earnings_close

actual_earnings = []
consensus_earnings = []

for ticker in list_tickers:

    url = "https://finance.yahoo.com/quote/" + ticker + "/analysis?p=" + ticker
    client = Req(url)
    page = client.read()
    soup = BeautifulSoup(page, "html.parser")
    
    reactid = 195

    for i in range(4):
        reactid = str(reactid)
        earnings_consensus = soup.find("td", {"data-reactid": reactid})
        if(earnings_consensus is None):
            consensus_earnings.append("N/A")
        elif(earnings_consensus.text == "N/A"):
            consensus_earnings.append("N/A")
        else:
            consensus_earnings.append(earnings_consensus.text)
        reactid = int(reactid)
        reactid += 2
    
    reactid = 206
    
    for x in range(4):
        reactid = str(reactid)
        earnings_actual = soup.find("td", {"data-reactid": reactid})
        if(earnings_actual is None):
            actual_earnings.append("N/A")
        elif(earnings_actual.text == "N/A"):
            actual_earnings.append("N/A")
        else:
            actual_earnings.append(earnings_actual.text)
        reactid = int(reactid)
        reactid += 2

num_elements = len(actual_earnings)

beat_or_missed = []
num = 0

for y in range(0, num_elements, 4):
    for a in range(4):
        actual = actual_earnings[y]
        consensus = consensus_earnings[y]

        if(actual == "N/A" or consensus == "N/A" or not "." in actual):
            beat_or_missed.append("N/A")
        else:
            actual = float(actual)
            consensus = float(consensus)

            if(actual > consensus):
                beat_or_missed.append("Beat")
            elif(actual < consensus):
                beat_or_missed.append("Missed")
            elif(actual == consensus):
                beat_or_missed.append("Met")
        
        num += 1
        y += 1
