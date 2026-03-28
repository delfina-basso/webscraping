"""
Módulo de menú principal.
Gestiona la interfaz de consola y la navegación del usuario.
"""
from ..rss import procesador_de_feeds as pf
import os
import pandas as pd
from src.interfaz import paginacion_csv as pcsv
from ..api.open_alex import OpenAlexClient
from ..api.lens_org import LensClient, TOKEN_LENS
from ..scraping import eventseye
from ..scraping import nferias
from ..scraping import tentimes

def mostrar_menu_principal():
    """
    Muestra el menú principal y gestiona las opciones del usuario.
    """
    while True:
        pcsv.limpiar_consola()
        print("\n" + "=" * 70)
        print("  MENÚ PRINCIPAL")
        print("=" * 70)
        print("\nRecuperación de Información en la Web")
        print("-" * 70)
        print()
        
        print("1. Consultar artículos científicos (OpenAlex)")
        print("2. Consultar patentes (The Lens)")
        print("3. Consultar próximos eventos y ferias (Web Scraping)")
        print("4. Consultar últimas noticias (RSS)")
        print("5. Ver archivos CSV generados")
        print("6. Acerca de")
        print("7. Salir")
        print()

        opcion = input("Seleccione una opción [1-7]: ").strip()
        if opcion == "1":
            mostrar_submenu_openalex()
            print()
        
        elif opcion == "2":
            mostrar_submenu_thelens()
            print()
        
        elif opcion == "3":
            mostrar_submenu_scraping()
            print()
        
        elif opcion == "4":
            mostrar_submenu_rss()
            print()
        
        elif opcion == "5":
            ver_csv_generados()
        
        elif opcion == "6":
            mostrar_acerca_de()
            print()
        
        elif opcion == "7":
            confirmar = input("\n¿Está seguro que desea salir? [S/N]: ").strip().upper()
            if confirmar == "S":
                print("\n¡Gracias por usar el sistema!")
                print("Documentación disponible en carpeta 'docs'.")
                print("\n¡Hasta luego! 👋\n")
                print()
                break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción del 1 al 7.")
            print()
        
        input("\nPresiona Enter para continuar...")

