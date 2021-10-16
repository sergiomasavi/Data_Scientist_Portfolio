import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_precio_energia_temporal(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['value'],
            mode='lines',
            name='Max Drawdown',
            line = dict(color='green', width=1)
            ),
    )

    fig.update_layout(height=600, 
                      width=1000, 
                      title_text='Precio (€) de la energía diario en el mercado eléctrico español')
    fig.update_traces(hovertemplate="%{y:.5f}")

    fig.update_yaxes(tickprefix="")

    fig.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    fig.show()