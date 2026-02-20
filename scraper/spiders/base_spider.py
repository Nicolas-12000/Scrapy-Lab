"""
Spider base para MercadoLibre Argentina.

Reglas respetadas según robots.txt:
- Crawl-delay implícito vía AutoThrottle (2-8 seg).
- No se accede a rutas disallow: /gz/cart/, /navigation/, /recommendations*, etc.
- Se scrape solo la página de listados públicos (/listado.mercadolibre.com.ar/<keyword>).
"""

import re
from datetime import datetime, timezone

import scrapy

from scraper.items import ProductoItem


class MercadoLibreBaseSpider(scrapy.Spider):
    """Spider genérico: recibe `start_url` y `categoria` como parámetros de clase."""

    items_per_page = 48      # ML muestra 48 productos por página
    max_pages = 5            # Límite para no sobrecargar el servidor

    def parse(self, response, page=1, **kwargs):
        products = response.css("li.ui-search-layout__item")

        if not products:
            self.logger.warning("No se encontraron productos en %s", response.url)
            return

        for product in products:
            item = self._parse_product(product)
            if item["nombre"]:
                yield item

        # Paginación: ML usa _Desde_N donde N = (page * items_per_page) + 1
        if page < self.max_pages:
            next_offset = page * self.items_per_page + 1
            # Construimos la URL de la siguiente página
            base_url = self._get_base_url()
            next_url = f"{base_url}_Desde_{next_offset}_NoIndex_True"
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                cb_kwargs={"page": page + 1},
            )

    def _get_base_url(self):
        """Subclases deben definir start_urls[0]; aquí lo reutilizamos."""
        return self.start_urls[0]

    def _parse_product(self, product):
        item = ProductoItem()

        # --- Nombre ---
        item["nombre"] = (
            product.css(".poly-component__title::text").get("")
            or product.css("h2.ui-search-item__title::text").get("")
        ).strip()

        # --- Precio actual ---
        item["precio_actual"] = self._parse_price(
            product.css(".poly-price__current .andes-money-amount__fraction::text").get()
            or product.css(".price-tag-fraction::text").get()
        )

        # --- Precio anterior ---
        item["precio_anterior"] = self._parse_price(
            product.css(
                ".andes-money-amount--previous .andes-money-amount__fraction::text"
            ).get()
        )

        # --- Descuento ---
        discount_text = (
            product.css(".andes-money-amount__discount::text").get("")
            or product.css(".ui-search-price__discount::text").get("")
        ).strip()
        item["descuento"] = self._parse_discount(discount_text)

        # --- Ubicación del vendedor ---
        item["ubicacion"] = (
            product.css(".poly-component__location::text").get("")
            or product.css(".ui-search-item__location::text").get("")
        ).strip()

        # --- Cuotas ---
        cuotas_raw = (
            product.css(".poly-price__installments::text").getall()
            or product.css(".ui-search-installments::text").getall()
        )
        item["cuotas"] = " ".join(t.strip() for t in cuotas_raw if t.strip()) or None

        # --- Envío gratis ---
        shipping_text = " ".join(
            product.css(".poly-component__shipping *::text").getall()
            + product.css(".ui-search-item__shipping *::text").getall()
        ).lower()
        item["envio_gratis"] = "gratis" in shipping_text

        # --- Enlace ---
        link = (
            product.css(".poly-component__title a::attr(href)").get()
            or product.css("h2.ui-search-item__title a::attr(href)").get()
            or product.css("a.ui-search-link::attr(href)").get()
            or ""
        )
        # Limpiar parámetros de tracking
        item["enlace"] = link.split("#")[0] if link else None

        # --- Categoría y fecha ---
        item["categoria"] = self.categoria
        item["fecha_extraccion"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        return item

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_price(raw):
        """Convierte '1.503.899' → 1503899.0 o None si no hay valor."""
        if not raw:
            return None
        cleaned = re.sub(r"[^\d,]", "", raw).replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return None

    @staticmethod
    def _parse_discount(raw):
        """Extrae número entero de '23% OFF' → 23 o None."""
        if not raw:
            return None
        match = re.search(r"(\d+)", raw)
        return int(match.group(1)) if match else None
