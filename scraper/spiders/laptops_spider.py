from scraper.spiders.base_spider import MercadoLibreBaseSpider


class LaptopsSpider(MercadoLibreBaseSpider):
    name = "laptops"
    categoria = "laptops"
    start_urls = ["https://listado.mercadolibre.com.ar/laptops"]
    max_pages = 5  # ~240 productos
