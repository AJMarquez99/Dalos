import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from yfinance import Ticker
from .stock_data import StockPage

external_stylesheets = [
    '/static/css/main.css',
]

def createStockDash(ticker: Ticker, is_authenticated: bool) -> None:
    info = ticker.info
    stock= StockPage(ticker)
    dash = DjangoDash(name=info['symbol'] + 'App', external_stylesheets=external_stylesheets)

    period = "1d"

    match period:
        case "1d":
            df = ticker.history(period=period, interval="5m")
            in_minutes = True
        case "1wk" | "1mo":
            df = ticker.history(period=period, interval="1h")
            in_minutes = True
        case "max":
            df = ticker.history(period=period, interval="1wk")
        case _:
            df = ticker.history(period=period, interval="1d")
    df.reset_index(inplace=True)

    fig = px.line(
        df, 
        x='Datetime', 
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

    daily_breaks = [
        dict(bounds=["sat", "mon"])
    ]
    hourly_breaks = [
        dict(bounds=["sat", "mon"]),
        dict(bounds=[17,9], pattern="hour")
    ]
    
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
        rangebreaks=hourly_breaks if in_minutes else daily_breaks,
        showticklabels=False,
        showgrid=False,
    )
    fig.update_yaxes(
        showticklabels = False,
        showgrid=False,
    )

    pos = stock.isGrowth(df['Open'][0])
    text_color_class = "ps-3 text-success" if pos else "ps-3 text-danger"

    dash.layout = html.Div([
        html.Div(
            children=[
                html.H2(
                    stock.shortName,
                    className="my-0"
                ),
                html.Span(
                    '${:,.2f}'.format(stock.currentPrice),
                    className=text_color_class,
                    id="ticker_price"
                ),
                html.Span(
                    '+{:.3f}%'.format(stock.currentPercentChange) if pos else '{:.3f}%'.format(stock.currentPercentChange) ,
                    className=text_color_class,
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
                    'High: ${:,.2f}'.format(stock.dayHigh),
                    className="pe-3",
                    id="period_high"
                ),
                html.Span(
                    'Low: ${:,.2f}'.format(stock.dayLow),
                    className="pe-3",
                    id="period_low"
                )
            ]
        ),
        dcc.RadioItems(
            id="graph_type",
            options=[
                {
                    "label": html.Label(['Line'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "line"
                },
                {
                    "label": html.Label(['Candlestick'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "candle"
                }
            ],
            inline=True,
            inputClassName="visually-hidden btn-check",
            className="mt-3",
            value="line",
        ),
        dcc.Graph(id="ticker_graph", figure=fig),
        dcc.RadioItems(
            id="date_range",
            options=[
                {
                    "label": html.Label(['1D'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "1d"
                },
                {
                    "label": html.Label(['1W'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "1wk"
                },
                {
                    "label": html.Label(['1M'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "1mo"
                },
                {
                    "label": html.Label(['3M'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "3mo"
                },
                {
                    "label": html.Label(['1Y'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "1y"
                },
                {
                    "label": html.Label(['5Y'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "5y"
                }
            ],
            inline=True,
            inputClassName="visually-hidden btn-check",
            className="mb-3",
            value="1d",
        ),
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
        in_minutes = False

        match date_range:
            case "1d":
                df = ticker.history(period=date_range, interval="5m")
                in_minutes = True
            case "1wk" | "1mo":
                df = ticker.history(period=date_range, interval="1h")
                in_minutes = True
            case "5y":
                df = ticker.history(period=date_range, interval="1wk")
            case _:
                df = ticker.history(period=date_range, interval="1d")

        df.reset_index(inplace=True)

        pos = stock.isGrowth(df['Open'][0])
        high = 'High: ${:,.2f}'.format(df['High'].max())
        low = 'Low: ${:,.2f}'.format(df['Low'].min())
        text_color = "ps-3 text-success" if pos else "ps-3 text-danger"
        percent_change = '+{:.3f}%'.format(stock.percentChange(df['Open'][0])) if pos else '{:.3f}%'.format(stock.percentChange(df['Open'][0]))

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
            rangebreaks=hourly_breaks if in_minutes else daily_breaks,
            showticklabels=False,
            showgrid=False,
        )
        fig.update_yaxes(
            showticklabels = False,
            showgrid=False,
        )

        return fig, high, low, text_color, text_color, percent_change