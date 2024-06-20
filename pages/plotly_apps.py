import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from dash import dcc, html, Input, Output, callback
from django_plotly_dash import DjangoDash
from .stock_data import StockPage

from .plotly_structures import *

external_stylesheets = [
    '/static/css/main.css',
]

def createStockDash(ticker: str, is_authenticated: bool) -> None:
    stock = StockPage(ticker)
    info = stock.stockInfo
    dash = DjangoDash(name=info.symbol + 'App', external_stylesheets=external_stylesheets)

    dash.layout = html.Div([
        html.Div(
            children=[
                html.H2(
                    info.shortName,
                    className="my-0"
                ),
                html.Span(
                    '${:,.2f}'.format(stock.currentPrice),
                    id="ticker_price",
                    className="ms-3"
                ),
                html.Span(
                    id="ticker_percent_change"
                ),
                html.A(
                    children=[
                        html.I(
                            className="bi bi-star"
                        )
                    ],
                    href="" if is_authenticated else "/login",
                    className="ps-3 fs-3 lh-1 text-dark"
                )
            ],
            className="d-flex flex-row align-items-end mb-3 stock-title"
        ),
        html.Div(
            children=[
                html.Span(
                    'High: ${:,.2f}'.format(info.dayHigh),
                    className="pe-3",
                    id="period_high"
                ),
                html.Span(
                    'Low: ${:,.2f}'.format(info.dayLow),
                    className="pe-3",
                    id="period_low"
                )
            ]
        ),
        getGraphTypeToggle(id="graph_type"),
        dcc.Graph(id="ticker_graph"),
        getGraphDateRangeHTML("date_range"),
    ])

    @callback(
        Output('ticker_graph', 'figure'),
        Output('period_high', 'children'),
        Output('period_low', 'children'),
        Output('ticker_price', 'className'),
        Output('ticker_percent_change', 'className'),
        Output('ticker_percent_change', 'children'),
        Input('date_range', 'value'),
        Input('graph_type', 'value'),
    )
    def update_date_range(date_range, graph_type):
        df = stock.getCommonDateRange(date_range)

        in_minutes = stock.inMinutes(date_range)

        pos = stock.isGrowth(df['Open'][0])
        high = 'High: ${:,.2f}'.format(df['High'].max())
        low = 'Low: ${:,.2f}'.format(df['Low'].min())
        text_color_class = "ps-3 text-success" if pos else "ps-3 text-danger"
        percent_change = '+{:.3f}%'.format(stock.getPercentageChange(df['Open'][0])) if pos else '{:.3f}%'.format(stock.getPercentageChange(df['Open'][0]))

        if graph_type == "candle":
            fig = go.Figure(data=go.Candlestick(
                x=df['Datetime'] if in_minutes else df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color='#00b300',
                decreasing_line_color='#e60000'
            ))
        else:
            fig = px.line(
                df, 
                x='Datetime' if in_minutes else 'Date', 
                y='Close',
            )
            fig.update_traces(
                line_color="#FF5400",
                hovertemplate=
                '<span>Date</span>: %{x}'+
                '<br><span>Price</span>: %{y:$.2f}<extra></extra>'
            )
            fig.add_hline(
                y=df['Close'][0],
                line_width=1,
                opacity=0.2,
            )
        
        fig.update_layout(
            template=pio.templates["none"],
            xaxis_title="",
            yaxis_title="",
            legend_title="",
            hovermode="x",
        )
        fig.update_xaxes(
            dtick=1000*60*60 if in_minutes else "M1",
            tickformat="%b\n%Y",
            rangeslider_visible=False,
            ticklabelmode="instant" if in_minutes else "period",
            rangebreaks=StockPage.getRangeBreaks(date_range),
            showticklabels=False,
            showgrid=False,
        )
        fig.update_yaxes(
            showticklabels = False,
            showgrid=False,
        )

        return fig, high, low, text_color_class, text_color_class, percent_change