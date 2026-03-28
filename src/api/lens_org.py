"""
Cliente para Scholar Request de Lens.org

Docs principales:
    - Scholar request docs: https://docs.api.lens.org/request-scholar.html
    - Swagger (interactivo): https://api.lens.org/swagger-ui/index.html
"""

from typing import List, Dict
import requests
import time
import os
import pandas as pd
import html
import re

TOKEN_LENS="oZS3AWPzGG2oB2Es6LgtllGeJLNRjOPmww87J44XPK8Plz5ap6QD"

class LensClient:
    BASE = "https://api.lens.org"
    SCHOLAR_SEARCH = BASE + "/scholarly/search"
    SCHOLAR_GET = BASE + "/scholarly/{}"
    

    def __init__(self, access_token: str = "", sleep_between_requests: float = 0.3):
        """
        :param sleep_between_requests: pausa entre requests para respetar rate limits
        """
        self.token = access_token or os.getenv("TOKEN_LENS")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.sleep = sleep_between_requests
    
    def consultar_por_tema(self, tema: str, limite: int = 50) -> List[str]:
        """
        Busca los últimos `limite` resultados relacionados con `tema`.
        Devuelve lista de lens_id (strings) ordenada por fecha de publicación descendente.
        """
        results = []
        fetched = 0
        offset = 0
        
        while fetched < limite:
            page_size = min(100, limite - fetched)
            body = {
                "query": {"query_string": {"query": tema}},
                "size": page_size,
                "from": offset,
                "sort": [{"date_published": "desc"}]
            }
            
            resp = self.session.post(self.SCHOLAR_SEARCH, json=body)
            if resp.status_code != 200:
                print(f"Error {resp.status_code}: {resp.text[:200]}")
                break
            
            data = resp.json()
            hits = data.get("data", [])
            
            if not hits:
                break
            
            results.extend(hits)
            fetched = len(results)
            offset += page_size
            time.sleep(self.sleep)
        
        return results[:limite]

    def consultar_generales(self, limite: int = 100) -> List[str]:
        """
        Recupera los últimos `limite` artículos/patentes en general (sin filtrar por tema),
        ordenados por fecha de publicación descendente.
        Hacemos una búsqueda match_all (query.match_all) ordenada por date_published desc.
        """
        results = []
        fetched = 0
        offset = 0
        
        while fetched < limite:
            page_size = min(100, limite - fetched)
            body = {
                "query": {"match_all": {}},
                "size": page_size,
                "from": offset,
                "sort": [{"date_published": "desc"}]
            }
            
            resp = self.session.post(self.SCHOLAR_SEARCH, json=body)
            if resp.status_code != 200:
                print(f"Error {resp.status_code}: {resp.text[:200]}")
                break
            
            data = resp.json()
            hits = data.get("data", [])
            if not hits:
                break
            
            results.extend(hits)
            fetched = len(results)
            offset += page_size
            time.sleep(self.sleep)
        
        return results[:limite]
    
    def consultar_patentes(self, limite: int = 50) -> List[str]:
        """
        Devuelve IDs de patentes de Lens, ordenadas por fecha de publicación.
        """
        results = []
        fetched = 0
        offset = 0
        
        while fetched < limite:
            page_size = min(100, limite - fetched)
            
            body = {
                "query": {
                    "term": {
                        "publication_type": "patent"
                    }
                },
                "size": page_size,
                "from": offset,
                "sort": [{"date_published": "desc"}]
            }
            
            resp = self.session.post(self.SCHOLAR_SEARCH, json=body)
            if resp.status_code != 200:
                print(f"Error {resp.status_code}: {resp.text[:200]}")
                break
            
            data = resp.json()
            hits = data.get("data", [])
            if not hits:
                break
            
            results.extend(hits)
            fetched = len(results)
            offset += page_size
            time.sleep(self.sleep)
        
        return results[:limite]

    def extraer_metadatos(self, lista_results: List[str]) -> List[Dict]:
        """
        Dada una lista de lens_id (ej '100-004-910-081-14X'), recupera metadatos completos.
        Para cada ID se extrae dicha ID, título, autores, fecha de publicación
        el abstract, tipo de publicación, país relacionado a la publicación, campo de estudio,
        palabras clave e instituciones. Devuelve lista de diccionarios.
        """
        results = []
        
        for w in lista_results:
            if "data" in w:
                w = w["data"]
            
            meta = {
                "lens_id": w.get("lens_id"),
                "title": w.get("title") or w.get("display_title"),
                "date_published": w.get("date_published"),
                "year_published": w.get("year_published"),
                "publication_type": w.get("publication_type"),
                "country": w.get("source", {}).get("country"),
                "fields_of_study": w.get("fields_of_study") or [],
                "keywords": w.get("keywords") or [],
            }
            
            autores = []
            for a in w.get("authors", []):
                if isinstance(a, dict):
                    autores.append(a.get("display_name"))
            meta["authors"] = autores
            
            insts = []
            for a in w.get("authors", []):
                for aff in a.get("affiliations", []):
                    insts.append(aff.get("name"))
            meta["institutions"] = insts
            
            results.append(meta)
        
        return results
            

    def guardar_csv(self, lista_metadata: List[Dict], path: str = "./data/articulos_lens.csv"):
        """
        Guarda la lista de metadata en CSV con columnas estandarizadas.
        """
        if not lista_metadata:
            new_df = pd.DataFrame()
        else:
            rows = []
            for m in lista_metadata:
                title = m.get("title")
                abstract = m.get("abstract")
                if not title and not abstract:
                    continue
                
                clean_authors = []
                for a in (m.get("authors") or []):
                    if isinstance(a, str):
                        clean_authors.append(a.replace("\n", " ").strip())
                    else:
                        clean_authors.append(str(a).strip())
                
                rows.append({
                    "id": m.get("lens_id"),
                    "title": title,
                    "authors": "; ".join(clean_authors),
                    "publication_date": m.get("date_published"),
                    "publication_year": m.get("year_published"),
                    "abstract": abstract,
                    "type": m.get("publication_type"),
                    "countries": m.get("country") or "",
                    "fields_of_study": "; ".join(m.get("fields_of_study") or []),
                    "keywords": "; ".join(m.get("keywords") or []),
                    "institutions": "; ".join(m.get("institutions") or [])
                })
            new_df = pd.DataFrame(rows)
        
        if not os.path.exists(path):
            new_df.to_csv(path, index=False)
            return
        
        old_df = pd.read_csv(path)
        combined = pd.concat([old_df, new_df], ignore_index=True)
        if "lens_id" in combined.columns:
            combined.drop_duplicates(subset=["lens_id"], inplace=True)
        
        combined.to_csv(path, index=False)

    def status_check(self, timeout: float = 5.0) -> Dict:
        """Realiza una petición mínima para comprobar el estado de la API de Lens.

        Devuelve diccionario con:
            - ok: True/False
            - status_code: código HTTP o None
            - detail: mensaje corto

        Usa `SCHOLAR_SEARCH` con una query match_all y `size=1`.
        """
        body = {"query": {"query_string": {"query": "test"}}, "size": 1}

        try:
            resp = self.session.post(self.SCHOLAR_SEARCH, json=body, timeout=timeout)
        except requests.exceptions.RequestException as e:
            return {"ok": False, "status_code": None, "detail": str(e)}

        if resp.status_code == 200:
            return {"ok": True, "status_code": 200}

        return {"ok": False, "status_code": resp.status_code, "detail": resp.text[:200]}
    
def limpiar_abstract(txt:str) -> str:
    if not txt:
        return ""
    
    if not isinstance(txt, str):
        txt = str(txt)
    
    return txt.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()