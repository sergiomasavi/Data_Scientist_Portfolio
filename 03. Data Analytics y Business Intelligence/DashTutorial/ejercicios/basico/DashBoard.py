import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# imports for pandas
import pandas as pd
import dash_table
# math
from math import log

df_posis = pd.read_excel('Portfolio.xlsx',sheet_name = 'Posiciones')
df_ts = pd.read_excel('Portfolio.xlsx',sheet_name = 'TS')
df_datos = pd.read_excel('Portfolio.xlsx',sheet_name = 'Datos')

# Calculo de la posicion agregada
total_portfolio = 0
len_ts = len(df_ts)-1
df_ts['Total'] = 0
df_posis['PosicionAct'] =0 

for i in range(len(df_posis)):
	cantidad_invertida = df_posis['Cantidad'][i] * df_ts[df_posis['Ticker'][i]][len_ts]
	total_portfolio += cantidad_invertida
	df_ts [f'{df_posis["Ticker"][i]} Acumulado'] = df_posis['Cantidad'][i] * df_ts[df_posis['Ticker'][i]]
	df_ts['Total'] += df_ts [f'{df_posis["Ticker"][i]} Acumulado']
	df_posis['PosicionAct'][i] = cantidad_invertida

# Preparamos el grafico de evolucion de la cartera
fig_evolucion_total = px.line(df_ts, x='Fecha', y='Total')

fig_evolucion_total.update_layout(

)


# Preparamos el grafico de la distribucion de la cartera
fig_posiciones_actuales = px.pie(df_posis, values='PosicionAct', names='Ticker')

# Preparamos el grafico de la evolucion de cada accion
fig_evolucion_individual = px.line(df_ts, x='Fecha', y=['AMZN','TSLA','GE','SPY'])

# Preparamos el grafico de comparativa de Per
fig_per = px.bar(df_datos, x='PER', y='Ticker')

# Preparamos el grafico de comparativa de PB, Beta
fig_PB = px.bar(df_datos, x=['BETA','PB'], y='Ticker',barmode='group')




app = dash.Dash()


app.layout = html.Div(style = {'backgroundColor':'#e9edf6'},children =[
	html.Br(),
	html.Div([
		html.H3(children = 'Evolución de la Cartera', style ={'text-align':'center','padding': 10}),
		dcc.Graph(
        	id='ev_total',
        	figure=fig_evolucion_total)
		], style={'width': '48%', 'display': 'inline-block','padding': 10}),
	html.Div([
		html.H3(children = 'Composición de la Cartera', style ={'text-align':'center','padding': 10}),
		dcc.Graph(
        	id='pos_act',
        	figure=fig_posiciones_actuales)
		], style={'width': '48%', 'display': 'inline-block','padding': 10}),
	html.Br(),
	html.Div([html.H3(children = 'Componentes de la Cartera', style ={'text-align':'center','padding': 10}),html.Br(),html.Br(),
		dash_table.DataTable(
    		data=df_posis[['Ticker','PosicionAct']].to_dict('records'),
    		columns=[{'id': c, 'name': c} for c in df_posis[['Ticker','PosicionAct']].columns],
    		style_cell={'textAlign': 'center'},
    		style_table={'height': '300px'}
		,style_as_list_view=True)], style={'width': '48%', 'display': 'inline-block','padding': 10}),

	html.Div([html.H3(children = 'Información financiera de la Cartera', style ={'text-align':'center','padding': 10}),html.Br(),html.Br(),
		dash_table.DataTable(
    		data=df_datos.to_dict('records'),
    		columns=[{'id': c, 'name': c} for c in df_datos.columns],
    		style_cell={'textAlign': 'center'},
    		style_table={'height': '300px'}
		, style_as_list_view=True)], style={'width': '48%', 'display': 'inline-block','padding': 10}),
	html.Br(),
		html.Div([
		html.H3(children = 'Evolución de cada Acción', style ={'text-align':'center','padding': 10}),
		dcc.Graph(
        	id='ev_individual',
        	figure=fig_evolucion_individual)
		], style={'width': '48%', 'display': 'inline-block','padding': 10}),
	html.Div([
		html.H3(children = 'PER de cada Acción', style ={'text-align':'center','padding': 10}),
		dcc.Graph(
        	id='per',
        	figure=fig_per)
		], style={'width': '48%', 'display': 'inline-block','padding': 10}),
	html.Br(),
	html.Div([
		html.H3(children = 'PB / BETA de cada Acción', style ={'text-align':'center','padding': 10}),
		dcc.Graph(
        	id='pb',
        	figure=fig_PB)
		], style={'width': '98%', 'display': 'inline-block','padding': 10})		


        ])

if __name__ == '__main__':
	app.run_server(debug = True)
