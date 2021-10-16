# Librerías
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime

# Paquetes
from modules import analisis as anl
from modules.CriticalLineAlgorithm import *

# Configuración
pio.templates.default = "simple_white"

# 1. Lee los datos
data = anl.cargar_datos_vela(directory='data/')
# 2. Obtener periodo común
data = anl.obtener_periodo_comun(data=data)
# 3. Crear portfolio de rendimientos
df_ret = anl.crear_portfolio(data, 'close_change')
# 4. Crear portfolio close
df_close = anl.crear_portfolio(data, 'Close')

# 5. Variables de configuración
assets = df_ret.columns.tolist()
min_date = df_ret.index.min()
max_date = df_ret.index.max()

# Selecciona el color del header
COLOR_HEADER = "rgb(11, 217, 240)"

# Lista con los títulos y los filtros de la barra de la izquierda.
MENU = [
    html.P("Assets", className="title-filter"),
    dcc.Dropdown(
        id="asset-selector",
        options=[{"label": pair, "value": pair} for pair in assets],
        value=assets,
        multi=True,
        clearable=False,
    ),
    html.P("Dates", className="title-filter"),
    dcc.DatePickerRange(
        id="date-selector",
        start_date=min_date,
        min_date_allowed=min_date,
        end_date=max_date,
        max_date_allowed=max_date,
        initial_visible_month=min_date,
    ),
]

# Lista con los gráficos
GRAFICOS = [dcc.Graph(id="line-chart"), dcc.Graph(id="donut-chart")]

# Estructura de la app (no hace falta modificarla)
app = dash.Dash('Fays_Crypto_Investing')
app.layout = html.Div(
    children=[
        html.Div(
            id="header",
            children=[html.H1("Fays Crypto Investing Tool", id="title")],
            style={"background": COLOR_HEADER},
        ),
        html.Div(
            children=[
                html.Div(
                    id="menu",
                    children=MENU,
                ),
                html.Div(
                    id="graphs",
                    children=GRAFICOS,
                ),
            ],
            id="content",
        ),
    ],
    id="wrapper",
)


# Callback que actualiza los gráficos
@app.callback(
    [Output("line-chart", "figure"), Output("donut-chart", "figure")],
    [
        Input("asset-selector", "value"),
        Input("date-selector", "start_date"),
        Input("date-selector", "end_date"),
    ],
)
def update_graphs(selected_assets, start_date, end_date):
    # Dataframe de visualización.
    df_close_ = df_close.loc[start_date:end_date][selected_assets]
    df_line = df_close_ / df_close_.iloc[0]

    # Calcular distribución de inversión con Critical Line Algorithm (Markowithz)
    cla = CLA()
    df_cla = df_ret.loc[start_date:end_date][selected_assets]
    cla.allocate(asset_prices=df_cla, resample_by='W', solution='min_volatility')  # Retornos semanales
    cla_weights = cla.weights.sort_values(by=0, ascending=False, axis=1)
    cla_weights = cla_weights.T
    cla_weights.columns = ['Allocation']
    cla_weights.index.name = 'Asset'

    #df_donut = df[(filter_region) & (filter_type) & (filter_date)][
    #    ["region", "Total Volume"]
    #]
    #df_donut = df_donut.groupby("region").sum().reset_index()

    # Create figures
    #fig_donut = px.pie(
    #    data_frame=df_donut,
    #    names="region",
    #    values="Total Volume",
    #    hole=0.5,
    #    title="Total Volume per Region",
    #)

    # Visualización 1. Line plot
    fig_line = px.line(df_line, title='Normalized historical price trend', labels={"AveragePrice": "", "Date": ""})
    fig_line.update_traces(hovertemplate="$%{y:.2f}")
    fig_line.update_yaxes(tickprefix="$")
    fig_line.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )
    fig_line.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    # Visualización 2. Donut
    df_donut = cla_weights.reset_index()
    fig_donut = px.pie(data_frame=df_donut, values="Allocation", names="Asset", hole=0.5, title="Asset Daily Allocation")

    return fig_line, fig_donut


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
