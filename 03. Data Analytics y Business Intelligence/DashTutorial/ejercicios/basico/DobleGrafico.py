import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# imports for pandas
import pandas as pd


app = dash.Dash()

df = pd.read_excel('Clase1_Datos.xlsx',sheet_name = 'Linea')

df['Range High-Low'] = 100*(df['High']-df['Low'])/df['Low']
df['Range Open-Close'] = 100*(df['Close']-df['Open'])/df['Open']
fig_1 = px.scatter(df, x='Volume', y='Range High-Low')
fig_2 = px.scatter(df, x='Volume', y='Range Open-Close')

app.layout = html.Div([
	html.Div([
	html.H1(children = 'Gráfico Izquierda',style = {'textAlign': 'center'}),
	dcc.Graph(
        id='graph1',
        figure=fig_1
    )], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
		html.H1(children = 'Gráfico Derecha',style = {'textAlign': 'center'}),
	dcc.Graph(
        id='graph2',
        figure=fig_2
    )], style={'width': '48%', 'display': 'inline-block'})

	]
	)

if __name__ == '__main__':
	app.run_server(debug = True)