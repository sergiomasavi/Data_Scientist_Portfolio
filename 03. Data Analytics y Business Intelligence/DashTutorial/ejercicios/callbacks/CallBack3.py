import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
# imports for pandas
import pandas as pd
import dash_table


df = pd.read_excel('Portfolio.xlsx',sheet_name = 'Datos')


app = dash.Dash()
app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Dropdown(
                id='drop_down',
                options=[{'label':'PER', 'value':'PER'},
                		{'label':'PB','value':'PB'},
                		{'label':'BETA','value':'BETA'},
                		{'label':'Precio', 'value':'Precio'}],
                value='Precio'
            ),
	dcc.Graph(
        id='my-graph'
    )]
	)

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='drop_down', component_property='value')
)
def callback_change_line(value):
    fig =  px.bar(df, x='Ticker' , y = value)
    fig.update_layout(transition_duration=500)
    return fig

	


if __name__ == '__main__':
	app.run_server(debug = True)


