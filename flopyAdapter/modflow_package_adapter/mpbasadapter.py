from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modpath as mp


class MpBasAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(MpBasAdapter, self).__init__(*args)

    def get_package(self, _mp):
        content = self.merge()
        return mp.ModpathBas(
            _mp,
            **content
        )

    @staticmethod
    def default():
        return {
            "hnoflo": -9999.0,
            "hdry": -8888.0,
            "def_face_ct": 0,
            "bud_label": None,
            "def_iface": None,
            "laytyp": 0,
            "ibound": 1,
            "prsity": 0.3,
            "prsityCB": 0.3,
            "extension": 'mpbas',
            "unitnumber": 86
        }

    @staticmethod
    def read_package(package):
        return {
            "hnoflo": package.hnoflo,
            "hdry": package.hdry,
            "def_face_ct": package.def_face_ct,
            "bud_label": package.bud_label,
            "def_iface": package.def_iface,
            "laytyp": package.laytyp,
            "ibound": package.ibound,
            "prsity": package.prsity,
            "prsityCB": package.prsityCB,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
        }
