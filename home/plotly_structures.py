import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from enum import Enum
from dash import dcc, html
from pandas import DataFrame
from typing import List

class ToggleType(Enum):
    CANDLE = "candle"
    LINE = "line"

def getGraphHeaderHTML(name: str, price: float, change: float, growth: bool, authenticated: bool) -> html.Div:
    text_color_class = "ps-3 text-success" if growth else "ps-3 text-danger"

    return html.Div(
            children=[
                html.H2(
                    name,
                    className="my-0"
                ),
                html.Span(
                    f"${price:,.2f}",
                    className=text_color_class,
                    id="ticker_price"
                ),
                html.Span(
                    f'+{change:.3f}%' if growth else f'{change:.3f}%',
                    className=text_color_class,
                    id="ticker_percent_change"
                ),
                html.A(
                    children=[
                        html.I(
                            className="bi bi-star"
                        )
                    ],
                    href="" if authenticated else "/login",
                    className="ps-3 fs-3 lh-1 text-dark"
                )
            ],
            className="d-flex flex-row align-items-end mb-3 stock-title"
        )

def getGraphDateRangeHTML(id: str, initial_value: str = "1d") -> dcc.RadioItems:
    button_class = "btn btn-outline-primary me-3 pe-none"

    return dcc.RadioItems(
        id=id,
        options=[
            {
                "label": "1D",  
                "value": "1d"
            },
            {
                "label": "1W", 
                "value": "1wk"
            },
            {
                "label": "1M", 
                "value": "1mo"
            },
            {
                "label": "3M", 
                "value": "3mo"
            },
            {
                "label": "1Y", 
                "value": "1y"
            },
            {
                "label": "5Y", 
                "value": "5y"
            },
        ],
        inline=True,
        inputClassName="visually-hidden btn-check",
        labelClassName="btn btn-outline-primary me-3 pe-none",
        className="mb-3",
        value=initial_value,
    )

def getGraphTypeToggleHTML(id: str, initial_value: str = ToggleType.LINE.value) -> dcc.RadioItems:
    button_class = "btn btn-outline-primary me-3 pe-none"

    return dcc.RadioItems(
        id=id,
        options=[
            {
                "label": html.Label(["Line"], className = button_class), 
                "value": ToggleType.LINE.value
            },
            {
                "label": html.Label(["Candlestick"], className = button_class), 
                "value": ToggleType.CANDLE.value
            },
        ],
        inline=True,
        inputClassName="visually-hidden btn-check",
        className="mt-3",
        value=initial_value,
    )

def getStockEndPointsHTML(high: float, low: float) -> html.Div:
    return html.Div(
        [
            html.Span(f"High: ${high:,.2f}", className="pe-3", id="period_high"),
            html.Span(f"Low: ${low:,.2f}", className="pe-3", id="period_low"),
        ],
    )

def getStandardStockFigure(df: DataFrame, in_minutes: bool, range_breaks: List, type: str = ToggleType.LINE.value) -> go.Figure:
    if type not in [t.value for t in ToggleType]:
        raise TypeError("Type must be of type ToggleType")
    
    match type:
        case ToggleType.CANDLE.value:
            fig = go.Figure(data=go.Candlestick(
                x=df['Datetime'] if in_minutes else df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color='#00b300',
                decreasing_line_color='#e60000'
            ))
        case ToggleType.LINE.value | _:
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
                y=df['Open'][0],
                line_width=1,
                opacity=0.2,
            )
    
    fig.update_layout(
        template=pio.templates["none"],
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        hovermode="x",
        paper_bgcolor="rgb(244, 247, 250)",
        plot_bgcolor="rgb(244, 247, 250)",
    )
    fig.update_xaxes(
        dtick=1000*60*60 if in_minutes else "M1",
        tickformat="%b\n%Y",
        rangeslider_visible=False,
        ticklabelmode="instant" if in_minutes else "period",
        rangebreaks=range_breaks,
        showticklabels=False,
        showgrid=False,
    )
    fig.update_yaxes(
        showticklabels = False,
        showgrid=False,
    )
    
    return fig            