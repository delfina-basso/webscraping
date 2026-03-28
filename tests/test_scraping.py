"""
Tests para el módulo de web scraping.
"""
import os
import csv
from src.scraping.eventseye import crawler_eventseye
from src.scraping.nferias import crawler_nferias
from src.scraping.tentimes import crawler_10times

def test_eventseye_scraping():
    """
    Test de scraping de eventseye.com.
    """
    csv_real = "./data/eventos.csv"
    crawler_eventseye(max_paginas=5, retraso=0)
    filas = read_csv(csv_real)

    assert len(filas) > 0, "El scraper no devolvió nada"
    assert "Nombre del evento" in filas[0], "Falta campo: Nombre del evento"
    assert "Fecha" in filas[0], "Falta campo: Fecha"

def test_nferias_scraping():
    """
    Test de scraping de nferias.com.
    """
    csv_real = "./data/eventos.csv"
    crawler_nferias(max_paginas=5, retraso=0)
    filas = read_csv(csv_real)

    assert len(filas) > 0, "El scraper no devolvió nada"
    assert "Nombre del evento" in filas[0]
    assert "Fecha" in filas[0]


def test_10times_scraping():
    """
    Test de scraping de 10times.com.
    """
    csv_real = "./data/eventos.csv"
    crawler_10times(max_paginas=5, retraso=0)
    filas = read_csv(csv_real)
    
    assert len(filas) > 0, "El scraper no devolvió nada"
    assert "Nombre del evento" in filas[0], "Falta campo: Nombre de evento"
    assert "Fecha" in filas[0], "Falta campo: Fecha"

def read_csv(path):
    assert os.path.exists(path), f"No existe {path}"
    assert os.path.getsize(path) > 0, f"CSV {path} vacío."
    
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)