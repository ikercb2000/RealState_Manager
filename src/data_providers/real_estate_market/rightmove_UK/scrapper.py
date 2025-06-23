# Packages

from lxml import html
import requests
import polars as pl
import datetime as dt
import re

# Scrapper Classes


class _GetDataFromURL:
    """Scraper para extraer listings de Rightmove, adaptado a la nueva estructura HTML."""

    def __init__(self, url: str):
        self.url = url
        self.first_page, self.status = self.make_request(self.url)
        if self.status != 200:
            raise ValueError(f"Error al contactar Rightmove ({self.status})")
        self.get_results = self.__get_results

    @staticmethod
    def make_request(url: str):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        r = requests.get(url, headers=headers)
        return r.content, r.status_code

    def get_page(self, content: bytes) -> pl.DataFrame:
        tree = html.fromstring(content)
        cards = tree.xpath(
            '//div[contains(@class,"PropertyCard_propertyCardContainer")]')

        rows = []
        for c in cards:
            href = c.xpath(
                './/a[@data-testid="property-details-lozenge"]/@href')
            url = href[0] if href else None
            pid = None
            if url:
                m = re.search(r"/properties/(\d+)", url)
                pid = int(m.group(1)) if m else None

            price = c.xpath(
                './/div[contains(@class,"PropertyPrice_price")]/text()')
            addr = c.xpath(
                './/address[contains(@class,"PropertyAddress_address")]/text()')
            ptype = c.xpath(
                './/span[contains(@class,"PropertyInformation_propertyType")]/@aria-label')
            beds = c.xpath(
                './/span[contains(@class,"PropertyInformation_bedroomsCount")]/text()')
            baths = c.xpath(
                './/span[contains(@class,"PropertyInformation_bathroomsCount")]/text()')
            desc = c.xpath(
                './/p[contains(@class,"PropertyInformation_description")]/text()')
            epc = c.xpath(
                './/span[contains(@class,"EpcRating_epcRating")]/text()')
            furnish = c.xpath(
                './/span[contains(@class,"PropertyInformation_furnishingStatus")]/text()')
            img = c.xpath('.//img[contains(@class,"PropertyCard_image")]/@src')
            tim = c.xpath(
                './/span[contains(@class,"MarketedBy_addedOrReduced")]/text()')
            agent = c.xpath(
                './/div[contains(@class,"PropertyCard_propertyCardEstateAgent")]'
                '//a[contains(@href,"estate-agents")]/@href'
            )

            rows.append({
                "id":              pid,
                "url":             url,
                "price":           price[0].strip() if price else None,
                "address":         addr[0].strip() if addr else None,
                "property_type":   ptype[0] if ptype else None,
                "bedrooms":        int(beds[0]) if beds else None,
                "bathrooms":       int(baths[0]) if baths else None,
                "snippet":         desc[0].strip() if desc else None,
                "epc_rating":      epc[0] if epc else None,
                "furnishing":      furnish[0] if furnish else None,
                "image_url":       img[0] if img else None,
                "time_in_market":  tim[0].strip() if tim else None,
                "agent_url":       agent[0] if agent else None,
            })

        return pl.DataFrame(rows)

    @property
    def __get_results(self) -> pl.DataFrame:
        # Primera página
        df = self.get_page(self.first_page)

        # Paginación hasta que no haya más resultados
        page = 1
        while True:
            next_url = f"{self.url}&index={page * 24}"
            content, status = self.make_request(next_url)
            if status != 200:
                break
            tmp = self.get_page(content)
            if tmp.height == 0:
                break
            df = pl.concat([df, tmp])
            page += 1

        # Limpieza y transformaciones finales
        return (
            df
            .with_columns([
                # Convertir precio a entero
                pl.col("price")
                  .str.replace_all(r"[£,pcmwp ]", "")
                  .cast(pl.Int64, strict=False),
                # Rellenar nulls y strip de espacios
                pl.col("address").fill_null("").str.strip_chars(),
                pl.col("property_type").fill_null("").str.strip_chars(),
                pl.col("snippet").fill_null("").str.strip_chars(),
                pl.col("epc_rating").fill_null("").str.strip_chars(),
                pl.col("furnishing").fill_null("").str.strip_chars(),
                pl.col("time_in_market").fill_null("").str.strip_chars(),
            ])
            .with_columns([
                # Añadir fecha de búsqueda
                pl.lit(dt.datetime.today()).alias("search_date")
            ])
        )


class rightmove_data:
    """Wrapper de resultados para usar en RightmoveDataFeed."""

    def __init__(self, url: str):
        self.__request_object = _GetDataFromURL(url)
        self.__url = url

    @property
    def url(self) -> str:
        return self.__url

    @property
    def get_results(self) -> pl.DataFrame:
        return self.__request_object.get_results

    @property
    def results_count(self) -> int:
        return self.get_results.height

    @property
    def average_price(self) -> int:
        df = self.get_results
        total = df["price"].sum()
        return int(total / df.height) if df.height else 0

    def summary(self, by: str = "bedrooms") -> pl.DataFrame:
        df = self.get_results.drop_nulls("price")
        return (
            df
            .groupby(by)
            .agg([
                pl.count("price").alias("count"),
                pl.mean("price").cast(pl.Int64).alias("mean"),
            ])
            .sort(by)
        )
