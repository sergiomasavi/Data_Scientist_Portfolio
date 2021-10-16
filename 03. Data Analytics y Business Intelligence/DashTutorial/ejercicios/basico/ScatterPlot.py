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
fig = px.scatter(df, x='Range High-Low', y='Range Open-Close',size='Volume')

app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Graph(
        id='graph',
        figure=fig
    )]
	)

if __name__ == '__main__':
	app.run_server(debug = True)