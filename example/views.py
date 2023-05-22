# example/views.py
from datetime import datetime

from django.http import HttpResponse

def index(request):
    now = datetime.now()
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
                        <th>Kurs kupna</th>
                        <th>Kurs sprzedaży</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>USD</td>
                        <td>3.85</td>
                        <td>3.90</td>
                      </tr>
                      <tr>
                        <td>EUR</td>
                        <td>4.30</td>
                        <td>4.35</td>
                      </tr>
                      <tr>
                        <td>GBP</td>
                        <td>5.10</td>
                        <td>5.20</td>
                      </tr>
                    </tbody>
                  </table>
            </div>
        </body>
    </html>
    '''

    response = HttpResponse(html % {'css_code': css_code})
    return response