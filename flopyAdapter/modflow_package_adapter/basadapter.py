from .adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class BasAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(BasAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowBas(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ibound": 1,
            "strt": 1.0,
            "ifrefm": True,
            "ixsec": False,
            "ichflg": False,
            "stoper": None,
            "hnoflo": -999.99,
            "extension": 'bas',
            "unitnumber": 13
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "ibound": package.ibound.array.tolist(),
            "strt": package.strt.array.tolist(),
            "ifrefm": package.ifrefm,
            "ixsec": package.ixsec,
            "ichflg": package.ichflg,
            "stoper": package.stoper,
            "hnoflo": package.hnoflo,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
