'''
    script hecho para crear funciones de modelado
'''

import pandas as pd
import numpy as np
import warnings
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, explained_variance_score, r2_score
warnings.filterwarnings("ignore")

def calcular_importancia(set_entrenamiento: pd.DataFrame, modelo: RandomForestRegressor) -> pd.DataFrame:
    """
    Calcula la importancia de cada feature en un modelo de Random Forest Regressor.

    Parameters:
    set_entrenamiento (pd.DataFrame): DataFrame que contiene el conjunto de entrenamiento.
    modelo (RandomForestRegressor): Modelo de Random Forest Regressor que se utilizó para entrenar.

    Returns:
    pd.DataFrame: DataFrame que contiene la importancia de cada feature en el modelo.
    """
    # Saco las features más importantes
    importancias_features = modelo.feature_importances_

    # Obtengo el nombre de las features
    nombres_features = set_entrenamiento.columns

    # Me armo un dataframe
    importancias_df = pd.DataFrame(
        {'Feature': nombres_features, 'Importancia': importancias_features}
    )

    # Ordeno el dataframe por orden de importancia
    return importancias_df.sort_values('Importancia', ascending=False)


def mostrar_podio_MVP(df_base:pd.DataFrame,columna_temporadas:str, columna_nombre:str, 
                      columna_votos:str   ,temporada:int, y_pred, cant_jugadores:int):
    """
    Muestra el podio de los jugadores más valiosos (MVP) para una temporada específica, basado en las predicciones y los votos reales.

    Parameters:
    df_base (pd.DataFrame): El dataframe base que contiene los datos.
    columna_temporadas (str): El nombre de la columna que representa las temporadas.
    columna_nombre (str): El nombre de la columna que representa los nombres de los jugadores.
    columna_votos (str): El nombre de la columna que representa los votos recibidos por los jugadores.
    temporada (int): El número de la temporada para la cual se desea mostrar el podio.
    y_pred: Las predicciones realizadas para los jugadores.
    cant_jugadores (int): La cantidad de jugadores que se desean mostrar en el podio.

    Returns:
    pd.DataFrame: Un dataframe que muestra el podio de los jugadores más valiosos (MVP) para la temporada especificada, basado en las predicciones y los votos reales.
    """
    # Genero un dataframe donde guardo las predicciones y el valor real
    df_comp = df_base[[columna_temporadas, columna_nombre, columna_votos]]
    df_comp.loc[:, 'y_pred'] = y_pred.flatten()
    df_comp = df_comp.sort_values(by='y_pred', ascending=False)

    return df_comp[df_comp[columna_temporadas] == temporada].head(cant_jugadores)


def metricas_reg(v_real, v_pred):
    """
    Calcula métricas de regresión basadas en los valores reales y predichos.

    Parameters:
    v_real (pd.DataFrame): DataFrame que contiene los valores reales.
    v_pred (pd.DataFrame): DataFrame que contiene los valores predichos.

    Returns:
    pd.DataFrame: Un objeto DataFrame que contiene las métricas de regresión calculadas.
    """
    # Calculo las métricas de regresión
    r2_test = r2_score(v_real, v_pred)  # Coeficiente de determinación
    explained_variance_test = explained_variance_score(v_real, v_pred)  # Varianza explicada
    mse_test = mean_squared_error(v_real, v_pred)  # Error Cuadrático Medio
    rmse_test = np.sqrt(mse_test)  # Raíz del Error Cuadrático Medio

    # Creo un DataFrame con las métricas calculadas
    metrics_df = pd.DataFrame({
        'Métrica': ['Coeficiente de determinación (R²)', 'Varianza explicada', 'MSE (Error Cuadrático Medio)', 'RMSE (Raíz del Error Cuadrático Medio)'],
        'Valor': [r2_test, explained_variance_test, mse_test, rmse_test]
    })
    
    return metrics_df