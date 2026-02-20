import scrapy


class ProductoItem(scrapy.Item):
    nombre = scrapy.Field()
    precio_actual = scrapy.Field()
    precio_anterior = scrapy.Field()
    descuento = scrapy.Field()
    ubicacion = scrapy.Field()
    cuotas = scrapy.Field()
    envio_gratis = scrapy.Field()
    enlace = scrapy.Field()
    categoria = scrapy.Field()
    fecha_extraccion = scrapy.Field()
