from .adapter_base import ModflowPackageAdapterBase
import flopy.modflow as mf


class HobAdapter(ModflowPackageAdapterBase):
    def __init__(self, *args):
        super(HobAdapter, self).__init__(*args)

    def get_package(self, _mf):
        content = self.merge()
        # noinspection PyTypeChecker
        content["obs_data"] = self.map_obs_data(_mf, content["obs_data"])
        return mf.ModflowHob(
            _mf,
            **content
        )

    @staticmethod
    def map_obs_data(model, observations):
        obs = []

        for o in observations:
            print(o)
            obs.append(mf.HeadObservation(
                model,
                layer=o['layer'],
                row=o['row'],
                column=o['column'],
                time_series_data=o['time_series_data']
            ))

        return obs

    @staticmethod
    def default():
        return {
            "iuhobsv": 1051,
            "hobdry": 0,
            "tomulth": 1.0,
            "obs_data": None,
            "hobname": None,
            "extension": 'hob',
            "unitnumber": None,
            "filenames": None
        }

    @staticmethod
    def read_package(package):
        content = {
            "iuhobsv": package.iuhobsv,
            "hobdry": package.hobdry,
            "tomulth": package.tomulth,
            "obs_data": package.obs_data,
            "hobname": package.hobname,
            "extension": package.extension[0],
            "unitnumber": package.unit_number[0],
            "filenames": package.filenames
        }
        return content
