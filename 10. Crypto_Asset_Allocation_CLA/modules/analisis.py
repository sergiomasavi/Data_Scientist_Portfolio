# Librerías
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import plotly
import plotly.graph_objects as go

def cargar_datos_vela(directory):
    """
    Cargar los ficheros csv de las divisas con las que se desea trabajar.

    Args:
    ----
        directory [{str}] -- Directorio que contiene el conjunto de ficheros csv.

    Returns:
    -----
        data [{dict}] -- Diccionario con la data cargada de los ficheros en el formato adecuado
    """

    # Variables
    directorios_csv = [directory + f for f in listdir(directory)]  # Lista de directorios de los ficheros .csv
    columns = ['Symbol', 'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume','close_change','volume_change' ]  # Columnas de interés

    # Variable de salida
    data = dict()

    # Bucle iterativo para cargar cada csv
    for filename in directorios_csv:
        if '.csv' in filename:
            # Lectura del dataframe
            df = pd.read_csv(filename, sep=';', encoding='utf-8-sig')

            # Obtenemos el nombre de la divisa
            currency_name = filename.split('_1h.csv')[0].split('/')[-1]

            # Añadir formato adecuado
            df['OpenTime'] = pd.to_datetime(df['OpenTime'], format='%Y-%m-%d %H:%M:%S')
            df['CloseTime'] = pd.to_datetime(df['CloseTime'], format='%Y-%m-%d %H:%M:%S')

            # Añadir información relevante
            df['close_change'] = df['Close'].pct_change(periods=1)  # Cambio porcentual
            df['volume_change'] = df['Volume'].pct_change(periods=1)  # Cambio porcentual

            # Almacenamiento en el diccionario
            data[currency_name] = df[columns].dropna(axis=0)

            # Información del dataset
            first_dt = data[currency_name]['OpenTime'].min()
            last_dt = data[currency_name]['OpenTime'].max()

            features = data[currency_name].shape[1]
            samples = data[currency_name].shape[0]

            print(f'[{currency_name}] - From "{first_dt}" to "{last_dt}". Features = {features}. Samples = {samples}')

    return data

def obtener_periodo_comun(data):
    """
    Obtener periodo común de todos los datasets para poder compararlos entre
    si.

    Args:
    -----
        data [{dict}] -- Diccionario de pandas.DataFrame con los datos cargados del dataset.

    Returns:
    -----
        data_bis [{dict}] -- Diccionario con elementos comunes
    """

    fechas_iniciales = list()
    fechas_finales = list()

    # Bucle iterativo para entrar periodo
    for currency_name, df in data.items():
        # Información del dataset
        first_dt = df['OpenTime'].min()
        last_dt = df['OpenTime'].max()

        fechas_iniciales.append(first_dt)
        fechas_finales.append(last_dt)

    # Periodo común de las divisas
    fi = max(fechas_iniciales)
    ff = min(fechas_finales)

    # Bucle iterativo de almacenamiento
    data_bis = dict()
    for currency_name, df in data.items():
        df_periodo = df[(df['OpenTime'] >= fi) & (df['OpenTime'] <= ff)].copy()
        data_bis[currency_name] = df_periodo.copy()

        # Información del dataset
        first_dt = data_bis[currency_name]['OpenTime'].min()
        last_dt = data_bis[currency_name]['OpenTime'].max()

        features = data_bis[currency_name].shape[1]
        samples = data_bis[currency_name].shape[0]

        print(f'[{currency_name}] - From "{first_dt}" to "{last_dt}". Features = {features}. Samples = {samples}')

        # Establece OpenTime como indice
        data_bis[currency_name].set_index('OpenTime', inplace=True)

    return data_bis

def crear_portfolio(data, column):
    """
    Crear portfolio de una de las features para cada divisa.

    Args:
    -----
        data [{dict}] -- Diccionario de datos de las divisas
        column [{str}] -- Columna de interes

    Returns:
    -----
        df_portfolio [{pandas.DataFrame}] -- Portfolio de características donde cada columna corresponde con cada divsa
    """

    portfolio = dict()

    for currency_name, df in data.items():
        df_currency = df[column].copy()
        portfolio[currency_name] = df_currency

    df_portfolio = pd.DataFrame(portfolio)

    return df_portfolio