from .adapter_base import ModflowPackageAdapterBase
import flopy.mt3d as mt


class LktAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(LktAdapter, self).__init__(*args)

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dLkt(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "nlkinit": 0,
            "mxlkbc": 0,
            "icbclk": None,
            "ietlak": 0,
            "coldlak": 0.0,
            "lk_stress_period_data": None,
            "dtype": None,
            "extension": 'lkt',
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "nlkinit": package.nlkinit,
            "mxlkbc": package.mxlkbc,
            "icbclk": package.icbclk,
            "ietlak": package.ietlak,
            "coldlak": package.coldlak,
            "lk_stress_period_data": package.lk_stress_period_data,
            "dtype": package.dtype,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames
        }
        return content
