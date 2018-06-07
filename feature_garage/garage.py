from typing import List
import logging
import pathlib
import numpy as np
import pandas as pd
from base64 import urlsafe_b64encode, urlsafe_b64decode


def b64_encode(s: str) -> str:
    b = s.encode('utf-8')
    return urlsafe_b64encode(b).decode('utf-8')


def b64_decode(s: str) -> str:
    b = s.encode('utf-8')
    return urlsafe_b64decode(b).decode('utf-8')


class Garage:
    def __init__(self, dirpath: str):
        self.dirpath = pathlib.Path(dirpath)
        self.logger = logging.getLogger('FeatureGarage')

    def save(self, df: pd.DataFrame, table: str,
             columns: List[str]=None, overwrite: bool=False, verbose: int=1):
        tablepath = self.dirpath/b64_encode(table)
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
                        msg += 'if you would like to overwrite it,' \
                               'please specify overwrite=1'
                    self.logger.warning(msg)

                if not overwrite:
                    continue

            np.save(tablepath/f"{b64_encode(column)}.npy", df[column])

    def load(self, table: str, columns: List[str]=None) -> pd.DataFrame:
        df = {}
        for path in self.column_paths(table):
            column = b64_decode(path.stem)

            if columns is not None and column not in columns:
                continue

            df[column] = np.load(path)

        return pd.DataFrame(df)

    def tables(self) -> List[str]:
        return [b64_decode(str(path.relative_to(self.dirpath)))
                for path in self.dirpath.glob('*')]

    def column_paths(self, table: str) -> List[pathlib.Path]:
        tablepath = self.dirpath/b64_encode(table)
        return list(tablepath.glob('*.npy'))

    def columns(self, table: str) -> List[str]:
        return [b64_decode(path.stem) for path in self.column_paths(table)]

    def drop_columns(self, table: str, columns: List[str]):
        tablepath = self.dirpath/b64_encode(table)

        for column in columns:
            path = tablepath/f"{b64_encode(column)}.npy"

            if not path.exists():
                self.logger.warning(f'{column} column doesn\'t exist')

            path.unlink()
