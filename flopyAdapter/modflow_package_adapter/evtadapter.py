from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class EvtAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(EvtAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowEvt(
            _mf,
            **content
        )

    @staticmethod
    def default():
        return {
            "nevtop": 3,
            "ipakcb": None,
            "surf": 0.,
            "evtr": 1e-3,
            "exdp": 1.,
            "ievt": 1,
            "extension": 'evt',
            "unitnumber": None,
            "filenames": None,
            "external": True
        }

    @staticmethod
    def read_package(package):
        return {
            "nevtop": package.nevtop,
            "ipakcb": package.ipakcb,
            "surf": package.surf,
            "evtr": package.evtr,
            "exdp": package.exdp,
            "ievt": package.ievt,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames,
            "external": package.external
        }
