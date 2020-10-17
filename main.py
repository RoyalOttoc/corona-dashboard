import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df, totals_df
from builders import make_table

stylesheets = ["https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
               "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap", ]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

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
                # html.Div(children=[make_table(countries_df)]),
            ]
        ),
    ],
)

map_figure = px.scatter_geo(countries_df)

if __name__ == "__main__":
    app.run_server(debug=True)
