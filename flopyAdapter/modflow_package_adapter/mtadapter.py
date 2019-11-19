from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.mt3d as mt


class MtAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(MtAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()

        return mt.Mt3dms(modflowmodel=_mf, **content)

    @staticmethod
    def default():
        default = {
            "modelname": 'mt3dtest',
            "namefile_ext": 'nam',
            "ftlfilename": 'mt3d_link.ftl',
            "ftlfree": False,
            "version": 'mt3dms',
            "exe_name": 'mt3dms.exe',
            "structured": True,
            "listunit": None,
            "ftlunit": None,
            "model_ws": '.',
            "external_path": None,
            "verbose": False,
            "load": True,
            "silent": 0
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            "modelname": package.namefile.split('.')[0],
            "namefile_ext": package.namefile_ext,
            "ftlfilename": package.ftlfilename,
            "ftlfree": package.ftlfree,
            "version": package.version,
            "exe_name": package.exe_name,  # None
            "structured": package.structured,
            "listunit": package.listunit,  # None
            "ftlunit": package.ftlunit,
            "model_ws": package.model_ws,
            "external_path": package.external_path,  # None
            "verbose": package.verbose,
            "load": package.load,
            "silent": package.silent
        }
        return content
