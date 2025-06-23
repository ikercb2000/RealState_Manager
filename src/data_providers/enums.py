# Packages

from enum import Enum

# Enums

cities = Enum("cities", ["London", "Coventry", "Bristol",
              "Oxford", "Madrid", "Barcelona", "Valencia", "Laussane", "Zurich", "Geneva"])

countries = Enum("countries", ["UK", "CH", "SP"])

file_types = Enum("file_types", ["Excel", "CSV", "Text"])
