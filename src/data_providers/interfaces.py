# Packages

from abc import ABC, abstractmethod

# Data Feed Interface


class DataFeedInterface(ABC):
    @abstractmethod
    def fetch_data(self):
        """Fetch data from the data feed."""
        pass

    @abstractmethod
    def process_data(self):
        """Process fetched database."""
        pass

    @abstractmethod
    def export_data(self):
        """Export dataframe to another file format."""
        pass
