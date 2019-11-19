from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.seawat as seawat


class VscAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(VscAdapter, self).__init__(*args)

    def get_package(self, _swt):
        content = self.merge()
        return seawat.SeawatVsc(
            _swt,
            **content
        )

    @staticmethod
    def default():
        return {
            "mt3dmuflg": -1,
            "viscmin": 0.0,
            "viscmax": 0.0,
            "viscref": 0.0008904,
            "nsmueos": 0,
            "mutempopt": 2,
            "mtmuspec": 1,
            "dmudc": 1.923e-06,
            "cmuref": 0.0,
            "mtmutempspec": 1,
            "amucoeff": None,
            "invisc": -1,
            "visc": -1,
            "extension": 'vsc',
            "unitnumber": None
        }

    @staticmethod
    def read_package(package):
        return {
            "mt3dmuflg": package.mt3dmuflg,
            "viscmin": package.viscmin,
            "viscmax": package.viscmax,
            "viscref": package.viscref,
            "nsmueos": package.nsmueos,
            "mutempopt": package.mutempopt,
            "mtmuspec": package.mtmuspec,
            "dmudc": package.dmudc,
            "cmuref": package.cmuref,
            "mtmutempspec": package.mtmutempspec,
            "amucoeff": package.amucoeff,
            "invisc": package.invisc,
            "visc": package.visc,
            "extension": package.extension,
            "unitnumber": package.unitnumber,
            "filenames": package.filenames
        }
