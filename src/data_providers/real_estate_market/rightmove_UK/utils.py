# Project Modules

from src.data_providers.real_estate_market.rightmove_UK.enums import cities, property_types, added_to_site, sale_or_rent, radius, bedrooms
from src.data_providers.real_estate_market.rightmove_UK.dicts import UK_cities_ids

# Rightmove URLs Auxiliary Class


class RightmoveURL:

    @staticmethod
    def construct_rightmove_url(
        action: sale_or_rent,
        city: cities,
        type: property_types,
        added_time: added_to_site,
        rad: radius,
        min_price=None,
        max_price=None,
        min_bedrooms=bedrooms,
        max_bedrooms=bedrooms,
        include_option=False,
    ):
        """Construct a Rightmove URL for sale or rent based on parameters."""

        search_type = "property-for-sale" if action == sale_or_rent.Sale else "property-to-rent"
        base_url = f"https://www.rightmove.co.uk/{search_type}/find.html?"

        # Convert enum bedrooms
        min_bedrooms = RightmoveURL.bedrooms_url(min_bedrooms)
        max_bedrooms = RightmoveURL.bedrooms_url(max_bedrooms)

        if max_bedrooms is not None and min_bedrooms is not None and max_bedrooms < min_bedrooms:
            raise ValueError(
                "Maximum number of bedrooms must be greater than or equal to the minimum.")

        # Convert price to nearest allowed
        if min_price is not None:
            if min_price < 0:
                raise ValueError("Price must be non-negative.")
            min_price = (
                RightmoveURL.sale_price_url(min_price)
                if action == sale_or_rent.Sale
                else RightmoveURL.rent_price_url(min_price)
            )

        if max_price is not None:
            if max_price < 0:
                raise ValueError("Price must be non-negative.")
            max_price = (
                RightmoveURL.sale_price_url(max_price)
                if action == sale_or_rent.Sale
                else RightmoveURL.rent_price_url(max_price)
            )

        if max_price is not None and min_price is not None and max_price < min_price:
            raise ValueError(
                "Maximum price must be greater than or equal to minimum.")

        params = {
            "searchLocation": city._name_,
            "useLocationIdentifier": "true",
            "locationIdentifier": f"REGION%{UK_cities_ids[city]}",
            "buy": "For+sale" if action == sale_or_rent.Sale else None,
            "rent": "To+rent" if action == sale_or_rent.Rent else None,
            "radius": RightmoveURL.radius_url(rad),
            "minPrice": str(min_price) if min_price != None else None,
            "maxPrice": str(max_price) if max_price != None else None,
            "minBedrooms": str(min_bedrooms) if min_bedrooms != None else None,
            "maxBedrooms": str(max_bedrooms) if max_bedrooms != None else None,
            "propertyTypes": RightmoveURL.property_url(type),
            "maxDaysSinceAdded": RightmoveURL.time_url(added_time),
            "_includeSSTC": "on" if action == sale_or_rent.Sale and include_option else None,
            "_includeLetAgreed": "on" if action == sale_or_rent.Rent and include_option else None,
        }

        if params["_includeSSTC"] == "on":
            params["includeSSTC"] = "true"

        if params["_includeLetAgreed"] == "on":
            params["includeLetAgreed"] = "true"

        query_string = "&".join(
            f"{key}={value}" for key, value in params.items() if value is not None)
        return f"{base_url}{query_string}"

    @staticmethod
    def property_url(type: property_types):
        """Translate property type enum to Rightmove URL parameter."""
        if type == property_types.Any:
            return
        elif type == property_types.Flats:
            return "flat"
        elif type == property_types.Houses:
            return "house"
        elif type == property_types.Commercial:
            return "commercial"
        elif type == property_types.Land:
            return "land"
        elif type == property_types.Bungalows:
            return "bungalow"

    @staticmethod
    def radius_url(rad: radius):
        radius_map = {
            radius.Zero: 0.0,
            radius.One_fourth: 0.25,
            radius.One_half: 0.5,
            radius.One: 1.0,
            radius.Three: 3.0,
            radius.Five: 5.0,
            radius.Ten: 10.0,
            radius.Fifteen: 15.0,
            radius.Twenty: 20.0,
            radius.Thirty: 30.0,
            radius.Forty: 40.0,
        }
        return radius_map.get(rad)

    @staticmethod
    def time_url(site: added_to_site):
        time_map = {
            added_to_site.Anytime: "",
            added_to_site.Last_24_H: 1,
            added_to_site.Last_3_D: 3,
            added_to_site.Last_7_D: 7,
            added_to_site.Last_14_D: 14,
        }
        return time_map.get(site)

    @staticmethod
    def bedrooms_url(rooms: bedrooms):
        bedroom_map = {
            bedrooms.Studio: 0,
            bedrooms.One: 1,
            bedrooms.Two: 2,
            bedrooms.Three: 3,
            bedrooms.Four: 4,
            bedrooms.Five: 5,
        }
        return bedroom_map.get(rooms)

    @staticmethod
    def sale_price_url(sale_price: int):
        sale_prices = [
            50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 125000, 130000,
            140000, 150000, 160000, 170000, 175000, 180000, 190000, 200000, 210000, 220000,
            230000, 240000, 250000, 260000, 270000, 280000, 290000, 300000, 325000, 350000,
            375000, 400000, 425000, 450000, 475000, 500000, 550000, 600000, 650000, 700000,
            800000, 900000, 1000000, 1250000, 1500000, 1750000, 2000000, 2500000, 3000000,
            4000000, 5000000, 7500000, 10000000, 15000000, 20000000,
        ]
        return min(sale_prices, key=lambda x: abs(x - sale_price))

    @staticmethod
    def rent_price_url(rent_price: int):
        rent_prices = [
            100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900,
            1000, 1100, 1200, 1250, 1300, 1400, 1500, 1750, 2000, 2250, 2500,
            2750, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 8000,
            9000, 10000, 12500, 15000, 17500, 20000, 25000, 30000, 35000, 40000,
        ]
        return min(rent_prices, key=lambda x: abs(x - rent_price))
