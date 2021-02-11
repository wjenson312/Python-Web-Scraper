from StockList import list_tickers, list_titles, list_price
from StockPrices import earnings_close, earnings_close_before, change
from SNP500 import snp_close, snp_close_before, snp_change
from GetEarnings import beat_or_missed

num_stocks = len(earnings_close)
num_stocks = str(num_stocks)

data_1 = []
data_2 = []

print(len(snp_close))
print(len(earnings_close))

filename = "Top " + num_stocks + " Consumer Cyclical Stocks.csv"
fl = open(filename, "w")
headers = "Ticker, Company Name, Today Price, Earnings Close(T), T-2, Delta(T), S&P @ T, S&P @ T-2, S&P Delta, Earnings -4Q, Earnings -3Q, Earnings -2Q, Earnings -1Q \n"
fl.write(headers)

num_elements = len(beat_or_missed) - 4
num = 0
num_stocks = int(num_stocks)
num_2 = 0

for ticker, title, price, close, close_before, changes, SNP_close, SNP_close_before, SNP_change in zip(list_tickers, list_titles, list_price, earnings_close, earnings_close_before, change, snp_close, snp_close_before, snp_change):
    string_data = ticker + "," + title.replace(",", "") + "," + price.replace(",", "") + "," + close.replace(",", "") + "," + close_before.replace(",", "") + "," + changes + "," + SNP_close.replace(",", "") + "," + SNP_close_before.replace(",", "") + "," + SNP_change.replace(",", "")
    data_1.append(string_data)
    num_2 += 1

num_earnings_ago = 0
for i in range(0, num_elements, 4):
    num_earnings_ago = 4
    for x in range(4):
        num_earnings_ago = str(num_earnings_ago)
        string_earnings = beat_or_missed[i]
        data_2.append(string_earnings)
        num_earnings_ago = int(num_earnings_ago)
        num_earnings_ago -= 1
        num += 1
        i += 1

#print(num_2)

for x, y in zip(range(0, num, 4), range(0, num_2)):
    string_all = data_1[y] + "," + data_2[x] + "," + data_2[x + 1] + "," + data_2[x + 2] + "," + data_2[x + 3] + "\n"
    fl.write(string_all)

fl.close()
