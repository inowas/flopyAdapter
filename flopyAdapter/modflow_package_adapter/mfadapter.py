from flopyAdapter.modflow_package_adapter.adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class MfAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(MfAdapter, self).__init__(*args)

    def get_package(self):
        content = self.merge()
        return mf.Modflow(
            **content
        )

    @staticmethod
    def default():
        default = {
            "modelname": "modflowtest",
            "namefile_ext": 'nam',
            "version": "mf2005",
            "exe_name": "mf2005.exe",
            "structured": True,
            "listunit": 2,
            "model_ws": '.',
            "external_path": None,
            "verbose": False
        }
        return default

    @staticmethod
    def read_package(package):
        content = {
            # "modelname": package.modelname,#None
            "namefile_ext": package.namefile_ext,
            "version": package.version,
            "exe_name": package.exe_name,
            "structured": package.structured,
            # "listunit": package.listunit,
            "model_ws": package.model_ws,
            "external_path": package.external_path,
            "verbose": package.verbose
        }
        return content
