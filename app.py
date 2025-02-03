import pandas as pd
from dash import Dash, Input, Output, dcc, html


# Read in data
data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

# These will populate dropdowns
regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()

# Point to external stylesheet
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Initialize Dash app, include external styling
app = Dash(__name__, external_stylesheets=external_stylesheets)
# Add title to app
app.title = "Avocado Analytics: Know Your Avocados"

# Define layout property of app, this is translated into html
app.layout = html.Div(
    children=[
        # Header div
        html.Div(
            children=[
                html.P(
                    children="🥑", className="header-emoji"
                ),
                html.H1(
                    children="Avocado Analytics",
                    className="header-title"),
                html.P(
                    children=(
                        "Analyze the behavior of avocado prices and the number"
                        " of avocados sold in the US between 2015 and 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # Add in filters for graphs, drop downs and date picker examples
        html.Div(
            children=[
                # region filter menu
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            # default value when page loads
                            value="Albany",
                            # user able to leave empty is False
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # type filter menu
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": avocado_type.title(),
                                    "value": avocado_type,
                                }
                                for avocado_type in avocado_types
                            ],
                            # default value when page loads
                            value="organic",
                            # user able to leave blank is False
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                # date range, start, end date filter menu
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        # remove floating bar Plotly shows by default
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

# This decorator triggers function when input changes to update graphs
# For outputs - takes id of elements they'll modify when function executes, and property of element to be modified
# For inputs - take id of elements they'll be watching for changes, and property of watched element they'll be watching for changes
@app.callback(
    # so this will update 'figure' property of 'price-chart' element, etc
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    # and this will watch the 'region-filter' element, and its 'value' property for changes
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)


# Create function to return filtered data back to figure
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )

    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Avocados Sold",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    return price_chart_figure, volume_chart_figure



if __name__ == "__main__":
    app.run_server(debug=True)

