import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import time
import re
import csv
import os

def crawler_eventseye(url_semilla="https://www.eventseye.com", max_paginas=10, retraso=1):      
        frontera = [url_semilla] 
        visitadas = set()
        meses_flag = True
        flag = True  

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

        while frontera and len(visitadas) < max_paginas: 
            url_actual = frontera.pop(0)
            if url_actual in visitadas: 
                continue

            if robot_parser:
                if not robot_parser.can_fetch("*", url_actual): 
                    print(f"Bloqueado por robots.txt: {url_actual}")
                    continue

            try: 
                response = requests.get(url_actual, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (compatible; BotEstudiantil/1.0)'
                })
                response.raise_for_status()
            except Exception as e:
                print(f"  Error al acceder: {e}")
                continue

            soup = BeautifulSoup(response.text, 'lxml') 
            visitadas.add(url_actual)
 
            if re.search(r"/fairs/f-", url_actual):
                try:
                    nombre = soup.find("li", class_="active") or soup.find("h1", class_="active") or soup.find("h1")
                    
                    if nombre:
                        nombre = nombre.get_text(strip=True)
                        nombre = re.sub(r"\([A-Z]{2}\)$", "", nombre).strip()
                    else:
                        nombre = ""

                    descripcion = soup.find("div", class_="description")
                    if descripcion:
                        descripcion = descripcion.get_text(strip=True).replace("Description","",count=1)
                    else:
                        descripcion = ""

                    tables = soup.find_all("table")
                    dates = None
                    for t in tables:
                        texto_tabla = t.get_text().lower()
                        if "date" in texto_tabla or "location" in texto_tabla:
                            dates = t
                            break
                    
                    fechas = []
                    ubicaciones = []
                    if dates:
                        for tr in dates.find_all("tr"):
                            tds = tr.find_all("td")
                            if len(tds) >= 3:
                                fechas.append(tds[0].get_text(strip=True))
                                ubicacion = tds[2].get_text(strip=True) + ", " + tds[1].get_text(strip=True)
                                ubicaciones.append(ubicacion)
                    
                    fechas_bonitas =  " | ".join(fechas) if fechas else ""
                    ubicaciones_bonitas = " | ".join(ubicaciones) if ubicaciones else ""
            
                    industrias = []
                    ind_div = soup.find("div", class_="industries") or soup.find("div", id="zone_themes")
                    if ind_div:
                        industrias = [a.get_text(strip=True) for a in ind_div.find_all("a")]
                    industrias_bonitas = " | ".join(industrias) if industrias else ""

                    contacto = soup.find("div", class_="more-info") or soup.find("div", class_="zone_more_info")
                    web = ""
                    email = ""
                    if contacto:
                        web = contacto.find("a", class_="ev-web")
                        if web:
                            web = web["href"]

                        amail = contacto.find("a", class_="ev-mail")
                        if amail and "mailto:" in amail.get("href", ""):
                            email = amail["href"].replace("mailto:", "")
                            
                    resultados.append({
                        "Nombre del evento": nombre,
                        "Descripción": descripcion,
                        "Fecha": fechas_bonitas,
                        "Ubicación": ubicaciones_bonitas,
                        "Sector / industrias relacionadas": industrias_bonitas,
                        "Web oficial": web,
                        "Correo de contacto": email
                    })
                except Exception as e:
                    print(f"Error extrayendo datos: {e}")
                
                time.sleep(retraso)
                continue      
      
            monthgraph = soup.find("div", class_="monthgraph")
            if monthgraph and meses_flag:
                meses_flag = False
                
                for enlace in monthgraph.find_all("a", href=True):
                    url_fairs = url_actual + "/fairs/"
                    url_encontrada = urljoin(url_fairs, enlace['href']).split('#')[0]
                    if url_encontrada not in visitadas and url_encontrada not in frontera and flag:
                        frontera.append(url_encontrada)
                        flag = False
            
            else:
                tradeshows = soup.find_all("table", class_="tradeshows")
                if tradeshows:
                    for tradeshow in tradeshows:
                        for enlace in tradeshow.find_all("a", href=re.compile(r"^f-")):
                            url_encontrada = urljoin(url_actual, enlace['href']).split('#')[0]
                            if url_encontrada not in visitadas and url_encontrada not in frontera:
                                frontera.append(url_encontrada)
                                
                    next_page_div = soup.find("div", class_="pages-links")
                    if next_page_div:
                        next_page_line = next_page_div.find("a", title=True)
                        if next_page_line:
                            url_encontrada = urljoin(url_actual, next_page_line['href']).split('#')[0]
                            if url_encontrada not in visitadas and url_encontrada not in frontera:
                                frontera.append(url_encontrada)
            time.sleep(retraso)

        if resultados:
            os.makedirs("./data", exist_ok=True)
            with open("./data/eventos.csv","a",newline="",encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=campos)
                archivo_vacio = not os.path.exists("./data/eventos.csv") or os.path.getsize("./data/eventos.csv") == 0
                if archivo_vacio:                   
                    w.writeheader()
                w.writerows(resultados)
            print(f"Guardado: ./data/eventos.csv ({len(resultados)} filas)")
        else:
            print("No se pudo extraer ferias.")
