from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash
from .stock_class import StockPage
from .plotly_structures import *

external_stylesheets = [
    '/static/css/main.css',
]
   
def createStockDash(ticker: str, is_authenticated: bool) -> None:
    stock = StockPage(ticker)
    info = stock.stockInfo
    dash = DjangoDash(name=info.symbol + 'App', external_stylesheets=external_stylesheets)

    df = stock.getCommonDateRange("1d")

    fig = getStandardStockFigure(df, StockPage.inMinutes("1d"), StockPage.getRangeBreaks("1d"))

    print("Current Price: ", stock.currentPrice)
    print("Open Price: ", df['Open'][0])
    print(stock.isGrowth(df['Open'][0]))
    print(df)

    dash.layout = html.Div([
        getGraphHeaderHTML(info.shortName, stock.currentPrice, stock.percentChange(df['Open'][0]), stock.isGrowth(df['Open'][0]), is_authenticated),
        getStockEndPointsHTML(info.dayHigh, info.dayLow),
        getGraphTypeToggleHTML("graph_type"),
        dcc.Graph(id="ticker_graph", figure=fig),
        getGraphDateRangeHTML("date_range"),
    ])

    @dash.callback(
        Output('ticker_graph', 'figure'),
        Output('period_high', 'children'),
        Output('period_low', 'children'),
        Output('ticker_price', 'className'),
        Output('ticker_percent_change', 'className'),
        Output('ticker_percent_change', 'children'),
        Input('date_range', 'value'),
        Input('graph_type', 'value'),
        prevent_initial_call=True
    )
    def update_date_range(date_range, graph_type):
        df = stock.getCommonDateRange(date_range)

        growth = stock.isGrowth(df['Open'][0])
        high = 'High: ${:,.2f}'.format(df['High'].max())
        low = 'Low: ${:,.2f}'.format(df['Low'].min())
        text_color = "ps-3 text-success" if growth else "ps-3 text-danger"
        percent_change = '+{:.3f}%'.format(stock.percentChange(df['Open'][0])) if growth else '{:.3f}%'.format(stock.percentChange(df['Open'][0]))

        fig = getStandardStockFigure(df, StockPage.inMinutes(date_range), StockPage.getRangeBreaks(date_range), graph_type)

        return fig, high, low, text_color, text_color, percent_change