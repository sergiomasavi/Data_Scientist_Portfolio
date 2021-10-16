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
            {'label': 'Male', 'value': 'male'},
            {'label': 'Female', 'value': 'female'}

        ],
        value='male'
    ),

	dcc.Graph(
        id='graph'
    )])

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='my-dropwdown', component_property='value')
    
)
def callback_plot(genero):
    #age
    #chol
    #target
    if genero == 'male':
        df_ = df[df['sex']==1]
    else: 
        df_ = df[df['sex']==0]
    fig =  px.scatter(df_, x = 'age', y = 'chol', color = 'target')
   
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
	app.run_server(debug = True)