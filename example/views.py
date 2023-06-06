from datetime import datetime, timedelta
import yfinance as yf
import json
from django.http import HttpResponse

def get_list_of_currencies():
    return ['EUR', 'USD', 'GBP', 'JPY']

def get_currency_info(symbol):
    ticker = yf.Ticker(symbol)
    today_data = ticker.history(period='1d')
    bid_price = ticker.info.get('bid')
    ask_price = ticker.info.get('ask')
    week_data = ticker.history(period='1wk')
    closing_prices = week_data['Close'].tolist()
    date_labels = (week_data.index - timedelta(days=6)).strftime('%Y-%m-%d').tolist()
    return today_data, bid_price, ask_price, closing_prices, date_labels

def get_currency_table_html(currencies, rounding=.4):
    currency_html = ""
    for currency in currencies:
        symbol = currency + 'PLN=X'
        currency_info = get_currency_info(symbol)
        currency_html += f'''<tr>
                                <td>{currency}</td>
                                <td>{currency_info[0]['Open'][-1]:{rounding}f}</td>
                                <td>{currency_info[0]['High'].max():{rounding}f}</td>
                                <td>{currency_info[0]['Low'].min():{rounding}f}</td>
                                <td>{currency_info[0]['Close'][-1]:{rounding}f}</td>
                                <td>{currency_info[1]:{rounding}f}</td>
                                <td>{currency_info[2]:{rounding}f}</td>
                                <td>
                                    <div class="chart-container">
                                        <canvas id="{currency}-chart"></canvas>
                                    </div>
                                </td>
                              </tr>
                              <script>
                                  var ctx = document.getElementById("{currency}-chart").getContext("2d");
                                  var chart = new Chart(ctx, {{
                                      type: 'line',
                                      data: {{
                                          labels: {json.dumps(currency_info[4])},
                                          datasets: [{{
                                              label: '{currency} Closing Prices',
                                              data: {json.dumps(currency_info[3])},
                                              backgroundColor: 'rgba(0, 123, 255, 0.1)',
                                              borderColor: 'rgba(0, 123, 255, 1)',
                                              borderWidth: 1,
                                              tension: 0.4
                                          }}]
                                      }},
                                      options: {{
                                          responsive: true,
                                          maintainAspectRatio: false,
                                          plugins: {{
                                              legend: {{
                                                  display: false
                                              }}
                                          }},
                                          scales: {{
                                              x: {{
                                                  display: true,
                                                  ticks: {{
                                                      autoSkip: true,
                                                      maxTicksLimit: 6
                                                  }}
                                              }},
                                              y: {{
                                                  display: true,
                                                  ticks: {{
                                                      callback: function(value, index, values) {{
                                                          return value.toFixed(2);
                                                      }}
                                                  }}
                                              }}
                                          }}
                                      }}
                                  }});
                              </script>'''
    return currency_html


