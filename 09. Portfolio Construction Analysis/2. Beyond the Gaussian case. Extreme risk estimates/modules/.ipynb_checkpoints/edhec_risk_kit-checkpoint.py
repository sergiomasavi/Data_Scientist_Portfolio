# -*- coding: utf-8 -*-
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# Librerías
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from plotly.subplots import make_subplots
import warnings
import numpy as np


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

    return max_drawdown, date_max_drawdown.strftime('%Y-%m')

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
    fig = make_subplots(rows=2, cols=1)

    # Formatear columna de marca temporal
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
            line = dict(color='blue', width=1)
            
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
            line = dict(color='green', width=2, dash='dot')
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
            line = dict(color='red', width=1)
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

def drawdown(stock_returns: pd.Series, capital_inicial:float):
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
    
    # Calcular índice de riqueza = Crecimiendo de cada unidad monetaria del capital inicial
    df_drawdowns['Wealth_Index'] = capital_inicial*(1 + stock_returns).cumprod() 
    
    # Calcular picos previos
    df_drawdowns['Previous_Peaks'] = df_drawdowns['Wealth_Index'].cummax()
    
    # Calcular drowdown en valor porcentual
    df_drawdowns['Drawdown'] = (df_drawdowns['Wealth_Index'] - df_drawdowns['Previous_Peaks'])/df_drawdowns['Previous_Peaks']
    
    return df_drawdowns

def get_ffme_returns(directory):
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    filename =f'{directory}/Portfolios_Formed_on_ME_monthly_EW.csv'
    
    me_m = pd.read_csv(filename,
                       header=0, index_col=0, na_values=-99.99)


    # Formato de la marca temporal
    series_date_time =  list()
    for date_value in me_m.index:
        date_value = str(date_value)
        date_value = f'{date_value[:4]}-{date_value[4:]}'
        series_date_time.append(date_value)


    series_date_time = np.array(series_date_time)
    me_m.index=series_date_time
    me_m.index = pd.to_datetime(me_m.index)

    rets = me_m[['Lo 10', 'Hi 10']]
    rets.columns = ['SmallCap', 'LargeCap']
    rets = rets/100
    
    return rets


def kurtosis(r):
    """
    Alternativa a scipy.stats.skew()
    
    Calcula la kurtosis de una serie temporal de rendimientos de entrada
    
    Args:
    -----
    r {[pandas.Series or pandas.DataFrame]} -- Serie temporal de rendimientos
    
    
    Returns:
    -----
    kurtosis {[float or Series]} -- Valor de kurtosis
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0) # population standard deviation (ddof=0)
    exp_demeaned_r = (demeaned_r**4).mean()
    kurtosis = exp_demeaned_r/sigma_r**4
    return kurtosis


def skewness(r):
    """
    Alternativa a scipy.stats.skew()
    
    Calcula la asimetría de una serie temporal de rendimientos de entrada
    
    Args:
    -----
    r {[pandas.Series or pandas.DataFrame]} -- Serie temporal de rendimientos
    
    
    Returns:
    -----
    skewness {[float or Series]} -- Valor de asimetría
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0) # population standard deviation (ddof=0)
    exp_demeaned_r = (demeaned_r**3).mean()
    skewness = exp_demeaned_r/sigma_r**3
    return skewness


def is_normal(r, level=0.01):
    """
    Aplica el test de Jarque-Bera para determinar si una Serie es normal o no
    
    
    Args:
    ------
    r {[pandas.Series]} -- Serie temporal de rendimientos
    level {[float]} -- Nivel de confianza del test. La prueba se aplica por defecto al nivel del 1%


    Returns:
    ---------
    aceptar_hipotesis {[bool]} -- Devuelve Verdadero si se acepta la hipótesis de normalidad, Falso en caso contrario
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(is_normal)
    else:
        statistic, p_value = scipy.stats.jarque_bera(r)
        return p_value > level
    
    return p_value > level


def get_hfi_returns(directory):
    """
    Load and format the EDHEC Hedge Fund Index Returns
    """
    filename = directory + 'edhec-hedgefundindices.csv'
    hfi = pd.read_csv(filename,
                      header=0, index_col=0, parse_dates=True)
    hfi = hfi/100
    hfi.index = hfi.index.to_period('M')

    return hfi
