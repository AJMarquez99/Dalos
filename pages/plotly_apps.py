import plotly.graph_objects as go
import plotly.io as pio

from dash import dcc, html
from django_plotly_dash import DjangoDash
from yfinance import Ticker


def createStockDash(ticker: Ticker) -> None:
    info = ticker.info
    dash = DjangoDash(name=info['symbol'] + 'App')

    df = ticker.history(period='1mo')
    df.reset_index(inplace=True)

    fig = go.Figure(data=go.Candlestick(
            x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))

    fig.update_layout(template=pio.templates["plotly_dark"])

    dash.layout = html.Div([
        html.H4(info['shortName'] + ' Last 30 Days'),

        dcc.Checklist(
            id='toggle-rangeslider',
            options=[{'label': 'Include Rangeslider', 
                    'value': 'slider'}],
            value=['slider']
        ),
        dcc.Graph(id="graph", figure=fig),
    ])