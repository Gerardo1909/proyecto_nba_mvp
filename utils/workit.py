'''
    script hecho para el trabajo con los dataframes
'''
import numpy as np
import pandas as pd
import inspect

def get_dataframe_name(df):
    # Inspecciona el marco de la pila para obtener el nombre del DataFrame
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    for var_name, var_val in callers_local_vars:
        if isinstance(var_val, pd.DataFrame) and var_val is df:
            return var_name
    return None

def imprimir_columnas(df):
    
    titulo = get_dataframe_name(df)
    columnas = df.columns
    
    print(f'{titulo}:')
    print(list(columnas))
    print()

