from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import numpy as np
import flopy.mt3d as mt


class DspAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(DspAdapter, self).__init__(*args)

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dDsp(
            _mt,
            **content
        )

    @staticmethod
    def default():
        default = {
            "al": 0.01,
            "trpt": 0.1,
            "trpv": 0.01,
            "dmcoef": 1e-09,
            "extension": 'dsp',
            "multiDiff": False,
            "unitnumber": None,
            "filenames": None
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "al": package.al.array.tolist(),
            "trpt": np.reshape(package.trpt.array, (len(package.trpt.array),)).tolist(),
            "trpv": np.reshape(package.trpv.array, (len(package.trpv.array),)).tolist(),
            # "dmcoef": package.dmcoef.array.tolist(),
            "extension": package.extension[0],
            "multiDiff": package.multiDiff,
            "unitnumber": package.unit_number[0],
            # "filenames": package.filenames
        }
        return content
