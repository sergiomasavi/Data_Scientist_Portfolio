import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
# imports for pandas
import pandas as pd


app = dash.Dash()

df = pd.read_excel('Clase1_Datos.xlsx',sheet_name = 'Linea')
for c in ['Open','Close','Low','High', 'Volume','Adj Close']:
	df[c] = df[c].apply(lambda x: round(x,2))

app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	html.Div(
	dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    style_cell={'textAlign': 'center'}

	), style={'width': '48%', 'display': 'inline-block'})
		]
	)

if __name__ == '__main__':
	app.run_server(debug = True)

