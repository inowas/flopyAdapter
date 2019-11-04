from .adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class ChdAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(ChdAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowChd(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "stress_period_data": None,
            "dtype": None,
            "extension": 'chd',
            "unitnumber": 24
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            # stress period data values translated to list of lists to be json serializable
            "stress_period_data": {k: [list(i) for i in v] for k, v in package.stress_period_data.data.items()},
            # "dtype": package.dtype,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
