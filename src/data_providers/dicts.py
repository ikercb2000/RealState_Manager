# Project Modules

from src.data_providers.enums import countries, cities

# Country-cities Mapping Dictionary


country_cities = {
    countries.UK: [cities.Bristol, cities.Coventry,
                   cities.London, cities.Oxford],
    countries.SP: [cities.Madrid, cities.Barcelona, cities.Valencia],
    countries.CH: [cities.Laussane, cities.Zurich, cities.Geneva],
}
