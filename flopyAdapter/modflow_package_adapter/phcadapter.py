from .adapter_base import ModflowPackageAdapterBase
import flopy.mt3d as mt


class PhcAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(PhcAdapter, self).__init__(*args)

    def get_package(self, _mt):
        content = self.merge()
        return mt.Mt3dPhc(
            _mt,
            **content
        )

    @staticmethod
    def default():
        return {
            "os": 2,
            "temp": 25,
            "asbin": 0,
            "eps_aqu": 0,
            "eps_ph": 0,
            "scr_output": 1,
            "cb_offset": 0,
            "smse": ['pH', 'pe'],
            "mine": [],
            "ie": [],
            "surf": [],
            "mobkin": [],
            "minkin": [],
            "surfkin": [],
            "imobkin": [],
            "extension": 'phc',
            "unitnumber": None
        }

    @staticmethod
    def read_package(package):
        return {
            "os": package.os,
            "temp": package.temp,
            "asbin": package.asbin,
            "eps_aqu": package.eps_aqu,
            "eps_ph": package.eps_ph,
            "scr_output": package.scr_output,
            "cb_offset": package.cb_offset,
            "smse": package.smse,
            "mine": package.mine,
            "ie": package.ie,
            "surf": package.surf,
            "mobkin": package.mobkin,
            "minkin": package.minkin,
            "surfkin": package.surfkin,
            "imobkin": package.imobkin,
            "extension": package.extension,
            "unitnumber": package.unitnumber
        }
