"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format. It creates

Author: Ralf Junghanns / Benjamin Gutzmann
EMail: ralf.junghanns@gmail.com
"""

from pathlib import PurePosixPath
import json
from jsonschema import Draft7Validator, RefResolver
from urllib.request import urlopen
from hashlib import md5

from flopyAdapter.mapping.flopy_package_to_adapter_mapping import FLOPY_PACKAGE_TO_ADAPTER_MAPPER
from flopyAdapter.flopy_adapter.flopy_calculationadapter import FlopyCalculationAdapter
from flopyAdapter.flopy_adapter.flopy_fitnessadapter import FlopyFitnessAdapter
from flopyAdapter.flopy_adapter.statistics.hobstatistics import HobStatistics

# SCHEMA_SERVER_URL = 'https://schema.inowas.com'
HTTPS_STRING = "https://"
SCHEMA_MODFLOW_MODEL_DATA = PurePosixPath("schema.inowas.com/modflow/packages/modflow_model_data.json")

with urlopen(f"{HTTPS_STRING}{SCHEMA_MODFLOW_MODEL_DATA}") as f:
    modflow_model_data_schema = json.load(f)

path_resolver = RefResolver(f"{HTTPS_STRING}{SCHEMA_MODFLOW_MODEL_DATA.parent}",
                            referrer=modflow_model_data_schema)


def sort_dictionary(dictionary: dict,
                    recursive: bool):
    """ Function to (recursively) sort dictionaries used for package data. This procedure is used to ensure
    that every time models produce the same hash independent if the order of the keys in the dictionaries.

    """
    assert isinstance(dictionary, dict), "Error: input is not of type dict"

    if recursive:
        for key, value in dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = sort_dictionary(value, recursive)

    return dict(sorted(dictionary.items(), key=lambda kv: (kv[0], kv[1])))


class ModflowDataModel:
    """The ModflowDataModel class is used to represent a layer between the optimization request and the
    modflow model data (dictionary)
    and the flopy models which are build on top of this data. It offers a function to add objects to the
    the model, which is important as we store objects separate from the original model as they are part
    of the optimization process and thus change often.  Furthermore the class offers methods to build
    flopy model objects ready to run for the calculation adapter and finally methods to read the fitness
    after a model run.

    Args:
        data () - modflow model data that holds the package information needed to build flopy models

    """

    def __init__(self,
                 # uuid: str,
                 # version: str,
                 data: dict):
        self.validate(data)

        self._data = data

    @staticmethod
    def validate(data):
        Draft7Validator(schema=modflow_model_data_schema, resolver=path_resolver).validate(data)

    def get_data(self):
        """ Function to return modflow model data

        :return:
        """
        return self._data

    def get_module(self, mf_module):
        """ Function to return one module from the modflow model data

        :param mf_module:
        :return:
        """
        assert mf_module in ["mf", "mt", "mp"], \
            f"Error: requested module {mf_module} is not one of 'mf', 'mt', 'mp'."

        try:
            return self.get_data()[mf_module]
        except KeyError:
            raise KeyError(f"Error: module {mf_module} is not available in modflow model data.")

    def get_package(self, mf_module, name):
        """ Function to return a specific package of a chosen modflow model module.

        """
        module_data = self.get_module(mf_module)

        try:
            return module_data[name]
        except KeyError:
            raise KeyError(f'Error: package {name} not found in module {mf_module}.')

    def create_hash(self) -> str:
        """ Function to create a md5-hash of the model data. We expect the general model to be

        Args:
            self._data (dict) - holds the modflow model data

        Returns:
            md5-hash - a string to identify a unique modflow model

        """

        ordered_model_data = sort_dictionary(self.get_data(), recursive=True)

        return md5(json.dumps(ordered_model_data).econde("utf-8")).hexdigest()

    # Attributes accessor
    def nlay(self):
        return self.get_package("mf", "dis")["nlay"]

    def nrow(self):
        return self.get_package("mf", "dis")["nrow"]

    def ncol(self):
        return self.get_package("mf", "dis")["ncol"]

    def nper(self):
        return self.get_package("mf", "dis")["nper"]

    def add_objects(self,
                    objects: list) -> None:
        """ Merges well objects into a modflow model, adding stress periods on existing ones or
        creating new ones for those which do not match in location

        Args:
            self - the model class holding the model data as dictionary
            objects (list) - a list of dictionaries, which each describe an object (well) with all
            its information and especially the stress periods

        Returns:
            None - merges objects into the existing model data of the class

        """

        # Set mf data path
        # mf_data = self.flopy_models_data["mf"]

        for obj in objects:

            if obj["type"] == "wel":
                lay = obj["position"]["lay"]["result"]
                row = obj["position"]["row"]["result"]
                col = obj["position"]["col"]["result"]
                pumping_rates = [obj["flux"][flux_period]["result"] for flux_period in obj["flux"]]

                self.add_well(lay=lay, row=row, col=col, pumping_rates=pumping_rates)
            else:
                raise ValueError(f"Error: object has unknown type {obj['type']}")

    def add_well(self, lay, row, col, pumping_rates):
        raise NotImplementedError
        # if obj_type not in mf_data:
        #     mf_data[obj_type] = FLOPY_PACKAGE_TO_ADAPTER_MAPPER[obj_type].default()
        #
        # if obj_type == "wel":
        #
        #     if not mf_data[obj_type]["stress_period_data"]:
        #         mf_data[obj_type]["stress_period_data"] = {}
        #
        #     for period, obj_flux in obj["flux"].items():
        #         period_flux = [obj_position["lay"]["result"],
        #                        obj_position["row"]["result"],
        #                        obj_position["col"]["result"],
        #                        obj_flux["result"]]
        #
        #         if period not in mf_data[obj_type]["stress_period_data"]:
        #             mf_data[obj_type]["stress_period_data"][period] = []
        #
        #         same_position_flux = [existing_flux
        #                               for existing_flux in mf_data[obj_type]["stress_period_data"][period]
        #                               if existing_flux[:3] == period_flux[:3]]
        #
        #         if same_position_flux:
        #             same_position_flux[0][3] += period_flux[3]
        #             continue
        #
        #         mf_data[obj_type]["stress_period_data"][period].append(period_flux)
        pass
