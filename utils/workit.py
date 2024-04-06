'''
    script hecho para el trabajo con los dataframes
'''
import numpy as np
import pandas as pd


def eliminar_columnas_comunes(df_a_modificar:pd.DataFrame, df_sin_modificar:pd.DataFrame, columnas_ignorar:list) -> pd.DataFrame:
    """
    Elimina las columnas comunes del dataframe que se quiere modificar, manteniendo las columnas especificadas para ignorar.

    Parameters:
    df_a_modificar (pd.DataFrame): El dataframe que se quiere modificar.
    df_sin_modificar (pd.DataFrame): El dataframe que se utiliza como referencia para identificar las columnas comunes.
    columnas_ignorar (list): Lista de nombres de columnas que se quieren mantener en el dataframe resultante.

    Returns:
    pd.DataFrame: Un nuevo dataframe con las columnas comunes eliminadas y las columnas especificadas para ignorar añadidas de vuelta.
    """
    columnas_utiles = [columna for columna in list(df_a_modificar.columns) if columna not in list(df_sin_modificar.columns)]
    
    for columna in columnas_ignorar:
        columnas_utiles.append(columna)
        
    return df_a_modificar.drop([columna for columna in list(df_a_modificar.columns) if columna not in columnas_utiles], axis = 1)
        
def columnas_con_valores_faltantes(df, n=10):
    """
    Encuentra las columnas con la mayor cantidad de valores faltantes en un DataFrame.

    Parameters:
    df (pd.DataFrame): El DataFrame en el que se buscarán los valores faltantes.
    n (int): El número de columnas con más valores faltantes para devolver (por defecto 10).

    Returns:
    list: Una lista de las n columnas con más valores faltantes, ordenadas por la cantidad de valores faltantes.
    """
    # Calcula la cantidad de valores faltantes en cada columna
    faltantes_por_columna = df.isnull().sum()

    # Ordena las columnas por la cantidad de valores faltantes
    columnas_ordenadas = faltantes_por_columna.sort_values(ascending=False)

    # Devuelve las n columnas con más valores faltantes
    return columnas_ordenadas.head(n).index.tolist()

def tomar_jugadores_con_votos(df:pd.DataFrame, columna_votos:str, columna_nombre:str) -> pd.DataFrame:
    """
    Filtra el DataFrame para tomar solo las filas de jugadores que tienen valores en la columna de votos, y devuelve un nuevo DataFrame con esas filas.

    Parameters:
    df (pd.DataFrame): El DataFrame del que se tomarán las filas.
    columna_votos (str): El nombre de la columna que contiene los votos.
    columna_nombre (str): El nombre de la columna que contiene los nombres de los jugadores.

    Returns:
    pd.DataFrame: Un nuevo DataFrame que contiene solo las filas de jugadores que tienen valores en la columna de votos.
    """
    # Me quedo con las filas con valores en la columna de interés
    df_jugadores_votados = df[df[columna_votos].notna()]

    # Armo una lista con los nombres de las instancias tomadas
    jugadores_con_votos = df_jugadores_votados[columna_nombre].unique()

    # Me quedo con las instancias cuyo nombre está en la lista
    return df[df[columna_nombre].isin(jugadores_con_votos)]

def crear_df_jugador(jugador:str,columna_nombre:str ,df:pd.DataFrame) -> pd.DataFrame:
    """
    Crea un DataFrame que contiene la información del jugador especificado.

    Parameters:
    jugador (str): El nombre del jugador del que se desea obtener la información.
    columna_nombre (str): El nombre de la columna que contiene los nombres de los jugadores en el DataFrame original.
    df (pd.DataFrame): El DataFrame del que se extraerá la información del jugador.

    Returns:
    pd.DataFrame: Un nuevo DataFrame que contiene la información del jugador especificado.
    """
    df_info_jugador = df[df[columna_nombre] == jugador]
    return df_info_jugador

def filtrar_temporadas_jugador(df_jugador, columna_temporadas:str, columna_filtro:str) -> pd.DataFrame:
    """
    Filtra el DataFrame del jugador para incluir solo las temporadas de interés, basándose en un criterio definido por las columnas especificadas.

    Parameters:
    df_jugador (pd.DataFrame): El DataFrame del jugador del que se filtrarán las temporadas.
    columna_temporadas (str): El nombre de la columna que contiene la información de las temporadas.
    columna_filtro (str): El nombre de la columna que se utilizará como criterio de filtro.

    Returns:
    pd.DataFrame: Un nuevo DataFrame que contiene solo las filas correspondientes a las temporadas de interés, según el criterio definido.
    """
    # Inicializa una lista para almacenar las temporadas de interés
    temporadas_interesantes = []

    # Itera sobre cada fila del DataFrame del jugador
    for index, fila in df_jugador.iterrows():
        # Verifica si la fila tiene un valor no nulo en la columna de filtro
        if not pd.isna(fila[columna_filtro]):
            # Utiliza el criterio para determinar las temporadas de interés
            temporada_actual = fila[columna_temporadas]
            temporada_anterior = temporada_actual - 1
            temporada_siguiente = temporada_actual + 1

            # Agrega las temporadas a la lista de temporadas de interés
            temporadas_interesantes.append(temporada_actual)

            # Verifica si la temporada anterior está dentro del rango de temporadas del jugador
            if temporada_anterior >= df_jugador[columna_temporadas].min():
                temporadas_interesantes.append(temporada_anterior)

            # Verifica si la temporada siguiente está dentro del rango de temporadas del jugador
            if temporada_siguiente <= df_jugador[columna_temporadas].max():
                temporadas_interesantes.append(temporada_siguiente)

    # Aplica el filtro al DataFrame del jugador para incluir solo las temporadas de interés
    filtro_temporadas_interesantes = df_jugador[columna_temporadas].isin(temporadas_interesantes)
    jugador_filtrado = df_jugador[filtro_temporadas_interesantes]

    return jugador_filtrado

def generar_df_mvp(df:pd.DataFrame, columna_nombre:str, columna_votos:str, columna_temporadas:str) -> pd.DataFrame:
    """
    Genera un DataFrame con la información de los jugadores que han recibido votos para el MVP en diferentes temporadas.

    Parameters:
    df (pd.DataFrame): El DataFrame original que contiene la información de los jugadores.
    columna_nombre (str): El nombre de la columna que contiene los nombres de los jugadores.
    columna_votos (str): El nombre de la columna que contiene los votos de los jugadores.
    columna_temporadas (str): El nombre de la columna que contiene la información de las temporadas.

    Returns:
    pd.DataFrame: Un nuevo DataFrame que contiene la información de los jugadores que han recibido votos para el MVP en diferentes temporadas.
    """
    
    #Selecciono a los jugadores con votos
    df = tomar_jugadores_con_votos(df, columna_votos, columna_nombre)
    
    #Armo la lista de nombres
    jugadores_unicos = df[columna_nombre].unique()  # Obtiene la lista de jugadores únicos

    #Inicializo un conjunto de datos vacio donde se almacenará el resultado
    resultado_final = pd.DataFrame()

    #Itero sobre la lista de jugadores únicos
    for jugador in jugadores_unicos:
        jugador_filtrado = filtrar_temporadas_jugador(crear_df_jugador(jugador, columna_nombre, df), columna_temporadas, columna_votos)
        resultado_final = pd.concat([resultado_final, jugador_filtrado])

    return resultado_final
    
    



