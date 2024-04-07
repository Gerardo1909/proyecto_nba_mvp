'''
    script hecho para crear funciones de visualización
'''
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

def mirar_distribuciones_num(df:pd.DataFrame, tamanio:tuple, bins:int,  columnas_ignorar:list):
    """
    Visualiza la distribución de columnas numéricas en un DataFrame utilizando histogramas.

    Parameters:
    df (pd.DataFrame): El DataFrame de pandas de entrada.
    tamanio (tuple): Una tupla que especifica las dimensiones del gráfico (ancho, altura).
    bins (int): El número de contenedores a usar para los histogramas.
    columnas_ignorar (list): Una lista de nombres de columnas que se deben ignorar durante la visualización.

    Returns:
    None
    """
    #Saco las columnas a ignorar
    df_numericas_interes = df.select_dtypes(include=['int64', 'float64']).drop(columns=columnas_ignorar)

    # Ahora puedes trazar los histogramas para las columnas numéricas restantes
    df_numericas_interes.hist(bins=bins, figsize=tamanio, edgecolor='black')
    plt.tight_layout()
    

def graficar_relaciones(df:pd.DataFrame, tamanio:tuple, columna_objetivo:str, columnas_ignorar:list):
    """
    Visualiza las relaciones entre las columnas numéricas de interés y la columna objetivo mediante gráficos de dispersión.

    Parameters:
    df (pd.DataFrame): El DataFrame de pandas que contiene los datos.
    tamanio (tuple): Una tupla que especifica las dimensiones del gráfico (ancho, altura).
    columna_objetivo (str): El nombre de la columna que se utilizará como eje y en los gráficos de dispersión.
    columnas_ignorar (list): Una lista de nombres de columnas que se deben ignorar durante la visualización.

    Returns:
    None
    """
    
    # Selecciona solo las columnas numéricas de interés
    df_numericas_interes = df.select_dtypes(include=['int64', 'float64']).drop(columns=columnas_ignorar)

    # Crea la figura y los ejes
    fig, axes = plt.subplots(nrows=len(df_numericas_interes.columns), figsize=tamanio)

    # Itera sobre las columnas numéricas de interés
    for i, col in enumerate(df_numericas_interes.columns):
        # Trama de dispersión para cada columna numérica con 'columna_objetivo' en el eje y
        sns.scatterplot(x=col, y=columna_objetivo, data=df_numericas_interes, ax=axes[i])

    # Ajusta el diseño
    plt.tight_layout()
    
    