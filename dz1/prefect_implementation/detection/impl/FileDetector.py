import os
from typing import Iterable

from prefect_implementation.detection.IDetectionAPI import IDetectionAPI


class FileDetector(IDetectionAPI):

    def __init__(self, files_sources: Iterable[str]):
        self.files_sources = list(files_sources)

    def detect_files(self) -> Iterable[str]:
        '''
        Metodu za detekciju datoteka iz direktorija.
        U konstruktoru je specificirana lista direktorija iz kojih se učitavaju sve datoteke koje će se procesirati
        Datoteke se učitaju te metoda vraća listu ili set kao rezultat
        Bonus: može se dodatno ubaciti filtriranje gdje će se vraćati samo određeni tip datoteka (npr. .mf4 u ovom slučaju)
        '''

        mdf_files_set = set()

        for folder in self.files_sources:
            for source in os.listdir(folder):
                source_path = os.path.join(folder, source)
                
                if os.path.isdir(source_path):
                    self.files_sources.append(source_path)
                
                elif os.path.isfile(source_path):
                    _, file_extension = os.path.splitext(source)
                    if file_extension == ".mf4":
                        mdf_files_set.add(source_path)
        
        return mdf_files_set