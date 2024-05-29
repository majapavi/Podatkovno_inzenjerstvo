from abc import abstractmethod
from typing import List, Dict
from pandas import DataFrame
from processing.models import Event

class ICalculator:
    def calculate(self, dataframe: DataFrame, event: Event, wanted_channels=List[str]) -> Dict[str, float]:
        dataframe_event_chunk = dataframe.query(f"{event.start}<index<{event.end}")
        result = self.calculate_on_dataframe_chunk(dataframe_event_chunk)
        wanted_channels = dataframe.columns.to_list()
        return result.get(wanted_channels).to_dict()    # type: ignore

    @abstractmethod
    def calculate_on_dataframe_chunk(self, dataframe_chunk: DataFrame) -> DataFrame:
        # Implementirano u implementacijskoj klasi
        raise NotImplementedError("Implement this abstract method in child classes!")

class YourCalculator(ICalculator):
    # Implementacijska klasa ICalculator abstraktne klase
    def calculate_on_dataframe_chunk(self, dataframe_chunk: DataFrame) -> DataFrame:
        return dataframe_chunk.agg(['min', 'max', 'mean', 'std'])