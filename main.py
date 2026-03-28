"""
Trabajo Práctico: Recuperación de Información en la Web
Universidad Nacional de Tres de Febrero - Estructuras de Datos

Este programa integra técnicas de:
- Consultas a APIs (OpenAlex, The Lens)
- Web Scraping (eventos y ferias)
- Procesamiento RSS (noticias de comercio internacional)

Autores: [Completar con nombres del equipo]
Fecha: Noviembre 2025
"""

import sys

from src.interfaz import menu

def main():
    """
    Punto de entrada principal del programa.
    Inicia la interfaz de consola interactiva.
    """
    print("=" * 70)
    print("  Trabajo Práctico: Recuperación de Información en la Web")
    print("  Universidad Nacional de Tres de Febrero")
    print("=" * 70)
    print()

    try:
        # Iniciar interfaz de consola
        menu.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario!")
        print("Hasta luego.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError inesperado: {e}")
        print("Por favor, revise el código y vuelva a intentar.")
        sys.exit(1)


if __name__ == "__main__":
    main()
