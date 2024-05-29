from typing import List, Tuple, Iterable

from asammdf import MDF

from prefect_implementation.quality_check.IQualityCheck import IQualityCheck


class QualityCheck(IQualityCheck):
    def check_quality(self, paths: Iterable[str]) -> Tuple[List[str], List[str]]:
        '''
        Metoda za filtriranje fajlova.
        Ocekivano ponašanje: u konstruktoru je specificirana lista putanja do datoteka
        Datoteke koje se ne ponašaju u skladu sa očekivanim ponašanjem se vraćaju u listi loših datoteka
        Očekivani rezultat se treba vratiti kao tuple lista, lista, npr. ["a.txt", "b.txt"], ["c.txt"]
        '''
        valid_files = []
        unvalid_files = []

        for source_path in paths:
            try:
                mdf_obj = MDF(source_path)
            except:
                print(f"{source_path}: Ne moze se otvoriti kao MDF datoteka.\n")
                unvalid_files.append(source_path)
                continue
            
            try:
                df = mdf_obj.to_dataframe()
            except:
                print(f"{source_path}: Ne moze se ucitati u dataframe.\n")
                unvalid_files.append(source_path)
                continue

            try:
                if df.empty:
                    raise Exception("Prazna datoteka.")
            except Exception as e:
                print(f"{source_path}: {e}\n")
                unvalid_files.append(source_path)
                continue

            try:
                if 'SPEED' not in df.columns:
                    raise ValueError("Stupac SPEED ne postoji.\n")
            except ValueError as e:
                    print(f"{source_path}: {e}\n")
                    unvalid_files.append(source_path)
                    continue

            try:
                if (df['SPEED'] < 0).any() or (df['SPEED'] > 300).any():
                    raise ValueError("Nedozvoljene vrijednosti u varijabli SPEED.\n")
            except ValueError as e:
                    print(f"{source_path}: {e}\n")
                    unvalid_files.append(source_path)
                    continue

            valid_files.append(source_path)

        quality_separated_files = (valid_files, unvalid_files)
        return quality_separated_files
