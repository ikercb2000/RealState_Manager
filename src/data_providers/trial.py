# Project Modules

from src.data_providers.real_estate_market.rightmove_UK.data_class import RightmoveDataFeed
from src.data_providers.real_estate_market.rightmove_UK.enums import *
from src.data_providers.enums import *

# Packages

import os

# Rightmove UK Data Feed

rm = RightmoveDataFeed()

data = rm.fetch_data(sale_or_rent.Rent, cities.London, radius.Five, property_types.Flats, added_to_site.Anytime,
                     min_price=500, max_price=850, min_bedrooms=1, max_bedrooms=4, include_option=True)

print(data)

rm.export_data(data, file_type=file_types.CSV,
               file_name="data_rightmove_UK", location_path=f"{os.getcwd()}/exported_data")
