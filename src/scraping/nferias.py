import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import time
import re
import csv
import os


def crawler_nferias(url_semilla="https://www.nferias.com", max_paginas=10, retraso=1):
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

        while frontera and len(visitadas) < max_paginas:
            url_actual = frontera.pop(0)
            if url_actual in visitadas:
                continue

            if robot_parser:
                if not robot_parser.can_fetch("*", url_actual):
                    continue

            try:
                response = requests.get(url_actual, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (compatible; BotEstudiantil/1.0)'
                })
                response.raise_for_status()
            except Exception as e:
                print(f"Error al acceder: {e}")
                continue

            soup = BeautifulSoup(response.text, 'lxml')
            visitadas.add(url_actual)

            if re.search(r"https://www.nferias.com/[a-zA-Z0-9\-/]+$", url_actual) and not re.search(r"sitemap", url_actual):

                nombre = soup.find("h1", class_="nTitle")
                if nombre:
                    nombre = nombre.get_text(strip=True)
                    nombre = nombre[:-5]
                else:
                    nombre = ""

                descripcion = "Sin descripción"

                dates = soup.find("table", class_="table table-sm table-responsive")
                fechas = []
                ubicaciones = []
                if dates:
                    for tr in dates.find_all("tr"):

                        if "hidden" in tr.attrs:
                            continue

                        tds = tr.find_all("td")
                        if len(tds) >= 3:
                            fechas.append(tds[1].get_text())
                            ubicacion = tds[2].get_text(strip=True)
                            ubicaciones.append(ubicacion)

                fechas_bonitas =  " | ".join(fechas) if fechas else ""
                ubicaciones_bonitas = " | ".join(ubicaciones) if ubicaciones else ""
        

                industrias = []
                web = ""
                articles = soup.find_all("article", class_="mb-4")
                for article in articles:
                    ps = article.find_all("p")
                    for p in ps:
                        texto = p.get_text(strip=True)
                        if re.search(r"Ficha técnica", texto):
                            ul = article.find("ul", class_="list-unstyled")
                            if ul:
                                as_ = ul.find_all("a")
                                for a in as_:
                                    industria = a.get_text(strip=True)
                                    industrias.append(industria)
                        if re.search(r"Próxima edición", texto):
                            a = article.find("a", rel="nofollow")
                            if a:
                                web = a["href"]

                industrias_bonitas = " | ".join(industrias) if industrias else ""
        
                email = "Sin mail de contacto"    

                resultados.append({
                    "Nombre del evento": nombre,
                    "Descripción": descripcion,
                    "Fecha": fechas_bonitas,
                    "Ubicación": ubicaciones_bonitas,
                    "Sector / industrias relacionadas": industrias_bonitas,
                    "Web oficial": web,
                    "Correo de contacto": email
                })
            
                time.sleep(retraso)
                continue      
      
            uls = soup.find_all("ul", class_="list-unstyled")
            if uls:
                for ul in uls:
                    as_ = ul.find_all("a")
                    if as_:    
                        for a in as_:
                            texto = a.get_text(strip=True)
                            if texto.lower() == "ferias":
                                url_ferias = a["href"]
                                if url_ferias not in visitadas and url_ferias not in frontera:
                                    frontera.append(url_ferias)
                                break

            if re.search(r"sitemap/[a-z]", url_actual):
                ul = soup.find("ul", class_="list-unstyled sitemap")
                if ul:
                    as_ = ul.find_all("a")
                    if as_:
                        for a in as_:
                            url_evento = a["href"]
                            if url_evento not in visitadas and url_evento not in frontera:
                                        frontera.append(url_evento)

            time.sleep(retraso)

        if resultados:
            os.makedirs("data", exist_ok=True)
            with open("data/eventos.csv","a",newline="",encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=campos)
                archivo_vacio = not os.path.exists("data/eventos.csv") or os.path.getsize("data/eventos.csv") == 0
                if archivo_vacio:                   
                    w.writeheader()
                w.writerows(resultados)
            print(f"Guardado: data/eventos.csv ({len(resultados)} filas)")

        else:
            print("No se pudo extraer ferias.")
