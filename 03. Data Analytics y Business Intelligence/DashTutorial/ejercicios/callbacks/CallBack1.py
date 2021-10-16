import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
# imports for pandas
import pandas as pd


df = pd.read_excel('SPY.xlsx',sheet_name = 'Sheet1')

# Preparamos el grafico de la evolucion de cada accion
fig = px.line(df, x='Date', y='Close')

app = dash.Dash()

app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Dropdown(
                id='drop_down',
                options=[{'label':'Open', 'value':'Open'},
                		{'label':'High','value':'High'},
                		{'label':'Close','value':'Close'},
                		{'label':'Low', 'value':'Low'}],
                value='Close'
            ),
	dcc.Graph(
        id='my-graph'
    )]
	)

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='drop_down', component_property='value')

)
def callback_change_line(column):
	fig =  px.line(df, x='Date', y = column)
	fig.update_layout(transition_duration=500)
	return fig

if __name__ == '__main__':
	app.run_server(debug = True)

