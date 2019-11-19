from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class GhbAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(GhbAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowGhb(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ipakcb": 0,
            "stress_period_data": None,
            "dtype": None,
            "no_print": False,
            "options": None,
            "extension": 'ghb',
            "unitnumber": 23
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "ipakcb": package.ipakcb,
            "stress_period_data": package.stress_period_data,
            "dtype": package.dtype,
            "no_print": package.no_print,
            "options": package.options,
            "extension": package.extension,
            "unitnumber": package.unitnumber
        }
        return content
