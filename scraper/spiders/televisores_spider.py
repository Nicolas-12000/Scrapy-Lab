from scraper.spiders.base_spider import MercadoLibreBaseSpider


class TelevisoresSpider(MercadoLibreBaseSpider):
    name = "televisores"
    categoria = "televisores"
    start_urls = ["https://listado.mercadolibre.com.ar/televisores"]
    max_pages = 5  # ~240 productos
