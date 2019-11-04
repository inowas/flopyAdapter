from .adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class LmtAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(LmtAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowLmt(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "output_file_name": 'mt3d_link.ftl',
            "output_file_unit": 54,
            "output_file_header": 'extended',
            "output_file_format": 'unformatted',
            "extension": 'lmt6',
            "package_flows": [],
            "unitnumber": None,
            "filenames": None
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "output_file_name": package.output_file_name,
            "output_file_unit": package.output_file_unit,
            "output_file_header": package.output_file_header,
            "output_file_format": package.output_file_format,
            "extension": package.extension[0],
            "package_flows": package.package_flows,
            "unitnumber": package.unit_number[0],
            # "filenames": None
        }
        return content
