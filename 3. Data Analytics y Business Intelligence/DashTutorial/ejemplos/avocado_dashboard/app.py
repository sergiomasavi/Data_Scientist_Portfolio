import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.io as pio
import plotly.express as px
from datetime import datetime
from dash.dependencies import Input, Output

app = dash.Dash(name=__name__)

def load_data(filename):
    df = pd.read_csv(filename)
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    df.sort_values('Date', inplace=True, ascending=True)
    df.reset_index(inplace=True, drop=True)
    df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d')
    return df.copy()

def gen_fig_line(df, avocado_type, regions, start_date, end_date):

    df = df.copy()

    # Filtros
    selected_regions = df.region.unique()[:3]
    filter_region = df.region.isin(regions)
    filter_type = df.type == avocado_type
    filter_date = df.Date.between(start_date, end_date)
    df_line = df[(filter_region) & (filter_type) & (filter_date)]

    fig = px.line(df_line, x='Date', y='AveragePrice', color='region',
                  title='Average Price of Avocados per Region',
                  labels={'AveragePrice': '',
                          'Date': ''})

    fig.update_traces(hovertemplate='$%{y:.2f}')
    fig.update_yaxes(tickprefix='$')
    fig.update_xaxes(showspikes=True, spikethickness=1, spikecolor='#999999', spikemode='across')
    fig.update_layout(hovermode='x unified', hoverdistance=200, spikedistance=100)

    return fig

def gen_fig_donut(df, avocado_type, regions, start_date, end_date):
    df = df.copy()
    selected_regions = df.region.unique()[:3]
    filter_region = df.region.isin(regions)
    filter_type = df.type == avocado_type
    filter_date = df.Date.between(start_date, end_date)

    columns = ['region', 'Total Volume']
    df_donut = df[(filter_region) & (filter_type) & (filter_date)][columns]
    df_donut = df_donut.groupby('region').sum().reset_index()
    df_donut.head()

    fig = px.pie(data_frame=df_donut,
                 names='region',
                 values='Total Volume',
                 hole=0.5,
                 title='Total Volume per Region')
    return fig


df = load_data('data/avocado.csv')
avocado_types = df.type.unique()
regions = df.region.unique()[:3]
min_date = df.Date.min()
max_date = df.Date.max()

# Valores por defecto
avocado_type_default = 'conventional'
regions_default = ['Chicago', 'Southeast', 'HarrisburgScranton']
start_date_default = datetime(2015, 1, 1)
end_date_default = datetime(2016,1,1)

fig_line =gen_fig_line(df,avocado_type_default, regions_default, start_date_default, end_date_default)
fig_donut = gen_fig_donut(df, avocado_type_default, regions_default, start_date_default, end_date_default)

app.layout = html.Div(
    children=[
        html.Div(
            id='header',
            children=[
                html.Div(children=[html.H1('Avocados Prices and Volume', id='title')])],
                ),
        html.Div(
            id='menu',
            children=[
                dcc.RadioItems(
                    id='type-selector',
                    options=[{'label': t.title(), 'value':t} for t in avocado_types],
                    value=avocado_types[0]
                ),
                dcc.Dropdown(
                    id='region-selector',
                    options=[{'label':r, 'value':r} for r in regions],
                    multi=True,
                    clearable=False,
                    value=regions
                ),
                dcc.DatePickerRange(
                    id='date-selector',
                    start_date=min_date,
                    end_date=max_date

                )
            ]
        ),
        html.Div(id='graphs', children=[dcc.Graph(id='line-chart', figure=fig_line),
                                        dcc.Graph(id='donut-chart', figure=fig_donut)])
    ],
    id='wrapper'
)

@app.callback(
    [
        Output('line-chart', 'figure'),
        Output('donut-chart', 'figure')
    ],
    [
        Input('type-selector', 'value'),
        Input('region-selector', 'value'),
        Input('date-selector','start_date'),
        Input('date-selector','end_date')
    ]
)
def update_graphs(avocado_type, regions, start_date, end_date):
    if len(regions)<1:
        regions = regions_default
    fig_line = gen_fig_line(df,avocado_type, regions, start_date, end_date)
    fig_donut = gen_fig_donut(df,avocado_type, regions, start_date, end_date)

    return fig_line, fig_donut

if __name__ =='__main__':
    app.run_server(debug=True)