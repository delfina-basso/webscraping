from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import csv
import time
import random
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

def crawler_10times(url_semilla="https://10times.com/",max_paginas=10, retraso=1):
    frontera = [url_semilla] 
    visitadas = set()
    resultados = []
    campos = [
        "Nombre del evento",
        "Descripción",
        "Fecha",
        "Ubicación",
        "Sector / industrias relacionadas",
        "Web oficial",
        "Correo de contacto"
    ]

    robots_url = urljoin(url_semilla, "/robots.txt")
    robot_parser = RobotFileParser()
    robot_parser.set_url(robots_url)

    try:
        robot_parser.read()
    except Exception as e:
        robot_parser = None

    urls_categorias = []

    while frontera and len(visitadas) < max_paginas:
        url_actual = frontera.pop(0)
        if url_actual in visitadas: 
            continue

        if robot_parser:
            if not robot_parser.can_fetch("*", url_actual):
                print(f"Bloqueado por robots.txt: {url_actual}")
                continue
  
        driver = crear_navegador()
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        driver.get(url_actual)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        visitadas.add(url_actual)

        if url_actual == url_semilla:
            div = soup.find("div", class_="container py-4")
            if div:
                as_ = div.find_all("a", href=True, onclick=False)
                for i, a in enumerate(as_): 
                    url_categoria = urljoin(url_actual, a["href"])
                    if url_categoria not in visitadas and url_categoria not in frontera:
                        frontera.append(url_categoria)
                        urls_categorias.append(url_categoria)

                        #como extrae todas las categroias primero tarda mmucho tiempo en extraer datos asi que agregamos 
                        #este if para que solo extraiga la primera categoria
                        if i == 0:
                            break 

        else:              
            table = soup.find("table", id="listing-events")
            if table:
                tds = table.find_all("td", attrs={"data-id":True, "onclick":True})
                for i, td in enumerate(tds):
                    url_evento = td["onclick"].replace("window.open", "").strip("()'")
                    if url_evento not in visitadas and url_evento not in frontera:
                        frontera.append(url_evento)
            
            fecha = ""
            nombre = ""
            ubicacion = ""
            div_header = soup.find("div", id="online-header-left")
            if div_header:
                div_date = div_header.find("div", class_=(re.compile("header_date")))
                if div_date:
                    fecha = div_date.get_text(strip=True)

                h1 = div_header.find("h1", class_="mb-0")
                if h1:
                    nombre = h1.get_text(strip=True)

                div_ubicacion = div_header.find("div",class_="mt-1 text-muted m-mins_lft")
                if div_ubicacion:
                    ubicacion = div_ubicacion.get_text()

            industrias = []
            div_industrias = soup.find("div", id="nav_btn")
            if div_industrias:
                for span in div_industrias.find_all("span", class_="quicklinks1 d-inline"):
                    industria = span.get_text(strip=True).replace("#", "")
                    industrias.append(industria)

            industrias_bonitas = " | ".join(industrias) if industrias else ""       

            descripcion = ""
            box = soup.find("section", class_=(re.compile("box fs-14")))
            if box:
                partes_desc = []
                divs = box.find_all("div", class_="mb-2")
                for div in divs:
                    spans = div.find_all("span")
                    for span in spans:
                        if span.get("id") == "toggleButton":
                            continue
                        texto = span.get_text(strip=True).replace("...Read More", "")
                        partes_desc.append(texto)
                        
                descripcion = " ".join(partes_desc)
                
            web = ""
            email = ""

            if url_actual not in urls_categorias:
                resultados.append({
                        "Nombre del evento": nombre,
                        "Descripción": descripcion,
                        "Fecha": fecha,
                        "Ubicación": ubicacion,
                        "Sector / industrias relacionadas": industrias_bonitas,
                        "Web oficial": web,
                        "Correo de contacto": email
                    })
                
        driver.quit()
        time.sleep(5 + random.random()*2)

    if resultados:
        os.makedirs("data", exist_ok=True)
        with open("data/eventos.csv","a",newline="",encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            archivo_vacio = not os.path.exists("data/eventos.csv") or os.path.getsize("data/eventos.csv") == 0
            if archivo_vacio:                   
                w.writeheader()
            
            #para resultados bloqueados por cloudfare
            resultados_no_vacios = []
            for resultado in resultados:
                for value in resultado.values():
                    if value != "":
                        resultados_no_vacios.append(resultado)
                        break
                
            w.writerows(resultados_no_vacios)
        print(f"Guardado: data/eventos.csv ({len(resultados_no_vacios)} filas)")

    else:
        print("No se pudo extraer ferias.")
        
def crear_navegador():
    op = Options() 
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    op.add_argument("--disable-blink-features=AutomationControlled")
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)
    op.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    op.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=op
    )

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined })
        """
    })
    
    return driver 

