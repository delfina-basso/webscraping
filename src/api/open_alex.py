"""
Cliente mínimo para extraer datos de la API de OpenAlex.

"""

from typing import List, Dict, Optional
import requests
import time
import pandas as pd
import html
import re
import os

class OpenAlexClient:
    BASE_URL = "https://api.openalex.org"

    def __init__(self, mailto: Optional[str] = None, api_key: Optional[str] = None, sleep_between_requests: float = 0.1):
        """
        :param mailto: (opcional) tu email para el polite pool (recomendado por OpenAlex)
        :param api_key: (opcional) tu API key de OpenAlex si la tienes
        :param sleep_between_requests: segundos a esperar entre requests para no golpear la API
        """
        self.mailto = mailto
        self.api_key = api_key
        self.sleep = sleep_between_requests
        
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _build_common_params(self, extra: Dict = None) -> Dict:
        params = {}
        if self.mailto:
            params["mailto"] = self.mailto
        if extra:
            params.update(extra)
        return params

    def consultar_por_tema(self, tema: str, limite: int = 50) -> List[str]:
        """
        Consulta los últimos artículos/patentes relacionados con un tema usando `search`.
        Devuelve lista de IDs OpenAlex (strings), ordenados por fecha de publicación (desc).
        :param tema: cadena de búsqueda (ej. "Inteligencia Artificial")
        :param limite: número máximo de resultados a devolver
        """
        endpoint = f"{self.BASE_URL}/works"
        ids = []
        per_page = min(max(1, limite), 200)
        page = 1
        
        while len(ids) < limite:
            params = self._build_common_params({
                "search": tema,
                "per-page": per_page,
                "page": page,
                "sort": "publication_date:desc"
            })
            
            try:
                resp = self.session.get(endpoint, params=params)
            except requests.exceptions.RequestException as e:
                print(f"Error de conexión: {e}")
                time.sleep(self.sleep)
                continue
            
            try:
                data = resp.json()
            except ValueError:
                print("Respuesta no-JSON de OpenAlex:", resp.text[:200])
                break
            
            results = data.get("results", [])
            if not results:
                break
            
            for w in results:
                if len(ids) >= limite:
                    break
                
                openalex_id = w.get("id")
                if isinstance(openalex_id, str) and openalex_id.startswith("https://openalex.org/"):
                    openalex_id = openalex_id.split("/")[-1]
                ids.append(openalex_id)
            
            page += 1
            if not data.get("meta", {}).get("next_page"):
                break
            time.sleep(self.sleep)
        
        return ids

    def consultar_generales(self, limite: int = 100) -> List[str]:
        """
        Consulta los últimos artículos/patentes publicados en general (por fecha de publicación descendente).
        Devuelve lista de IDs OpenAlex (strings).
        :param limite: número máximo de resultados a devolver
        """
        endpoint = f"{self.BASE_URL}/works"
        ids = []
        per_page = min(max(1, limite), 200)
        page = 1

        while len(ids) < limite:
            params = self._build_common_params({
                "per-page": per_page,
                "page": page,
                "sort": "publication_date:desc"
            })
            
            try:
                resp = self.session.get(endpoint, params=params)
            except requests.exceptions.RequestException as e:
                print(f"Error de conexión: {e}")
                time.sleep(self.sleep)
                continue
            
            try:
                data = resp.json()
            except ValueError:
                print("Respuesta no-JSON de OpenAlex:", resp.text[:200])
                break
            
            results = data.get("results", [])
            if not results:
                break
            
            for w in results:
                if len(ids) >= limite:
                    break
                
                openalex_id = w.get("id")
                if isinstance(openalex_id, str) and openalex_id.startswith("https://openalex.org/"):
                    openalex_id = openalex_id.split("/")[-1]
                
                ids.append(openalex_id)
            
            page += 1
            if not data.get("meta", {}).get("next_page"):
                break
            time.sleep(self.sleep)
        
        return ids

    @staticmethod
    def _invert_abstract(inverted_index: Dict) -> Optional[str]:
        """
        Reconstruye el abstract a partir de abstract_inverted_index si está disponible.
        abstract_inverted_index: dict palabra -> lista de posiciones
        """
        
        if not inverted_index:
            return None
        
        max_pos = -1
        positions = {}
        
        for word, pos_list in inverted_index.items():
            for p in pos_list:
                if p not in positions:
                    positions[p] = word
                max_pos = max(max_pos, p)
                    
        return " ".join(positions.get(i, "") for i in range(max_pos +1)).strip() or None

    def extraer_metadatos(self, lista_IDs_articulos: List[str]) -> List[Dict]:
        """
        A partir de una lista de IDs OpenAlex (p.ej. ['W1234','W5678']) recupera metadatos completos.
        Para cada ID se extrae dicha ID, título, autores, fecha de publicación
        el abstract, tipo de publicación, país relacionado a la publicación, campo de estudio,
        palabras clave e instituciones. Devuelve lista de diccionarios.
        """
        normalized_ids = []
        
        for id_ in lista_IDs_articulos:
            if id_ is None:
                continue
            if isinstance(id_, str) and id_.startswith("https://openalex.org/"):
                normalized_ids.append(id_.split("/")[-1])
            else:
                normalized_ids.append(str(id_))
        
        results = []
        chunk_size = 100 
        
        for i in range(0, len(normalized_ids), chunk_size):
            chunk = normalized_ids[i:i + chunk_size]
            filter_val = "openalex:" + "|".join(chunk)
            endpoint = f"{self.BASE_URL}/works"
            params = self._build_common_params({
                "filter": filter_val,
                "per-page": len(chunk)
            })
            
            try:
                resp = self.session.get(endpoint, params=params)
            except requests.exceptions.RequestException as e:
                print(f"Error de conexión: {e}")
                time.sleep(self.sleep)
                continue
            
            if resp.status_code != 200:
                for single in chunk:
                    try:
                        single_meta = self._get_single_work(single)
                        if single_meta:
                            results.append(single_meta)
                    except Exception:
                        continue
                time.sleep(self.sleep)
                continue

            try:
                data = resp.json()
            except ValueError:
                print("Respuesta no-JSON de OpenAlex:", resp.text[:200])
                break
            
            works = data.get("results", [])
            for w in works:
                meta = {}
                openalex_id = w.get("id")
                if isinstance(openalex_id, str) and openalex_id.startswith("https://openalex.org/"):
                    openalex_id = openalex_id.split("/")[-1]
                
                meta["id"] = openalex_id
                meta["title"] = w.get("display_name") or w.get("title") or None

                authors_list = []
                institutions_coll = []
                countries = set()
                authorships = w.get("authorships", []) or []
                
                for auth in authorships:
                    author_obj = auth.get("author", {}) or {}
                    author_name = author_obj.get("display_name") or author_obj.get("name")
                    author_id = author_obj.get("id") or author_obj.get("openalex_id")
                    
                    if isinstance(author_id, str) and author_id.startswith("https://openalex.org/"):
                        author_id = author_id.split("/")[-1]
                    
                    if author_name or author_id:
                        authors_list.append(f"{author_name or 'N/A'}")
                    insts = auth.get("institutions") or []
                    
                    for inst in insts:
                        inst_id = inst.get("id")
                        
                        if isinstance(inst_id, str) and inst_id.startswith("https://openalex.org/"):
                            inst_id_short = inst_id.split("/")[-1]
                        else:
                            inst_id_short = inst_id
                        
                        inst_name = inst.get("display_name") or inst.get("name") or None
                        institutions_coll.append(f"{inst_name or 'N/A'} ({inst_id_short or ''})")
                        country_code = inst.get("country_code")
                        if country_code:
                            countries.add(country_code)

                meta["authors"] = authors_list
                meta["institutions"] = list(dict.fromkeys(institutions_coll))
                meta["countries"] = list(countries)
                
                pub_date = w.get("publication_date") or None
                pub_year = w.get("publication_year") or None
                meta["publication_date"] = pub_date
                meta["publication_year"] = int(pub_year) if pub_year is not None else None
                abs_inv = w.get("abstract_inverted_index")
                if abs_inv:
                    abstract = self._invert_abstract(abs_inv)
                else:
                    abstract = w.get("abstract") or w.get("summary")
                meta["abstract"] = limpiar_abstract(abstract)
                
                meta["type"] = w.get("type") or w.get("type_of_work")

                concepts = w.get("concepts") or []
                fields = []
                for c in concepts:
                    name = c.get("display_name") or c.get("name")
                    if name:
                        fields.append(name)
                
                meta["fields_of_study"] = fields

                keyword_list = w.get("keywords") or []
                processed_keywords = []

                if isinstance(keyword_list, str):
                    keyword_list = [keyword_list]

                for k in keyword_list:
                    if k is None:
                        continue
                    if isinstance(k, str):
                        processed_keywords.append(k)
                        continue
                    
                    if isinstance(k, dict):
                        for key in ("display_name", "name", "keyword", "text", "label"):
                            val = k.get(key)
                            if isinstance(val, str) and val.strip():
                                processed_keywords.append(val.strip())
                                break
                        continue
                    
                meta["keywords"] = list(dict.fromkeys(processed_keywords))

                results.append(meta)

            time.sleep(self.sleep)

        map_meta = {r["id"]: r for r in results if r.get("id")}
        ordered_results = [map_meta.get(i) for i in normalized_ids if map_meta.get(i)]
        
        return ordered_results

    def _get_single_work(self, work_id: str) -> Optional[Dict]:
        """
        Recupera un work individualmente: /works/{id}
        """
        if work_id.startswith("https://openalex.org/"):
            work_id = work_id.split("/")[-1]
        
        url = f"{self.BASE_URL}/works/{work_id}"
        params = self._build_common_params()
        resp = self.session.get(url, params=params)
        
        if resp.status_code != 200:
            return None
        tmp = self.extraer_metadatos([work_id])
        
        return tmp[0] if tmp else None

    def guardar_csv(self, lista_metadata: List[Dict], path: str = "./data/articulos_openalex.csv"):
        """
        Guarda la lista de metadata (lista de diccionarios) en CSV.
        Campos que se guardan (columnas):
        id, title, authors, publication_date, publication_year, abstract,
        type, countries, fields_of_study, keywords, institutions
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
                
                clean_authors = [a.replace("\n", " ").strip() for a in (m.get("authors") or [])]
                
                rows.append({
                "id": m.get("id"),
                "title": title,
                "authors": "; ".join(clean_authors),
                "publication_date": m.get("publication_date"),
                "publication_year": m.get("publication_year"),
                "abstract": abstract,
                "type": m.get("type"),
                "countries": "; ".join(m.get("countries") or []),
                "fields_of_study": "; ".join(m.get("fields_of_study") or []),
                "keywords": "; ".join(m.get("keywords") or []),
                "institutions": "; ".join(m.get("institutions") or []),
            })
            new_df = pd.DataFrame(rows)
        
        if not os.path.exists(path):
            new_df.to_csv(path, index=False)
            return
        
        old_df = pd.read_csv(path)
        combined = pd.concat([old_df, new_df], ignore_index=True)
        if "id" in combined.columns:
            combined.drop_duplicates(subset=["id"], inplace=True)
        
        combined.to_csv(path, index=False)


    def status_check(self, timeout: float = 5.0) -> Dict:
        """Realiza una petición liviana para comprobar que la API de OpenAlex responde.

        Devuelve un diccionario con claves:
            - ok: True/False
            - status_code: código HTTP o None si no hubo respuesta
            - detail: mensaje corto (opcional)

        El método hace una petición a `/works` con `per-page=1`.
        """
        endpoint = f"{self.BASE_URL}/works"
        params = self._build_common_params({"per-page": 1})
        
        try:
            resp = self.session.get(endpoint, params=params, timeout=timeout)
        except Exception as e:
            return {"ok": False, "status_code": None, "detail": str(e)}

        if resp.status_code == 200:
            return {"ok": True, "status_code": 200}

        return {"ok": False, "status_code": resp.status_code, "detail": resp.text[:200]}
    
def limpiar_abstract(txt:str) -> str:
    if not isinstance(txt, str):
        return txt
    
    desescapado = html.unescape(txt)
    limpio = re.sub(r'<[^>]+>', '', desescapado)
    
    return limpio.strip()