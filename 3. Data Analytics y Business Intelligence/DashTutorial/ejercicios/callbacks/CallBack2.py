import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
# imports for pandas
import pandas as pd
import dash_table


df_sp = pd.read_excel('SPY.xlsx',sheet_name = 'Sheet1')
df_tsla = pd.read_excel('tesla.xlsx',sheet_name = 'Sheet1')


app = dash.Dash()

app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Dropdown(
                id='drop_down_column',
                options=[{'label':'Open', 'value':'Open'},
                		{'label':'High','value':'High'},
                		{'label':'Close','value':'Close'},
                		{'label':'Low', 'value':'Low'}],
                value='Close'
            ),
    dcc.Dropdown(
                id='drop_down_company',
                options=[{'label':'TSLA', 'value':'TSLA'},
                        {'label':'SPY','value':'SPY'}],
                value='SPY'
            ),
	dcc.Graph(
        id='my-graph'
    )]
	)

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='drop_down_column', component_property='value'),
    Input(component_id='drop_down_company', component_property='value'))
def callback_change_line(column, stock):
    if stock == 'SPY':
        df = df_sp
    else: 
        df = df_tsla

    fig =  px.line(df, x='Date', y = column)
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
	app.run_server(debug = True)