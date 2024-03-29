import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import plotly.express as px
from data import countries_df, totals_df, dropdown_options, make_global_df, make_country_df
from builders import make_table

stylesheets = ["https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
               "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap", ]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

server = app.server

bubble_map = px.scatter_geo(countries_df,
                            size="Confirmed",
                            size_max=40,
                            template="plotly_dark",
                            color_continuous_scale=px.colors.sequential.Oryel,
                            title="Confirmed By Country",
                            # projection="natural earth",
                            hover_name="Country_Region",
                            color="Confirmed",
                            locations="Country_Region",
                            locationmode="country names",
                            hover_data={
                                "Confirmed": ':,2f',
                                "Deaths": ':,2f',
                                "Recovered": ':,2f',
                                "Country_Region": False},

                            )
bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=0))

bars_graph = px.bar(totals_df,
                    x="condition",
                    y="count",
                    template="plotly_dark",
                    title="Total Global Cases",
                    labels={"condtion": "Condition",
                            "count": "Count"},
                    hover_data={
                        "count": ":,"
                    })
bars_graph.update_layout(
    xaxis=dict(title="Condition"),
    yaxis=dict(title="Count")
)

bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={"backgroundColor": "#111111", "minHeight": "100vh",
           "color": "white", "fontFamily": "Open Sans, sans-serif"},
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)]),
                html.Div(
                    style={"marginRight": "30px"},
                    children=[make_table(countries_df)]),
            ]
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {'label': country, 'value': country} for country in dropdown_options
                            ]),
                        dcc.Graph(
                            style={"marginRight": "30px"},
                            id="country_graph")

                    ]),
            ]
        ),
    ],
)


@app.callback(
    Output("country_graph", "figure"),
    [Input("country", "value")]
)
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()

    fig = px.line(df, x="date", y=["confirmed", "deaths", "recovered"],
                  template="plotly_dark", labels={
        "value": "Cases",
        "variable": "Condition",
        "date": "Date"
    },
        hover_data={
        "variable": False,
        "value": ':,'
    }
    )

    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig


map_figure = px.scatter_geo(countries_df)
