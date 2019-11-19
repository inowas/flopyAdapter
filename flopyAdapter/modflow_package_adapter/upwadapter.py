from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class UpwAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(UpwAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowUpw(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "laytyp": 0,
            "layavg": 0,
            "chani": 1.0,
            "layvka": 0,
            "laywet": 0,
            "ipakcb": 53,
            "hdry": -1e+30,
            "iphdry": 0,
            "hk": 1.0,
            "hani": 1.0,
            "vka": 1.0,
            "ss": 1e-5,
            "sy": 0.15,
            "vkcb": 0.0,
            "extension": 'upw',
            "unitnumber": 31
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "laytyp": package.laytyp.array.tolist(),
            "layavg": package.layavg.array.tolist(),
            "chani": package.chani.array.tolist(),
            "layvka": package.layvka.array.tolist(),
            "laywet": package.laywet.array.tolist(),
            "ipakcb": package.ipakcb,
            "hdry": package.hdry,
            "iphdry": package.iphdry,
            "hk": package.hk.array.tolist(),
            "hani": package.hani.array.tolist(),
            "vka": package.vka.array.tolist(),
            "ss": package.ss.array.tolist(),
            "sy": package.sy.array.tolist(),
            "vkcb": package.vkcb.array.tolist(),
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
