from .adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class PcgAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(PcgAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowPcg(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "mxiter": 50,
            "iter1": 30,
            "npcond": 1,
            "hclose": 1E-5,
            "rclose": 1E-5,
            "relax": 1.0,
            "nbpol": 0,
            "iprpcg": 0,
            "mutpcg": 3,
            "damp": 1.0,
            "dampt": 1.0,
            "ihcofadd": 0,
            "extension": 'pcg',
            "unitnumber": 27
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "mxiter": package.mxiter,
            "iter1": package.iter1,
            "npcond": package.npcond,
            "hclose": package.hclose,
            "rclose": package.rclose,
            "relax": package.relax,
            "nbpol": package.nbpol,
            "iprpcg": package.iprpcg,
            "mutpcg": package.mutpcg,
            "damp": package.damp,
            "dampt": package.dampt,
            "ihcofadd": package.ihcofadd,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
