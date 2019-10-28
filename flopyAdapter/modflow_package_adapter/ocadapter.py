from .adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class OcAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(OcAdapter, self).__init__(*args)

    # Override
    @staticmethod
    def to_dict(data):
        if not data or type(data) is not list:
            return data

        stress_period_data = {}
        for stress_period in data:
            sp = stress_period[0][0]
            ts = stress_period[0][1]
            oc_data = stress_period[1]
            stress_period_data[(sp, ts)] = oc_data

        return stress_period_data

    def get_package(self, _mf):
        content = self.merge()
        return mf.ModflowOc(
            _mf,
            **content
        )

    @staticmethod
    def default():
        default = {
            "ihedfm": 0,
            "iddnfm": 0,
            "chedfm": None,
            "cddnfm": None,
            "cboufm": None,
            "compact": True,
            "stress_period_data": None,
            "extension": ['oc', 'hds', 'ddn', 'cbc'],
            "unitnumber": [14, 51, 52, 53]
        }

        return default

    @staticmethod
    def read_package(package):
        content = {
            "ihedfm": package.ihedfm,
            "iddnfm": package.iddnfm,
            "chedfm": package.chedfm,
            "cddnfm": package.cddnfm,  # None
            "cboufm": package.cboufm,  # None
            "compact": package.compact,
            # stress period data dict keys transformed from tuple to string to be json serializable
            "stress_period_data": {str(k): v for k, v in package.stress_period_data.items()},
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0]
        }
        return content
