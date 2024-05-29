import os
import pickle
from pprint import pprint
from typing import Iterable

from asammdf import MDF
from pandas import DataFrame

from processing.calculators import YourCalculator
from processing.models import Event, Results


def get_events(df: DataFrame, file_path: str) -> Iterable[Event]:
    '''
    Implementira logiku za detekciju evenata
    '''
    events = list()

    filtered_df = df[(df['SPEED'] >= 40) & (df['SPEED'] <= 60)]

    if len(filtered_df) == 0:
        raise Exception(f"Nema intervala u kojima je brzina izmedu 40 i 60 km/h.")
    
    in_interval = False
    last_start = None
    for index, row in df.iterrows():
        if (in_interval == True) and ((row['SPEED'] < 40) or (row['SPEED'] > 60)):
            events.append(Event(last_start, index, file_path)) # type: ignore
            in_interval = False
        elif (in_interval == False) and (row['SPEED'] >= 40) and (row['SPEED'] <= 60):
            last_start = index
            in_interval = True
    
    return events


def get_dataframe_from_mf4(file_path: str) -> DataFrame:
    #Implementira logiku za učitavanje mdf datoteka u dataframe koji se zove dataframe
    mdf_obj = MDF(file_path)
    dataframe = mdf_obj.to_dataframe()
    return dataframe

def processing_flow_logic(file_path: str, result_output_path: str):
    dataframe = get_dataframe_from_mf4(file_path)
    try:
        events = get_events(df=dataframe, file_path=file_path)
    except Exception as e:
        print(f"{file_path}: {e}\n")
        return

    calculator = YourCalculator()

    calculated = {}
    for event in events:
        try:
            calculated[hash(event)] = calculator.calculate(dataframe, event)
        except Exception:
            print(f"{file_path}: Could not calculate for event on file.\n")
            pass

    result = Results()
    result.events = list(events)
    result.calculations = calculated

    file_name = f'{result_output_path}\\{file_path.split("\\")[-1].split(".")[0]}.pickle'
    with open(file_name, 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open(file_name, 'rb') as handle:
        data_from_pickle = pickle.load(handle)
    
    pprint(data_from_pickle)
