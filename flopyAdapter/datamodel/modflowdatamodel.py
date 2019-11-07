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
        self._data = data

    @staticmethod
    def from_data(data, schema, resolver):
        ModflowDataModel.validate(data, schema, resolver)

        return ModflowDataModel(data)

    @staticmethod
    def validate(data, schema, resolver):
        Draft7Validator(schema=schema, resolver=resolver).validate(data)

    @property
    def data(self):
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
            return self.data[mf_module]
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

        ordered_model_data = sort_dictionary(self.data, recursive=True)

        return md5(json.dumps(ordered_model_data).econde("utf-8")).hexdigest()

    # Attributes accessor
    @property
    def nlay(self):
        return self.get_package("mf", "dis")["nlay"]

    @property
    def nrow(self):
        return self.get_package("mf", "dis")["nrow"]

    @property
    def ncol(self):
        return self.get_package("mf", "dis")["ncol"]

    @property
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

        for obj in objects:
            assert obj["type"] in ["wel"], f"Error: object has unknown type {obj['type']}"

            if obj["type"] == "wel":
                lay = obj["position"]["lay"]["result"]
                row = obj["position"]["row"]["result"]
                col = obj["position"]["col"]["result"]
                pumping_rates = [obj["flux"][flux_period]["result"] for flux_period in obj["flux"]]

                self.add_well(lay=lay, row=row, col=col, pumping_rates=pumping_rates)

    def add_well(self, lay, row, col, pumping_rates):
        bound_error_message = f"Error: {0} {1} out of bounds which are [0, {2}] for nlay {3}"
        if lay not in range(self.nlay):
            raise ValueError(bound_error_message.format("layer", lay, self.nlay - 1, self.nlay))
        if row not in range(self.nrow):
            raise ValueError(bound_error_message.format("row", row, self.nrow - 1, self.nrow))
        if col not in range(self.ncol):
            raise ValueError(bound_error_message.format("layer", lay, self.nlay - 1, self.nlay))
        if len(pumping_rates) != self.nper:
            raise ValueError(f"Error: number of pumping rates is {len(pumping_rates)} not equal to nper={self.nper}")

        if "wel" not in self.data["mf"]:
            self.data["mf"]["packages"].extend("wel")
            self.data["mf"]["wel"] = FLOPY_PACKAGE_TO_ADAPTER_MAPPER["wel"].default()

        if not self.data["mf"]["wel"]["stress_period_data"]:
            self.data["mf"]["wel"]["stress_period_data"] = {}

        for period, flux in enumerate(pumping_rates):
            period_flux = [lay, row, col, flux]

            if str(period) not in self.data["mf"]["wel"]["stress_period_data"]:
                self.data["mf"]["wel"]["stress_period_data"][str(period)] = []

            same_position_flux = [existing_flux
                                  for existing_flux in self.data["mf"]["wel"]["stress_period_data"][str(period)]
                                  if existing_flux[:3] == period_flux[:3]]

            if same_position_flux:
                same_position_flux[0][3] += period_flux[3]
                continue

            self.data["mf"]["wel"]["stress_period_data"][period].append(period_flux)

