import textwrap
import os
import platform
import re

def paginar_articulos_api(data_frame, archivo_seleccionado):
    """
    Configuración para paginar por consola los articulos recuperados de Lens y OpenAlex
    """
    indice = 0
    ind_final = len(data_frame)
    
    while True:
        limpiar_consola()
        fila = data_frame.iloc[indice]
        
        ajuste_linea = textwrap.TextWrapper(width=70)
        titulo_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["title"])))
        autores_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["authors"])))
        resumen_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["abstract"])))
        campos_estudio_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["fields_of_study"])))
        palabras_clave_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["keywords"])))
        instituciones_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["institutions"])))
        
        fecha_og = safe_str(fila['publication_date'])
        match = re.match(r'\d{4}-\d{2}-\d{2}', fecha_og)
        fecha_limpia = match.group(0) if match else fecha_og
        
        print("\n" + "="*70)
        print(f"   {archivo_seleccionado} - Fila {indice + 1}/{ind_final}")
        print("=" * 70)
        print()
        
        print(f"ID:\n{safe_str(fila['id'])}")
        print(f"Título:\n{titulo_ajustado}")
        print(f"Autor/es:\n{autores_ajustado}")
        print(f"Fecha de Publicación:\n{fecha_limpia}")
        print(f"Resumen:\n{resumen_ajustado}")
        print(f"Tipo de publicación:\n{safe_str(fila['type'])}")
        print(f"País relacionado a noticia:\n{safe_str(fila['countries'])}")
        print(f"Campos de estudio:\n{campos_estudio_ajustado}")
        print(f"Palabras clave:\n{palabras_clave_ajustado}")
        print(f"Instituciones relacionadas:\n{instituciones_ajustado}")
        print("\n" + "=" * 70)
        print("Controles: \n [s]: Siguiente \n [a]: Anterior \n [c] Cerrar")
        
        control = input("-> ").strip().lower()
        if control == "s" and indice < ind_final - 1:
            indice += 1
        elif control == "a" and indice > 0:
            indice -= 1
        elif control == "c":
            break
        
def paginar_feriasyeventos_csv(data_frame, archivo_seleccionado):
    """
    Configuración para paginar por consola los articulos recuperados de 10times, nferias y eventseye
    """
    indice = 0
    ind_final = len(data_frame)
    
    while True:
        limpiar_consola()
        fila = data_frame.iloc[indice]
        
        ajuste_linea = textwrap.TextWrapper(width=70)
        
        nombre_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Nombre del evento"])))
        descripcion_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Descripción"])))
        fechas_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Fecha"])))
        ubicaciones_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Ubicación"])))
        industrias_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Sector / industrias relacionadas"])))
        paginas_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Web oficial"])))
        contactos_ajustado = "\n".join(ajuste_linea.wrap(safe_str(fila["Correo de contacto"])))
        
        print("\n" + "="*70)
        print(f"   {archivo_seleccionado} - Fila {indice + 1}/{ind_final}")
        print("=" * 70)
        print()
        
        print(f"Nombre de evento:\n{nombre_ajustado}")
        print(f"Descripción:\n{descripcion_ajustado}")
        print(f"Fechas:\n{fechas_ajustado}\n")
        print(f"Ubicaciones:\n{ubicaciones_ajustado}\n")
        print(f"Sector / Industrias asociadas:\n{industrias_ajustado}")
        print(f"Página web:\n{paginas_ajustado}")
        print(f"Contacto:\n{contactos_ajustado}")
        print("\n" + "=" * 70)
        print("Controles: \n [s]: Siguiente \n [a]: Anterior \n [c] Cerrar")
        
        control = input("-> ").strip().lower()
        if control == "s" and indice < ind_final - 1:
            indice += 1
        elif control == "a" and indice > 0:
            indice -= 1
        elif control == "c":
            break

def paginar_noticias_csv(data_frame, archivo_seleccionado):
    """
    Configuración para paginar por consola las noticias recuperadas de feeds RSS.
    """
    indice = 0
    ind_final = len(data_frame)
    
    while True:
        limpiar_consola()
        fila = data_frame.iloc[indice]
        
        ajuste_linea = textwrap.TextWrapper(width=70)
        titulo_ajustado = "\n".join(ajuste_linea.wrap(fila["title"]))
        resumen_ajustado = "\n".join(ajuste_linea.wrap(fila["summary"]))
        
        fecha_og = fila['publication_date']
        match = re.match(r'[A-Za-z]{3},\s\d{2}\s[A-Za-z]{3}\s\d{4}', fecha_og)
        fecha_limpia = match.group(0) if match else fecha_og
        
        print("\n" + "="*70)
        print(f"   {archivo_seleccionado} - Fila {indice + 1}/{ind_final}")
        print("=" * 70)
        print()

        print(f"Fuente:\n{fila['source']}")
        print(f"Título:\n{titulo_ajustado}")
        print(f"Resumen:\n{resumen_ajustado}")
        print(f"Fecha de Publicación:\n{fecha_limpia}")
        print(f"País relacionado a noticia:\n{fila['country']}")
        print("\n" + "=" * 70)
        print("Controles: \n [s]: Siguiente \n [a]: Anterior \n [c] Cerrar")
        
        control = input("-> ").strip().lower()
        if control == "s" and indice < ind_final - 1:
            indice += 1
        elif control == "a" and indice > 0:
            indice -= 1
        elif control == "c":
            break
        
def limpiar_consola():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        
def safe_str(value):
    if isinstance(value, float):
        return ""
    if value is None:
        return ""
    return str(value)