from scraper.spiders.base_spider import MercadoLibreBaseSpider


class CelularesSpider(MercadoLibreBaseSpider):
    name = "celulares"
    categoria = "celulares"
    start_urls = ["https://listado.mercadolibre.com.ar/celulares-telefonos"]
    max_pages = 5  # ~240 productos
