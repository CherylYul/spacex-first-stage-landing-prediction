import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("dashboard/web-cleaned-data.csv")
max_payload = df["Payloadmass"].max()
min_payload = df["Payloadmass"].min()

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"font-size": "40px", "textAlign": "center", "color": "#404E7C"},
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCSFS SLC-40", "value": "CCSFS SLC-40"},
                {"label": "VSFB SLC-4E", "value": "VSFB SLC-4E"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
            ],
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
            style={
                "width": "80%",
                "padding": "5px auto",
                "font-size": "20px",
                "text-align-last": "center",
            },
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=18000,
            step=1000,
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(launch_site):
    if launch_site == "ALL":
        fig = px.pie(
            df, names="Boosterlanding", title="Landing status for all Launch sites"
        )
    else:
        df_launch_site = df.loc[df["Launchsite"] == launch_site]
        fig = px.pie(
            df_launch_site,
            names="Boosterlanding",
            title=f"Landing status for site {launch_site}",
        )
    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(launch_site, payload):
    df_payload = df.loc[df["Payloadmass"].between(payload[0], payload[1])]
    if launch_site == "ALL":
        fig = px.scatter(
            df_payload,
            x="Payloadmass",
            y="Boosterlanding",
            color="BoosterVersion",
            title="Landing status count on payload mass for all sites",
        )
    else:
        df_payload_launchsite = df_payload.loc[df_payload["Launchsite"] == launch_site]
        fig = px.scatter(
            df_payload_launchsite,
            x="Payloadmass",
            y="Boosterlanding",
            color="BoosterVersion",
            title=f"Landing status count on payload mass for site {launch_site}",
        )
    return fig


if __name__ == "__main__":
    app.run_server()
