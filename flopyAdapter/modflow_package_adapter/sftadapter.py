from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.mt3d as mt


class SftAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(SftAdapter, self).__init__(*args)

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dSft(
                _mt,
                **content
            )

    @staticmethod
    def default():
        default = {
            "nsfinit": 0,
            "mxsfbc": 0,
            "icbcsf": 0, 
            "ioutobs": None,
            "ietsfr": 0,
            "isfsolv": 1,
            "wimp": 0.5,
            "wups": 1.0,
            "cclosesf": 1e-06,
            "mxitersf": 10,
            "crntsf": 1.0,
            "iprtxmd": 0,
            "coldsf": 0.0,
            "dispsf": 0.0,
            "nobssf": 0,
            "obs_sf": None,
            "sf_stress_period_data": None,
            "unitnumber": None,
            "filenames": None,
            "dtype": None,
            "extension": 'sft'
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "nsfinit": package.nsfinit,
            "mxsfbc": package.mxsfbc,
            "icbcsf": package.icbcsf, 
            "ioutobs": package.ioutobs,
            "ietsfr": package.ietsfr,
            "isfsolv": package.isfsolv,
            "wimp": package.wimp,
            "wups": package.wups,
            "cclosesf": package.cclosesf,
            "mxitersf": package.mxitersf,
            "crntsf": package.crntsf,
            "iprtxmd": package.iprtxmd,
            "coldsf": package.coldsf,
            "dispsf": package.dispsf,
            "nobssf": package.nobssf,
            "obs_sf": package.obs_sf,
            "sf_stress_period_data": package.sf_stress_period_data,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames,
            "dtype": package.dtype,
            "extension": package.extension
        }
        return content
