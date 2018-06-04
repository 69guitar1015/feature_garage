from setuptools import setup, find_packages

setup(
    name='feature_garage',
    version='0.1',
    url='https://github.com/69guitar1015/feature_garage',
    maintainer='69guitar1015',
    description='`FeatureGarage`: A fast and simple `pandas.DataFrame` r/w library for feature engineering',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    license='MIT',
)
