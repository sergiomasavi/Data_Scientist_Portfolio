import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# imports for pandas
import pandas as pd

df = pd.read_excel("Clase1_Datos.xlsx", sheet_name="Histograma1")
fig = px.histogram(df, x="Edades", histnorm="probability density")


app = dash.Dash()
app.layout = html.Div(
    [html.H1(children="Mi Gráfico"), dcc.Graph(figure=fig, id="line")]
)


if __name__ == "__main__":
    app.run_server(debug=True)
