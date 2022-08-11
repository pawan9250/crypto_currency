from currency_convert_package import Convert_to_currency
from bs4 import BeautifulSoup
import requests
from request_header import headers
import json
# import pprint as prity_print
page = '1'
url = "https://www.coingecko.com/?page="+page


def extract_digit(price):
    price_list = list(price)
    price_remove = price_list.pop(0)
    price_final = "".join(price_list)
    return price_final

convert_to = "INR"
convert_from = "USD"
r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")
# time.sleep(5)
#find coin table 
coin_table = soup.find('table', 'table')
#coin table body
table_body = coin_table.find('tbody')
#find table row
table_row = table_body.find_all('tr')
for tds in table_row:
    td = tds.find_all('td')
#find table data
    #rank
    rank = td[1].get_text().strip()
    #logo
    logo_path = td[2].find('img')['src'].strip() 
    #name 
    coin_name = td[2].find_all('span')[0].get_text().strip()
    #price
    price = extract_digit(td[4].get_text().strip())
    coint_price_convert = Convert_to_currency(convert_to, convert_from, price)
    coin_price = coint_price_convert.get_currency_convert()
    #market_capital
    market_cap = extract_digit(td[9].get_text().strip())
    market_cap_convert = Convert_to_currency(convert_to, convert_from, market_cap)
    market_cap_price = market_cap_convert.get_convert_only_value()

    data = {
        'rank': rank,
        'logo_path': logo_path,
        'coin_name': coin_name,
        'coin_price': coin_price['to']['inr'],
        'market_cap_price': market_cap_price['value']
    }
    # prity_print.pprint(data)
    print(json.dumps(data, indent=4))
