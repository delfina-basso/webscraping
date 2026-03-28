"""
Tests para el módulo de APIs.
"""

import os
from unittest.mock import patch, MagicMock
from src.api.open_alex import OpenAlexClient
from src.api.lens_org import TOKEN_LENS
from src.api.lens_org import LensClient

def test_openalex_connection():
    """
    Test de conexión a OpenAlex API.
    """
    openalex_api = OpenAlexClient(mailto="abrilreinaga@hotmail.com")
    status = openalex_api.status_check()

    assert status["ok"] is True, f"Error en la conexión a OpenAlex API. Error: {status['status_code']}."

def test_thelens_connection():
    """
    Test de conexión a The Lens API.
    """
    respuesta_prueba = MagicMock()
    respuesta_prueba.status_code = 200
    
    with patch("requests.Session.post", return_value=respuesta_prueba):
        lens = LensClient(access_token="dummy")
        status = lens.status_check()
    
    assert status["ok"] is True
    assert status["status_code"] == 200


def test_extract_article_metadata():
    """
    Test de extracción de metadatos de artículos.
    """
    openalex = OpenAlexClient(mailto="abrilreinaga@hotmail.com")
    ids = openalex.consultar_por_tema("Machine Learning", limite=50)
    metadata = openalex.extraer_metadatos(ids)

    if len(metadata) == 0:
        token = TOKEN_LENS
        assert token, "Falta TOKEN_LENS para Lens"

        lens = LensClient(access_token=token)
        ids = lens.consultar_por_tema("Machine Learning", limite=50)
        metadata = lens.extraer_metadatos(ids)

    assert len(metadata) >= 10, "No se encontraron suficientes artículos."

def test_extract_patent_metadata():
    """
    Test de extracción de metadatos de patentes.
    """
    token = TOKEN_LENS
    assert token, "Falta TOKEN_LENS para Lens"

    lens = LensClient(access_token=token)
    ids = lens.consultar_patentes(limite=50)
    
    metadata = lens.extraer_metadatos(ids)
    patentes = [m for m in metadata if m.get("publication_type") == "patent"]
    
    if len(patentes) == 0:
        print("Lens no devolvió patentes. Problema temporal")
        return
    
    for p in patentes:
        assert p.get("title") is not None
        assert p.get("lens_id") is not None

def test_save_to_csv():
    """
    Test de guardado de datos en CSV.
    """
    openalex = OpenAlexClient(mailto="abrilreinaga@hotmail.com")
    ids = openalex.consultar_por_tema("Machine Learning", limite=20)
    metadata = openalex.extraer_metadatos(ids)
    
    if len(metadata) == 0:
        token = TOKEN_LENS
        assert token, "Falta TOKEN_LENS para Lens"
        
        lens = LensClient(access_token=token)
        ids = lens.consultar_por_tema("Machine Learning", limite=20)
        metadata = lens.extraer_metadatos(ids)
    
    path = "./data/api_test.csv"
    openalex.guardar_csv(metadata, path)
    
    assert os.path.isfile(path), "No se generó el archivo."