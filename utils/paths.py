'''
    script hecho para el manejo de rutas
'''
import pyprojroot 


def crear_funcion_directorio(nombre_directorio:str):
    """
    Crea una función que genera rutas relativas a un directorio base.

    Parameters:
    nombre_directorio (str): El nombre del directorio base al que se generarán las rutas.

    Returns:
    function: Una función que toma argumentos variables y devuelve la ruta relativa al directorio base.
    """
    
    def funcion_directorio(*args:str):
        """
        Genera una ruta relativa al directorio base con los argumentos proporcionados.

        Parameters:
        *args (str): Argumentos variables que forman parte de la ruta relativa.

        Returns:
        Path: La ruta relativa al directorio base con los argumentos proporcionados.
        """
        return pyprojroot.here().joinpath(nombre_directorio, *args)

    return funcion_directorio