def mostrar_submenu_openalex():
    """
    Muestra la interfaz para consultar artículos científicos (OpenAlex).
    """
    while True:
        pcsv.limpiar_consola()
        print("\n" + "=" * 70)
        print("  ARTÍCULOS CIENTÍFICOS")
        print("=" * 70)
        print()
        
        print("¿Quiéres consultar de un tema en particular? ¿O ver en general?")
        print()
        print("1. Elegir un tema")
        print("2. Consultar artículos en general")
        print("3. Regresar al Menú Principal")
        print()
        
        opcion = input("Elige una opción [1-3]: ").strip()
        if opcion == "1":
            tema = mostrar_submenu_elegir_tema()
            if tema is None:
                continue
            else:
                print("\nConsultando articulos de OpenAlex.org...")
            
                openalex = OpenAlexClient(mailto="abrilreinaga@hotmail.com")
                ids = openalex.consultar_por_tema(tema)
                metadata = openalex.extraer_metadatos(ids)
                openalex.guardar_csv(metadata)
            
                if os.path.exists("./data/articulos_openalex.csv"):
                    print("¡Artículos procesados correctamente! Guardados en 'data/articulos_openalex.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
                else:
                    print("Ocurrió un error inesperado, vuelve a intentar.\n")
            
        elif opcion == "2":
            print("\nConsultando articulos de OpenAlex.org...")
            
            openalex = OpenAlexClient(mailto="abrilreinaga@hotmail.com")
            ids = openalex.consultar_generales()
            metadata = openalex.extraer_metadatos(ids)
            openalex.guardar_csv(metadata)
            
            if os.path.exists("./data/articulos_openalex.csv"):
                print("¡Artículos procesados correctamente! Guardados en 'data/articulos_openalex.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
            else:
                print("Ocurrió un error inesperado, vuelve a intentar.\n")
            
        elif opcion == "3":
            return
        else:
            print("\nOpción invalida, vuelve a intentar.")
            
        input("\nPresiona Enter para continuar...")

def mostrar_submenu_thelens():
    """
    Muestra la interfaz para consultar patentes.
    """
    while True:
        pcsv.limpiar_consola()
        print("\n" + "=" * 70)
        print("  ARTÍCULOS Y PATENTES")
        print("=" * 70)
        print()
        
        print("¿Quiéres consultar de un tema en particular? ¿O ver en general?")
        print()
        print("1. Elegir un tema")
        print("2. Consultar artículos en general")
        print("3. Filtrar patentes de CSV generado")
        print("4. Regresar al Menú Principal")
        print()
        
        opcion = input("Elige una opción [1-4]: ").strip()
        if opcion == "1":
            tema = mostrar_submenu_elegir_tema()
            
            if tema is None:
                continue
            else:
                print("\nConsultando articulos de Lens.org...")
            
                lens = LensClient(access_token=TOKEN_LENS, sleep_between_requests=3.0)
                ids = lens.consultar_por_tema(tema)
                metadata = lens.extraer_metadatos(ids)
                lens.guardar_csv(metadata)
            
                if os.path.exists("./data/articulos_lens.csv"):
                    print("¡Artículos procesados correctamente! Guardados en 'data/articulos_lens.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
                else:
                    print("Ocurrió un error inesperado, vuelve a intentar.\n")
            
        elif opcion == "2":
            print("\nConsultando articulos de OpenAlex.org...")
            
            lens = LensClient(access_token=TOKEN_LENS, sleep_between_requests=3.0)
            ids = lens.consultar_generales()
            metadata = lens.extraer_metadatos(ids)
            lens.guardar_csv(metadata)
            
            if os.path.exists("./data/articulos_lens.csv"):
                print("¡Artículos procesados correctamente! Guardados en 'data/articulos_lens.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
            else:
                print("Ocurrió un error inesperado, vuelve a intentar.\n")
        
        elif opcion == "3":
            if not os.path.exists("./data/articulos_lens.csv"):
                print("\nNo se hicieron consultas aún, elige las opciones 1 o 2.")
            
            else:
                print("\nFiltrando patentes...")
                df = pd.read_csv("./data/articulos_lens.csv")
                
                df_patentes = df[df["publication_type"] == "patent"]
                
                if df_patentes.empty:
                    print("\nNo se encontraron artículos de patentes.")
                    continue
                else:
                    print(f"\nSe encontraron {len(df_patentes)} patentes.")
                    df_patentes.to_csv("./data/patentes_lens.csv", index=False)
                    print("\nArtículos guardados en 'data/patentes_lens.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
                    continue
        
        elif opcion == "4":
            return
        else:
            print("\nOpción invalida, vuelve a intentar.")
            
        input("\nPresiona Enter para continuar...")
        
def mostrar_submenu_scraping():
    """
    Muestra la interfaz para consultar ferias y eventos.
    """
    
    while True:
        pcsv.limpiar_consola()
        print("\n" + "=" * 70)
        print("  FERIAS Y EVENTOS")
        print("=" * 70)
        print()
        
        print("¿De qué fuente quieres consultar próximas ferias o eventos?")
        print()
        print("1. Events Eye")
        print("2. 10 Times")
        print("3. N Ferias")
        print("4. Regresar al Menú Principal")
        print()
        
        
        opcion = input("Elige una opción [1-4]: ").strip()
        
        if opcion == "1":
            print("\nBuscando eventos y ferias en Events Eye...")
            
            eventseye.crawler_eventseye(max_paginas=22)
            
            if os.path.exists("./data/eventos.csv"):
                print("¡Artículos procesados correctamente! Guardados en './data/eventos.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
            else:
                print("Ocurrió un error inesperado, vuelve a intentar.\n")
        
        elif opcion == "2":
            print("\nBuscando eventos y ferias en 10 Times...")
            
            tentimes.crawler_10times(max_paginas=10)
            
            if os.path.exists("./data/eventos.csv"):
                print("¡Artículos procesados correctamente! Guardados en './data/eventos.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
            else:
                print("Ocurrió un error inesperado, vuelve a intentar.\n")
        
        elif opcion == "3":
            print("\nBuscando eventos y ferias en N Ferias...")
            
            nferias.crawler_nferias(max_paginas=22)
            
            if os.path.exists("./data/eventos.csv"):
                print("¡Artículos procesados correctamente! Guardados en './data/eventos.csv'.\nPara verlos ir a 'Ver archivos CSV generados'.\n")
            else:
                print("Ocurrió un error inesperado, vuelve a intentar.\n")
        
        elif opcion == "4":
            return
        else:
            print("\nOpción invalida, vuelve a intentar.")
            
        input("\nPresiona Enter para continuar...")

def mostrar_submenu_elegir_tema():
    """
    Muestra la interfaz para elegir tema de búsqueda en submenús de TheLens y OpenAlex
    """
    opciones = [
                "Machine Learning",
                "Deep Learning",
                "Natural Language Processing",
                "Computer Vision",
                "Robotics",
                "Otro (escribir manualmente)"
            ]
    
    while True:
        print("\nElige una opción: ")
        
        for i, opcion in enumerate(opciones, start=1):
            print(f"{i}. {opcion}")
        print("0. Regresar")
        
        eleccion = input(" -> ").strip()
        if eleccion == "0":
            return None

        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
            eleccion = int(eleccion)
            
            if eleccion == len(opciones):
                tema = input("\nIngrese un tema (en inglés): ").strip()
                return tema
            else:
                return opciones[int(eleccion)-1]
        
        else:
            print("Opción inválida, vuelve a intentar.")        
        
        input("\nPresiona Enter para continuar...")     



def mostrar_submenu_rss():
    """
    Muestra la interfaz para consultar noticias RSS.
    """
    while True:
        pcsv.limpiar_consola()
        print("\n" + "=" * 70)
        print("  NOTICIAS RSS")
        print("=" * 70)
        print()
        
        print("¿De cuál fuente quieres consultar noticias?")
        print("1. Clarín")
        print("2. El Economista")
        print("3. Wall Street Journal")
        print("4. Regresar al Menú Principal")
        print()
        
        opcion = input("Elige una opción [1-4]: ").strip()
        if opcion == "1":
            print("Procesando noticias de Clarín...\n")
            resultado = pf.process_rss_feeds("Clarin", pf.feed_URLs["Clarin"], "./data/noticias.csv")
        
        elif opcion == "2":
            print("Procesando noticias de El Economista...\n")
            resultado = pf.process_rss_feeds("El Economista", pf.feed_URLs["El Economista"], "./data/noticias.csv")
        
        elif opcion == "3":
            print("Procesando noticias de Wall Street Journal...\n")
            resultado = pf.process_rss_feeds("Wall Street Journal", pf.feed_URLs["Wall Street Journal"], "./data/noticias.csv")
        
        elif opcion == "4":
            return
        
        else:
            print("Opción no valida, vuelve a intentar.\n")
            input("Presiona ENTER para continuar...")
            continue
        
        if resultado:
                print("¡Noticias procesadas correctamente! Guardadas en './docs/noticias.csv'.\nPara verlas ir a 'Ver archivos CSV generados'.\n")
        else:
            print("Ocurrió un error inesperado, vuelve a intentar.\n") 
        
        input("Presiona ENTER para continuar...")

def ver_csv_generados():
    """
    Ver archivos CSV generados en las consultas, paginados.
    """
    carpeta = "./data"
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".csv") and not f.endswith("_test.csv")]
    if not archivos:
        print("\n No tienes documentos CSV para ver.")
        return
    
    while True:
        pcsv.limpiar_consola()
        print("\n" + "=" * 70)
        print("   DOCUMENTOS CSV")
        print("=" * 70)
        
        for i, archivo in enumerate(archivos, start=1):
            print(f"{i}. {archivo}")
        print("0. Regresar al Menú Principal \n")
        
        opcion = input("Elige una opción [0-{}]: ".format(len(archivos))).strip()
        if opcion == "0":
            return
        
        if not opcion.isdigit() or not (1<= int(opcion) <= len(archivos)):
            print("\n Opción no valida, vuelve a intentar.\n")
            input("Presiona ENTER para continuar...")
            continue
        
        archivo_seleccionado = archivos[int(opcion)-1]
        ruta_archivo = os.path.join(carpeta, archivo_seleccionado)
        
        try:
            data_frame = pd.read_csv(ruta_archivo)
        except Exception as e:
            print(f"\n Error de lectura: {e}")
            input("\nPresiona ENTER para continuar...")
            continue
        
        if "country" in data_frame.columns and "summary" in data_frame.columns:
            pcsv.paginar_noticias_csv(data_frame, archivo_seleccionado)

        elif "type" in data_frame.columns and "abstract" in data_frame.columns and "fields_of_study" in data_frame.columns:
            if (data_frame["type"] == "patent").all():
                pcsv.paginar_articulos_api(data_frame, archivo_seleccionado)
            else:
                pcsv.paginar_articulos_api(data_frame, archivo_seleccionado)
        
        elif "Nombre del evento" in data_frame.columns and "Descripción" in data_frame.columns and "Fecha" in data_frame.columns:
            pcsv.paginar_feriasyeventos_csv(data_frame, archivo_seleccionado)
        
        else:
            print("\n⚠️ No se reconoce el formato del CSV. No se puede paginar.")
            print("Columnas encontradas:", list(data_frame.columns))
            input("\nPresiona ENTER para continuar...")

def mostrar_acerca_de():
    """
    Muestra información sobre el proyecto.
    """
    pcsv.limpiar_consola()
    print("\n" + "=" * 70)
    print("  ACERCA DE")
    print("=" * 70)
    print()
    print(" Trabajo Práctico: Recuperación de Información en la Web")
    print()
    print(" Universidad Nacional de Tres de Febrero")
    print("   Licenciatura en Informática")
    print("   Estructuras de Datos y Algoritmos")
    print()
    print(" Equipo de Desarrollo:")
    print("   - Delfina Emma Basso Natale")
    print("   - Abril Reinaga ")
    print("   - Matias Di Bernardo")
    print()
    print(" Fecha: Noviembre 2025")
    print()
    print(" Tecnologías utilizadas:")
    print("   - Python 3.x")
    print("   - requests (APIs y HTTP)")
    print("   - BeautifulSoup (Web Scraping)")
    print("   - feedparser (RSS)")
    print("   - pandas (Manipulación de datos)")
    print()
    print(" Fuentes de datos:")
    print("   - OpenAlex (artículos científicos)")
    print("   - The Lens (patentes)")
    print("   - eventseye.com, nferias.com, 10times.com (eventos)")
    print("   - Investing, El Economista, Wall Street Journal (noticias RSS)")
    print()