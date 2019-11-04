from setuptools import setup, find_packages

try:
    import flopy
    __version__ = flopy.version.__version__
except ImportError:
    __version__ = None

if not __version__:
    __version__ = '3.2.12'

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='flopyAdapter',
    version=__version__,
    description='A module that serves the inowas flopy adapters and a flopy datamodel class',
    license='MIT',
    long_description=long_description,
    author='Benjamin Gutzmann',
    author_email='gutzemann@gmail.com',
    packages=find_packages(),
    install_requires=[f'flopy>={__version__}', 'numpy==1.17.2']
)