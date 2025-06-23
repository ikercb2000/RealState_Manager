# Project Modules

from src.data_providers.interfaces import DataFeedInterface

# Packages

import pandasdmx as pdmx
import polars as pl

# OECD


class OECDDataFeed(DataFeedInterface):

    def __init__(self):

        self.oecd = pdmx.Request("OECD")

    def fetch_data(self, resource_id: str, key: str):

        data = self.oecd.data(resource_id=resource_id, key=key).to_pandas()
        df = pl.from_dataframe(data)

        return df
