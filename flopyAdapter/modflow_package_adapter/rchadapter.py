from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class RchAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(RchAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowRch(
            _mf,
            **content
        )

    @staticmethod
    def default():
        return {
            "nrchop": 3,
            "ipakcb": 0,
            "rech": 0,
            "irch": 0,
            "extension": 'rch',
            "unitnumber": 19
        }

    @staticmethod
    def read_package(package):
        return {
            "nrchop": package.nrchop,
            "ipakcb": package.ipakcb,
            "rech": package.rech,
            "irch": package.irch,
            "extension": package.extension,
            "unitnumber": package.unitnumber
        }
