# Project Modules

from src.data_feeds.enums import cities, file_types

# Packages

from enum import Enum

# Enums

property_types = Enum("property_types", [
                      "Any", "Houses", "Flats", "Bungalows", "Land", "Commercial", "Other"])

added_to_site = Enum("added_to_site", [
    "Last_24_H", "Last_3_D", "Last_7_D", "Last_14_D", "Anytime"])

sale_or_rent = Enum("sale_or_rent", ["Sale", "Rent"])

radius = Enum("radius", ["Zero", "One_fourth", "One_half", "One",
              "Three", "Five", "Ten", "Fifteen", "Twenty", "Thirty", "Forty"])

bedrooms = Enum("bedrooms", ["Studio", "One", "Two", "Three", "Four", "Five"])
