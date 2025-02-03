import pandas as pd
from dash import Dash, dcc, html


# Read in data, filter for now since not yet interactive
data = (
    pd.read_csv("avocado.csv")
    .query("type == 'conventional' and region == 'Albany'")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

# Initialize Dash app
app = Dash(__name__)

# Define layout property of app, this is translated into html
app.layout = html.Div(
    children=[
        html.H1(
            children="Avocado Analytics",
            className="header-title"),
        html.P(
            children=(
                "Analyze the bahavior of avocado prices and the number"
                " of avocados sold in the US between 2015 and 2018"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados Sold"},
            },
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)

