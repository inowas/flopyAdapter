from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class WelAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(WelAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()

        return mf.ModflowWel(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ipakcb": 0,
            "stress_period_data": None,
            "dtype": None,
            "extension": 'wel',
            "unitnumber": 20,
            "options": None
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "ipakcb": package.ipakcb,
            # stress period data values translated to list of lists to be json serializable
            "stress_period_data": {k: [list(i) for i in v] for k, v in package.stress_period_data.data.items()},
            # "dtype": package.dtype,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0],
            # options is None if options list is empty:
            "options": package.options if package.options else None
        }
        return content
