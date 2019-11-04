"""init tries to get the flopy version of the environment it is installed into"""
try:
    import flopy
    __version__ = flopy.version.__version__
except ImportError:
    __version__ = None

from flopyAdapter.datamodel.flopydatamodel import FlopyDataModel
