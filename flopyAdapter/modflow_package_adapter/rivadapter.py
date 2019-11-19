from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class RivAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(RivAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowRiv(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ipakcb": 0,
            "stress_period_data": None,
            "dtype": None,
            "extension": "riv",
            "unitnumber": 18,
            "options": None
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "ipakcb": package.ipakcb,
            "stress_period_data": package.stress_period_data,
            "dtype": package.dtype,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "options": package.options
        }
        return content
