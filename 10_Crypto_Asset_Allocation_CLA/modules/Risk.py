# Librerías
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from plotly.subplots import make_subplots
import warnings
import numpy as np
import scipy.stats # skewness and kurtosis
from scipy.stats import norm
from scipy.optimize import minimize

def bar_sharpe_ratio(df_bar, plot=True):
    """
    Visualización BarChar del niel de permanencia por región:

        - (1) Fidelización baja. Aquellos clientes que permanencen en el registro entre 0 y 6 meses.
        - (2) Fidelización media. Aquellos clientes que permanecen en el registro entre 7 y 10 meses.
        - (3) Fidelización alta. Aquellos clientes que permanecen en el registro entre 11 y 15 meses.
        - (4) Fidelización completa. Aquellos clientes que permanencen en el registro entre 16 y 17 meses.

    Args:
        df_bar [{pandas.DataFrame}] -- DataFrame del df_bar

    Returns:

    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_bar['symbol'],
        y=df_bar['sharpe_ratio'],
        name='Sharpe Ratio'
    ))

    fig.update_layout(title_text="Sharpe Ratio", yaxis_title='SR')
    fig.update_traces(hovertemplate="%{y:.2f}")

    fig.update_xaxes(
        showspikes=True, spikethickness=2, spikecolor="#999999", spikemode="across"
    )

    fig.update_layout(
        hovermode="x unified",
        hoverdistance=200,
        spikedistance=200,
        transition_duration=500,
    )

    if plot:
        fig.show()
    else:
        return fig

def annualize_rets(r, periods_per_year):
    """
    Computar la anualización de un conjunto de rendimientos.

    Args:
    -----
    r [{}] --
    periods_per_year [{}] --


    Returns:
    -----


    """
    compounded_growth = (1 + r).prod()
    n_periods = r.shape[0]
    annualize_returns = compounded_growth ** (periods_per_year / n_periods) - 1
    return annualize_returns

def annualize_vol(r, periods_per_year):
    """
    Computar la volatilidad anualizada de un conjunto de rendimientos

    Args:
    -----
    r [{}] --
    periods_per_year [{}] --


    Returns:
    -----

    """
    annualize_volatility = r.std() * periods_per_year ** 0.5
    return annualize_volatility

def sharpe_ratio(r, risk_free_rate, periods_per_year):
    """
    Computar el sharpe ratio anualizado de un conjunto de rendimientos.

    Args:
    -----

    r [{}] --
    periods_per_year [{}] --
    risk_free_rate [{float}] -- Tasa libre de riesgo.




    Returns:
    -----

    """

    # Convertir la tasa libre de riesgo
    rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    ann_vol = annualize_vol(r, periods_per_year)

    return ann_ex_ret / ann_vol

def drawdown(stock_returns: pd.Series, capital_inicial: float):
    """
    Toma una serie temporal de rendimientos de activos y devuelve un DataFrame
    con columnas para:
        - El índice de riqueza (wealth index).
        - Picos anteriores (previous peak).
        - El drowdown porcentual.

    Args:
    ------
    stock_returns [{pandas.Series}] -- Serie de retornos de un activo.

    Returns:
    ------
    df_drawdowns [{pandas.DataFrame}] -- Dataframe de drawdowns cuyas columnas
                                         corresponden con el índice de riqueza,
                                         los picos previos y el drawdown.
    """
    df_drawdowns = pd.DataFrame()

    #  Calcular índice de riqueza = Crecimiendo de cada unidad monetaria del capital inicial
    df_drawdowns['Wealth_Index'] = capital_inicial * (1 + stock_returns).cumprod()

    # Calcular picos previos
    df_drawdowns['Previous_Peaks'] = df_drawdowns['Wealth_Index'].cummax()

    # Calcular drowdown en valor porcentual
    df_drawdowns['Drawdown'] = (df_drawdowns['Wealth_Index'] - df_drawdowns['Previous_Peaks']) / df_drawdowns[
        'Previous_Peaks']

    return df_drawdowns

def get_coins_max_drawdown(drw):
    """
    FALTA DESCRIBIR LA FUNCIÓN
    """
    max_drw = dict()

    for currency_name in drw.columns.to_list():
        curr_drawdowns = drw[currency_name].copy()
        md = max_drawdown(drawdowns=curr_drawdowns)
        max_drw[currency_name] = md

    df_mdrw = pd.DataFrame(max_drw).T
    df_mdrw.columns = ['MaxDrawdown', 'Date']
    df_mdrw['MaxDrawdown'] = df_mdrw['MaxDrawdown'].apply(np.abs)
    return df_mdrw

def max_drawdown(drawdowns):
    """
    Calcular Max Drawdown a partir de la serie temporal de drawdowns para
    delvolver su valor y su marca temporal

    Args:
    -----
    drawdowns [{pandas.Series}] -- Drawdowns
    """
    # Calcular Max Drawdown
    max_drawdown = drawdowns.min()
    date_max_drawdown = drawdowns.idxmin()

    return max_drawdown, date_max_drawdown.strftime('%Y-%m-%d %H:%M:%S')

def plot_drawdowns(df_drawdowns, title):
    """
    Visualización drawdowns con plotly.

    Args:
    -----
    df_drawdowns [{pandas.DataFrame}] -- DataFrame de drawdowns resultados de
                                         aplicar la función drawdowns(...)
    title [{str}] -- Título del gráfico

    Returns:
    ------
    None
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    #  Formatear columna de marca temporal
    df_drawdowns['date_time'] = df_drawdowns.index
    df_drawdowns['date_time'] = df_drawdowns['date_time'].apply(str)
    df_drawdowns.reset_index(drop=True, inplace=True)
    df_drawdowns['date_time'] = pd.to_datetime(df_drawdowns['date_time'], format='%Y-%m')
    df_drawdowns.set_index('date_time', inplace=True)

    fig.add_trace(
        go.Scatter(
            x=df_drawdowns.index,
            y=df_drawdowns['Wealth_Index'],
            mode='lines',
            name='Wealth Index',
            line=dict(color='blue', width=1)

        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df_drawdowns.index,
            y=df_drawdowns['Previous_Peaks'],
            mode='lines',
            name='Previous Peaks',
            line=dict(color='green', width=2, dash='dot')
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df_drawdowns.index,
            y=df_drawdowns['Drawdown'],
            mode='lines',
            name='Drawdown',
            line=dict(color='red', width=1)
        ),
        row=2,
        col=1
    )

    # Calcular max drawdown
    date_max_drawdown = df_drawdowns["Drawdown"].idxmin()
    max_drawdown = df_drawdowns.loc[date_max_drawdown]['Drawdown']

    df_drawdowns['MaxDrawdown'] = np.nan
    df_drawdowns.loc[date_max_drawdown, 'MaxDrawdown'] = max_drawdown

    fig.add_trace(
        go.Scatter(
            x=df_drawdowns.index,
            y=df_drawdowns['MaxDrawdown'],
            mode='markers',
            name='Max Drawdown',
            marker=dict(
                color='black',
                size=10,
                opacity=0.8,
                symbol='triangle-up'
            )),
        row=2,
        col=1
    )

    fig.update_layout(height=600, width=1000, title_text=title)
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
