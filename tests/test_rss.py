"""
Tests para el módulo de RSS.
"""

import pytest
import os
import pandas as pd
import feedparser
from src.rss import procesador_de_feeds as pf

@pytest.fixture
def sample_entry():
    return {
        "title": "China’s Deflationary Pressures Eased in October",
        "publication_date": "Sun, 09 Nov 2025 02:51:00 GMT",
        "summary": "<p>China’s downward price pressures further eased in October.</p>",
        "country": "China"
    }

def test_clarin_rss_feed():
    """
    Test de lectura del feed RSS de Clarin.
    """
    feed = feedparser.parse(pf.feed_URLs["Clarin"])
    assert feed.entries, "El feed de Clarin no tiene contenido"

def test_economista_rss_feed():
    """
    Test de lectura del feed RSS de El Economista.
    """
    feed = feedparser.parse(pf.feed_URLs["El Economista"])
    assert feed.entries, "El feed de El Economista no tiene contenido"

def test_wsj_rss_feed():
    """
    Test de lectura del feed RSS de Wall Street Journal.
    """
    feed = feedparser.parse(pf.feed_URLs["Wall Street Journal"])
    assert feed.entries, "El feed de Wall Street Journal no tiene contenido"

def test_parse_news_item(sample_entry):
    """
    Test de parsing de un item de noticia.
    """
    example = sample_entry
    
    title = example.get("title")
    summary = pf.clean_html_tags(example.get("summary"))
    
    assert title == "China’s Deflationary Pressures Eased in October"
    assert summary == "China’s downward price pressures further eased in October."

def test_extract_country(sample_entry):
    """
    Test de extracción de país asociado a noticia.
    """
    example = sample_entry
    cty = pf.get_country_name(example)
    assert cty == "China"
    
def test_extract_country_fail():
    """
    Test erróneo de extracción de país asociado a noticia.
    """
    entry = {
        "title": "Apple updates App Store",
        "description": "Now we can look through apps more easily."
    }

    cty = pf.get_country_name(entry)
    assert cty == "Country not specified"

def test_save_news_to_csv():
    """
    Test de guardado de noticias en CSV.
    """
    url = pf.feed_URLs["Wall Street Journal"]
    csv_path = "./data/noticias_test.csv"
    
    pf.process_rss_feeds("Wall Street Journal", url, csv_path)
    
    assert os.path.exists(csv_path), "El archivo no existe"
    
    data_frame = pd.read_csv(csv_path)
    
    assert not data_frame.empty, "El archivo esta vacio"
    
    expected_columns = {"title", "publication_date", "summary", "country"}
    
    assert expected_columns.issubset(set(data_frame.columns)), "No se encuentras las columnas solicitadas"
    
