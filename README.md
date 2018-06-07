# FeatureGarage
`FeatureGarage`: A fast and simple `pandas.DataFrame` r/w library for feature engineering

## Installation
```
pip install -U git+https://github.com/69guitar1015/feature_garage
```

## Basic Usage
```python
from feature_garage import Garage
import pandas as pd

garage = Garage(dirpath='path/to/datadir')

df1 = pd.read_csv('path/to/csv')

# Get table list
print(garage.tables())

# Get feature list in a table
print(garage.columns(table='table'))

# Save all columns
garage.save(df1, table='df1')
# Save only specified columns
garage.save(df1, table='df1', columns=['f1', 'f2'])
# Overwrite existing columns
garage.save(df1, table='df1', overwrite=True)
# Make warning silent
garage.save(df1, table='df1', verbose=0)

# Load
df2 = garage.load(table='df2')
```

## How to save
`FeatureGarage` is just saving each column as array in npy format.
`table` is just a directory and `column`(`feature`) is just a npy file.

**categorical features may be saved as 'object'**

## Future Work
- Prallel r/w
- seemless loading for categorical features
