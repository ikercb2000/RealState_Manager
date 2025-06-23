# Project Modules

from src.data_providers.interfaces import DataFeedInterface
from src.data_providers.real_estate_market.rightmove_UK.enums import *
from src.data_providers.real_estate_market.rightmove_UK.utils import RightmoveURL
from src.data_providers.real_estate_market.rightmove_UK.scrapper import rightmove_data

# Packages

import polars as pl
from pathlib import Path

# Rightmove Data Feed Class


class RightmoveDataFeed(DataFeedInterface):

    def fetch_data(self, sale_or_rent: sale_or_rent, city: cities, radius: radius,
                   property_type: property_types, added_when: added_to_site, min_price: int, max_price: int, min_bedrooms: bedrooms,
                   max_bedrooms: bedrooms, include_option: bool):
        """Fetch data from the Idealista data feed."""
        url = RightmoveURL.construct_rightmove_url(
            action=sale_or_rent,
            city=city,
            type=property_type,
            added_time=added_when,
            min_price=min_price,
            max_price=max_price,
            min_bedrooms=min_bedrooms,
            max_bedrooms=max_bedrooms,
            rad=radius,
            include_option=include_option,
        )

        print(f"\n\nObtained URL:\n\n{url}\n\n")

        data = rightmove_data(url)
        df = data.get_results
        return df

    def process_data(self):
        """Process fetched database."""
        pass

    def export_data(self, df: pl.DataFrame,
                    file_type: file_types,
                    location_path: str,
                    file_name: str = "data"):
        """
        Export DataFrame to Excel, CSV, and plain text formats.
        """

        out_dir = Path(location_path)
        out_dir.mkdir(parents=True, exist_ok=True)

        path = out_dir / \
            f"{file_name}.{RightmoveDataFeed.find_extension(file_type)}"

        if file_type == file_types.Excel:
            pdf = df.to_pandas()
            pdf.to_excel(str(path), index=False)
        elif file_type == file_types.CSV:
            df.write_csv(str(path))
        elif file_type == file_types.Text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(pdf.to_string(index=False))

        print(
            f"\n\nExported database to {file_type._name_.lower()}. Path: {path}\n\n")

    @staticmethod
    def find_extension(file_type: file_types):

        if file_type == file_types.Excel:
            return "xlsx"
        elif file_type == file_types.CSV:
            return "csv"
        elif file_type == file_types.Text:
            return "txt"
