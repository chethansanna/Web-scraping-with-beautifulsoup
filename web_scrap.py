"""
Retriving the "Closing Price" of Bitcoin and Ethereum from a website for a particular date range
and then plotting the Closing Price along each Date using Plotly
"""

import bs4 as bs
import urllib.request
import pandas as pd
import plotly.graph_objs as go

def GettingData(coin, start_date_str, end_date_str):
    """Function dedicated to scraping coinmarketcap and retrieving a Pandas DataFrame"""

    # Formatting of user inputs
    coin = coin.lower()
    start_date_str = pd.to_datetime(start_date_str)
    end_date_str = pd.to_datetime(end_date_str)
    start_date = start_date_str.strftime('%Y%m%d')
    end_date = end_date_str.strftime('%Y%m%d')


    # Retrieves data with BeautifulSoup and parses
    url = 'https://coinmarketcap.com/currencies/' + coin + '/historical-data/?start=' + start_date + '&end='+end_date
    print(url)
    link = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(link, "html.parser")
    prices_table = soup.find_all('tr')
    prices_table = prices_table[2:]

    # Creates list of dictionaries to feed into the DataFrame
    list_of_dic = []
    for count, itemset in enumerate(prices_table):
        itemset = list(itemset)
        date = itemset[0].text
        Open = itemset[1].text
        high = itemset[2].text
        low = itemset[3].text
        close = itemset[4].text
        volume = itemset[5].text
        dictionary = {'Date' : date, 'Coin' : coin.capitalize(), 'Opening Price' : Open,'Closing Price' : close, 'Low' :
            low, 'High': high, 'Volume' : volume}
        list_of_dic.append(dictionary)

        if count == (end_date_str-start_date_str).days+2:
            break

    # Creates and sends our DataFrame
    df = pd.DataFrame(list_of_dic)
    df = df.drop(df.index[0:2])
    df['Date'] = pd.to_datetime(df['Date'])
    Closing_price_df = df[['Date','Closing Price']]
    return Closing_price_df

def plot(date, price_data, coin):
    fig = go.Figure()
    coin_trace = fig.add_trace(go.Scatter(x=date, y=price_data))
    fig.update_layout(title= coin,
                   xaxis_title='Date',
                   yaxis_title='Closing Price')
    fig.show()

if __name__ == "__main__":
    Closing_price_bitcoin = GettingData('Bitcoin','Jan 1, 2019', 'July 31, 2020')
    Closing_price_ethereum = GettingData('Ethereum','Jan 1, 2019', 'July 31, 2020')    
    plot(Closing_price_bitcoin['Date'],Closing_price_bitcoin['Closing Price'], 'Bitcoin')
    plot(Closing_price_ethereum['Date'],Closing_price_ethereum['Closing Price'], 'Ethereum')
