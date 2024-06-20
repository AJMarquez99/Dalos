from enum import Enum
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

class ToggleType(Enum):
    CANDLE = "candle"
    LINE = "line"

def getGraphDateRangeHTML(id: str, initial_value: str = "1d") -> dcc.RadioItems:
    button_class = "btn btn-outline-primary me-3 pe-none"

    return dcc.RadioItems(
        id=id,
        options=[
            {
                "label": html.Label(['1D'], className=button_class),
                "value": "1d"
            },
            {
                "label": html.Label(['1W'], className=button_class),
                "value": "1wk"
            },
            {
                "label": html.Label(['1M'], className=button_class),
                "value": "1mo"
            },
            {
                "label": html.Label(['3M'], className=button_class),
                "value": "3mo"
            },
            {
                "label": html.Label(['1Y'], className=button_class),
                "value": "1y"
            },
            {
                "label": html.Label(['5Y'], className=button_class),
                "value": "5y"
            }
        ],
        inline=True,
        inputClassName="visually-hidden btn-check",
        className="mb-3",
        value=initial_value,
    )

def getGraphTypeToggle(id: str, initial_value: ToggleType = "line") -> dcc.RadioItems:
    button_class = "btn btn-outline-primary me-3 pe-none"

    return dcc.RadioItems(
            id=id,
            options=[
                {
                    "label": html.Label(['Line'], className=button_class),
                    "value": "line"
                },
                {
                    "label": html.Label(['Candlestick'], className=button_class),
                    "value": "candle"
                }
            ],
            inline=True,
            inputClassName="visually-hidden btn-check",
            className="mt-3",
            value=initial_value,
        )