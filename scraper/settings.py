BOT_NAME = "ml_scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# --- Identificación del bot (respetuoso con el sitio) ---
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# --- Respetar robots.txt ---
ROBOTSTXT_OBEY = True

# --- Throttle: una petición cada 2-4 segundos para no saturar ---
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 8
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2

# --- Headers para parecer un browser normal ---
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

# --- Pipelines ---
ITEM_PIPELINES = {
    "scraper.pipelines.CsvExportPipeline": 300,
}

# --- Exportar CSV ---
FEEDS = {
    "productos.csv": {
        "format": "csv",
        "encoding": "utf-8",
        "store_empty": False,
        "overwrite": True,
        "fields": [
            "nombre", "precio_actual", "precio_anterior",
            "descuento", "ubicacion", "cuotas",
            "envio_gratis", "enlace", "categoria", "fecha_extraccion",
        ],
    }
}

# --- Misc ---
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = "INFO"
