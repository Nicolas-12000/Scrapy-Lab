import csv
import os
from datetime import datetime


class CsvExportPipeline:
    """Pipeline que acumula items; el export real lo hace Scrapy FEEDS."""

    def process_item(self, item, spider):
        return item
