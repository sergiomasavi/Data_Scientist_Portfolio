import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# imports for pandas
import pandas as pd


app = dash.Dash()

df = pd.read_excel('Clase1_Datos.xlsx',sheet_name = 'Tarta')

fig = px.sunburst(df, path=['Continente', 'Nacionalidad'], values='Alumnos', hover_data=['Alumnos'])
app.layout = html.Div([
	html.H1(children = 'Mi Gráfico'),
	dcc.Graph(
        id='graph',
        figure=fig
    )]
	)

if __name__ == '__main__':
	app.run_server(debug = True)