def index(request):
    now = datetime.now()
    currencies = get_list_of_currencies()
    css_code = '''
    <style>
        * {
          border: none;
          outline: none;
        }
            
         body {
          font-family: Arial, sans-serif;
          margin: 0;
          background-color: #f2f2f2;
        }

        #header {
          width: 100%;
        }
        
        #main {
          margin-top: 50px;
        }
        
        img {
          display: block;
          margin-left: auto;
          margin-right: auto;
          width: 100%;
          height: auto;
        }

        h1 {
          text-align: center;
        }
        
        .mt-4 {
          padding-top: 50px;
        }
        
        table {
          text-align: center;
        }
        
        td, th {
          vertical-align: middle;
        }

        @media only screen and (max-width: 600px) {
          h1 {
            font-size: 18px;
          }
        }
        
    </style>
    '''
    chart_script = '''
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.5.1/dist/chart.min.js"></script>
    '''
    bootstrap_link = '''
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    '''
    bootstrap_script = '''
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KyZXEAg3QhqLMpG8r+6+Scdh5PDUo3I5td0nqj7P2JqRAFa3a625fcd00zstjQ4y" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    '''
    script = '''
        <script>
            function sendAlert() {
                alert("Wysyłanie maila...");
            }
        </script>
    '''
    html = f'''
    <html>
      <head>
        <title>Zabawne kursy na każdy dzień!</title>
        {chart_script}
        {css_code}
        {bootstrap_link}
        {bootstrap_script}
        {script}
      </head>
      <body>
        <nav class="navbar fixed-top navbar-expand-lg navbar-light bg-light">
          <div class="container">
            <a class="navbar-brand text-warning" href="https://io-project-eta.vercel.app/">Złoty Stand-up</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                  <a class="nav-link" href="https://io-project-eta.vercel.app/">Strona główna</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#main">Kursy</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#about">O nas</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#footer">Kontakt</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        
        <section class="mt-4 container">
            <p>Rynek walutowy, znany również jako Forex, jest największym i najbardziej płynnym rynkiem na świecie. Tutaj handluje się różnymi walutami z całego globu, tworząc nieustanne możliwości inwestycyjne. Na naszej stronie prezentujemy aktualne kursy walut wobec złotego, aby pomóc Ci śledzić zmiany w wartości walut i podejmować informowane decyzje inwestycyjne.</p>
            <p>Na stronie znajdziesz aktualne kursy kilku najważniejszych walut światowych. Są to między innymi dolar amerykański (USD), euro (EUR), funt brytyjski (GBP) i jen japoński (JPY). Kursy walut są aktualizowane na bieżąco, umożliwiając Ci monitorowanie zmian wartości tych walut w stosunku do polskiego złotego.</p>
            <p>Nasza strona nie tylko dostarcza aktualnych kursów walut, ale również udostępnia narzędzia i wykresy, które mogą pomóc Ci analizować trendy i prognozować przyszłe zmiany w wartości walut. Możesz zobaczyć wykresy historyczne, porównać wybrane waluty i przeprowadzić techniczną analizę, aby uzyskać lepsze zrozumienie rynku.</p>
            <p>Na naszej stronie znajdziesz również aktualne informacje o najważniejszych wydarzeniach gospodarczych, które mogą mieć wpływ na kursy walut. Regularnie aktualizujemy nasze wiadomości, abyś był na bieżąco z najświeższymi informacjami związanymi z gospodarką światową i mogłeś lepiej zrozumieć, dlaczego kursy walut się zmieniają.</p>
            <p>Inwestowanie na rynku walutowym może być zarówno ekscytujące, jak i ryzykowne. Dlatego na naszej stronie udostępniamy porady i wskazówki dotyczące inwestowania w waluty. Dowiesz się, jak analizować rynek, zarządzać ryzykiem i podejmować trafne decyzje inwestycyjne. Pamiętaj, że inwestowanie na rynku walutowym wiąże się z ryzykiem straty kapitału, dlatego zawsze powinieneś dobrze się zastanowić i skonsultować z profesjonalistą przed podjęciem jakichkolwiek decyzji inwestycyjnych.</p>
        </section>

        <div id="main" class="container">
          <div class="d-flex justify-content-between align-items-center">
            <h1>Obecne kursy walut:</h1>
            <button class="btn btn-primary" id="alert-button" onclick="sendAlert()">Ustaw alert!</button>
          </div>

          <div class="table-responsive">
            <table class="table table-bordered mt-4">
              <thead>
                <tr>
                  <th>Waluta</th>
                  <th>Otwarcie</th>
                  <th>Szczyt</th>
                  <th>Dół</th>
                  <th>Zamknięcie</th>
                  <th>Bid</th>
                  <th>Ask</th>
                  <th>Wykres</th>
                </tr>
              </thead>
              <tbody>
                {get_currency_table_html(currencies)}
              </tbody>
            </table>
          </div>
        </div>
        
        <section id="about">
          <div class="container">
            <h2>O Nas</h2>
            <p>
              Jesteśmy młodym i dynamicznym zespołem pasjonatów finansów i technologii. Naszą misją jest dostarczenie użytkownikom łatwego i intuicyjnego sposobu śledzenia aktualnych kursów walut.
            </p>
            <p>
              Nasza strona powstała z myślą o tych, którzy potrzebują szybkiego dostępu do aktualnych informacji o kursach walut. Chcieliśmy stworzyć miejsce, gdzie użytkownicy mogą na bieżąco śledzić zmiany i analizować wykresy, aby podejmować lepsze decyzje inwestycyjne.
            </p>
            <p>
              Nasz zespół składa się z doświadczonych ekspertów finansowych i programistów, którzy połączyli swoje umiejętności, aby stworzyć tę stronę. Dążymy do ciągłego doskonalenia naszych usług i dostarczania najbardziej aktualnych i dokładnych danych o kursach walut.
            </p>
          </div>
        </section>
        
        <footer class="bg-dark text-light py-4" id="footer">
            <div class="container">
                <div class="row">
                    <div class="col-lg-6">
                        <h4>Kontakt</h4>
                        Uniwersytet Pedagogiczny im. Komisji Edukacji Narodowej w Krakowie
                    </div>
                    <div class="col-lg-6">
                        <h4>Linki</h4>
                        <ul class="list-unstyled">
                            <li><a href="https://io-project-eta.vercel.app/">Strona główna</a></li>
                            <li><a href="#main">Kursy</a></li>
                            <li><a href="#about">O nas</a></li>
                            <li><a href="#contact">Kontakt</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </footer>
      </body>
    </html>
    '''

    return HttpResponse(html)
