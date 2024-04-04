'''
    script hecho para el manejo de rutas
'''
import pyprojroot #Librería para el menejo de rutas relativas

#Esta función se encarga de generar "accesos directos" a carpetas del proyecto
def crear_funcion_directorio(nombre_directorio:str):
    
        def funcion_directorio(*args:str):
            
            return pyprojroot.here().joinpath(nombre_directorio, *args)

        return funcion_directorio

