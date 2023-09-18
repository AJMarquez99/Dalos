import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from yfinance import Ticker

external_stylesheets = [
    '/static/css/main.css',
]

def createStockDash(ticker: Ticker) -> None:
    info = ticker.info
    dash = DjangoDash(name=info['symbol'] + 'App', external_stylesheets=external_stylesheets)

    df = ticker.history(period="1mo", interval="1h")
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
        dtick=1000*60*60,
        tickformat="%b\n%Y",
        rangeslider_visible=False,
        ticklabelmode="instant",
        rangebreaks=hourly_breaks,
        showticklabels=False,
        showgrid=False,
    )

    fig.update_yaxes(
        showticklabels = False,
        showgrid=False,
    )

    dash.layout = html.Div([
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
                    "label": html.Label(['All'], className="btn btn-outline-primary me-3 pe-none"),
                    "value": "max"
                }
            ],
            inline=True,
            inputClassName="visually-hidden btn-check",
            className="mb-3",
            value="1mo",
        ),
    ])

    @dash.callback(
        Output('ticker_graph', 'figure'),
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
            case "max":
                df = ticker.history(period=date_range, interval="1wk")
            case _:
                df = ticker.history(period=date_range, interval="1d")

        df.reset_index(inplace=True)

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

        return fig