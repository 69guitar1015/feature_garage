from typing import List
import logging
import pathlib
import numpy as np
import pandas as pd

class Garage:
    def __init__(self, dirpath: str):
        self.dirpath = pathlib.Path(dirpath)
        self.logger = logging.getLogger('FeatureGarage')

    def save(self, df: pd.DataFrame, table: str, columns: List[str]=None, overwrite: bool=False, verbose: int=1):
        tablepath = self.dirpath/table
        existings = self.columns(table)

        if not tablepath.exists():
            tablepath.mkdir(parents=True)

        for column in df.columns:
            if columns is not None and column not in columns:
                continue

            if column in existings:
                if verbose > 0:
                    msg = f'{column} column is already existing.'
                    if overwrite:
                        msg += 'it will be overwritten.'
                    else:
                        msg += 'if you would like to overwrite it, please specify overwrite=1'
                    self.logger.warning(msg)

                if not overwrite:
                    continue

            np.save(tablepath/f"{column}.npy", df[column])

    def load(self, table: str, columns: List[str]=None) -> pd.DataFrame:
        df = {}
        for path in (self.dirpath/table).glob('*.npy'):
            if columns is not None and path.stem not in columns:
                continue

            df[path.stem] = np.load(path)

        return pd.DataFrame(df)

    def tables(self) -> List[str]:
        return [str(path.relative_to(self.dirpath)) for path in self.dirpath.glob('*')]

    def columns(self, table: str) -> List[str]:
        return [path.stem for path in (self.dirpath/table).glob('*.npy')]
