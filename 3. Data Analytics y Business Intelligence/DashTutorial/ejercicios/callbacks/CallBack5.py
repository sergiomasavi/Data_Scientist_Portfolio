import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
# imports for pandas
import pandas as pd
import dash_table


df_spy = pd.read_excel('SPY.xlsx',sheet_name = 'Sheet1')
df_tsla = pd.read_excel('tesla.xlsx',sheet_name = 'Sheet1')
df = {'SPY':df_spy,'TSLA':df_tsla}


app = dash.Dash()
app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Dropdown(
        id = 'my-dropwdown',
        options=[
            {'label': 'SPY', 'value': 'SPY'},
            {'label': 'TSLA', 'value': 'TSLA'}

        ],
        value='SPY'
    ),

    dcc.Checklist(
        id='my-checklist',
        options=[{'label':'Open', 'value':'Open'},
                {'label':'High','value':'High'},
                {'label':'Close','value':'Close'},
                {'label':'Low', 'value':'Low'}
        ],                
        value=['Close']
    ),

	dcc.Graph(
        id='my-graph'
    )]
	)

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my-dropwdown', component_property='value'),
    Input(component_id='my-checklist', component_property='value')
)
def callback_change_line(ticker,columnas):
    fig =  px.line(df[ticker], x='Date' , y = columnas)
    fig.update_layout(transition_duration=500)
    return fig

	


if __name__ == '__main__':
	app.run_server(debug = True)