"""
main.py  –  Orquestador del pipeline completo.

Pasos:
  1. Scraping   → genera productos.csv
  2. DB setup   → crea base de datos y tabla si no existen
  3. Carga      → inserta el CSV en PostgreSQL
  4. Análisis   → ejecuta las 9 consultas SQL y las imprime

Uso:
  python main.py              # pipeline completo
  python main.py --skip-scrape  # solo carga + análisis (útil si ya tienes el CSV)
  python main.py --only-analysis  # solo ejecuta las consultas SQL
"""

import argparse
import os
import sys

# Asegurar que el proyecto raíz esté en el path
sys.path.insert(0, os.path.dirname(__file__))


def run_scraping():
    """Lanza los tres spiders de Scrapy en secuencia."""
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    os.chdir(os.path.dirname(__file__))  # el scrapy.cfg debe estar aquí

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    from scraper.spiders.laptops_spider import LaptopsSpider
    from scraper.spiders.celulares_spider import CelularesSpider
    from scraper.spiders.televisores_spider import TelevisoresSpider

    process.crawl(LaptopsSpider)
    process.crawl(CelularesSpider)
    process.crawl(TelevisoresSpider)

    print("[SCRAPER] Iniciando spiders: laptops, celulares, televisores …")
    process.start()  # bloquea hasta que todos terminen
    print("[SCRAPER] Scraping finalizado. Archivo productos.csv generado.")


def run_db_setup():
    """Crea la DB y la tabla si no existen."""
    from database.schema import create_database_if_not_exists, create_tables

    create_database_if_not_exists()
    create_tables()


def run_load():
    """Carga el CSV en PostgreSQL."""
    from database.loader import load_csv_to_db

    load_csv_to_db()


def run_analysis():
    """Ejecuta las consultas SQL analíticas."""
    from analysis.queries import run_all

    run_all()


# ------------------------------------------------------------------ #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ML Scraper")
    parser.add_argument(
        "--skip-scrape",
        action="store_true",
        help="Saltar el scraping (usa el CSV existente)",
    )
    parser.add_argument(
        "--only-analysis",
        action="store_true",
        help="Ejecutar solo el análisis SQL (la DB ya debe tener datos)",
    )
    args = parser.parse_args()

    if args.only_analysis:
        run_analysis()
        sys.exit(0)

    if not args.skip_scrape:
        run_scraping()

    run_db_setup()
    run_load()
    run_analysis()
