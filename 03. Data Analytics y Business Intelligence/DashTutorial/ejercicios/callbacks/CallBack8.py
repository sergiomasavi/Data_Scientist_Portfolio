import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
# imports for pandas
import pandas as pd

df = pd.read_csv('heart.csv')

app = dash.Dash()
app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Dropdown(
        id = 'my-dropwdown',
        options=[
            {'label': 'thal', 'value': 'thal'},
            {'label': 'ca', 'value': 'ca'}

        ],
        value='thal'
    ),

	dcc.Graph(
        id='graph'
    )])

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='my-dropwdown', component_property='value')    
)
def callback_plot(columna):
    my_list = []

    for cat in df[columna].unique():
        my_list.append(1 - df[df[columna]==cat]['target'].sum()/len(df[df[columna]==cat]))

    fig =  px.bar(x = df[columna].unique(), y = my_list)
   
    fig.update_layout(transition_duration=500, xaxis_title = columna, yaxis_title = 'P de supervivencia')
    return fig

if __name__ == '__main__':
	app.run_server(debug = True)