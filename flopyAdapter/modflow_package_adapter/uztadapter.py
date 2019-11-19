from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.mt3d as mt


class UztAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(UztAdapter, self).__init__(*args)

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dUzt(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "mxuzcon": 0,
            "icbcuz": None,
            "iet": 0,
            "iuzfbnd": None,
            "wc": 0.0,
            "sdh": 0.0,
            "cuzinf": None,
            "cuzet": None,
            "cgwet": None,
            "extension": 'uzt',
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "mxuzcon": package.mxuzcon,
            "icbcuz": package.icbcuz,
            "iet": package.iet,
            "iuzfbnd": package.iuzfbnd,
            "wc": package.wc,
            "sdh": package.sdh,
            "cuzinf": package.cuzinf,
            "cuzet": package.cuzet,
            "cgwet": package.cgwet,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames
        }
        return content
