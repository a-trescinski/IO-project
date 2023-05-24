# example/views.py
from datetime import datetime
import yfinance as yf

from django.http import HttpResponse


def get_list_of_currencies():
    '''nk sprawdzi, czy jest jakaś prosta metoda
     na pobranie wszystkich/wybranych trzyliterowych
     oznaczeń walut: [USD,EUR,JPN,...]'''
    return ['EUR', 'USD', 'GBP', 'JPY']

def get_current_price(symbol):
    """Get basic currency information from last day"""
    ticker = yf.Ticker(symbol)
    today_data = ticker.history(period='1d')
    return today_data


def get_currency_table_html(currencies, rounding=.4):
    currency_html = ""
    for currency in currencies:
        symbol = currency + 'PLN=X'
        currency_info = get_current_price(symbol)
        currency_html += f'''<tr>
                                    <td>{currency}</td>
                                    <td>{currency_info['Open'][0]:{rounding}f}</td>
                                    <td>{currency_info['High'][0]:{rounding}f}</td>
                                    <td>{currency_info['Low'][0]:{rounding}f}</td>
                                    <td>{currency_info['Close'][0]:{rounding}f}</td>
                                  </tr>'''
    return currency_html


def index(request):
    now = datetime.now()
    currencies = get_list_of_currencies()
    css_code = '''
    <style>
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 20px;
          background-color: #f2f2f2;
        }
        
        img {
          display: block;
          margin-left: auto;
          margin-right: auto;
        }
        
        h1 {
          text-align: center;
        }
        
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
        }
        
        th, td {
          padding: 10px;
          text-align: center;
          border: 1px solid #ccc;
        }
        
        th {
          background-color: #e0e0e0;
        }
        
        tr:nth-child(even) {
          background-color: #f9f9f9;
        }
    </style>
    '''
    html = f'''
    <html>
        <head>
            <title>Super strona!</title>
            %(css_code)s
        </head>
        <body>
            <div id="header">
                <img src="https://cdn.pixabay.com/photo/2018/03/10/09/45/businessman-3213659_960_720.jpg">
            </div>
            
            <div id="main">
                  <h1>Kursy Walut</h1>
  
                  <table>
                    <thead>
                      <tr>
                        <th>Waluta</th>
                        <th>Otwarcie</th>
                        <th>Szczyt</th>
                        <th>Dół</th>
                        <th>Zamknięcie</th>
                      </tr>
                    </thead>
                    <tbody>
                    {get_currency_table_html(currencies)}
                    </tbody>
                  </table>
            </div>
        </body>
    </html>
    '''

    response = HttpResponse(html % {'css_code': css_code})
    return response
