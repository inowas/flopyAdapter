"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format. It creates

Author: Ralf Junghanns / Benjamin Gutzmann
EMail: ralf.junghanns@gmail.com
"""

from typing import Optional, List, Union
from pathlib import Path
import json
from jsonschema import Draft7Validator, RefResolver, ValidationError, RefResolutionError
from hashlib import md5

from flopyAdapter.mapping.flopy_package_to_adapter_mapping import FLOPY_PACKAGE_TO_ADAPTER_MAPPER


SUPPORTED_OBJECTTYPES_FOR_ADDING = ["wel"]


def sort_dictionary(dictionary: dict,
                    recursive: bool):
    """ Function to (recursively) sort dictionaries used for package data. This procedure is used to ensure
    that models always produce the same hash independent of the order of the keys in the dictionaries.
    Sorting is done by the Python internal sorting methods depending on the data. This means sorting only
    works for keys with same type and otherwise will throw a TypeError.

    """
    if not isinstance(dictionary, dict):
        raise TypeError("input is not of type dict")
    if not isinstance(recursive, bool):
        raise TypeError("recursive is not of type bool")

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
                 data: dict):
        self._data = data

    @staticmethod
    def from_data(data: dict,
                  schema: dict,
                  resolver: Optional[RefResolver] = None):
        """ Function to instantiate the model with data that is first validated before the model
        is created with the data itself

        Args:
            data (dict) - the model data consisting of modflow packages in flopy shape
            schema (dict) - the schema that the data is tested against. Using a function argument
            ensures that the schema is always up to date as it first has to be downloaded
            resolver (RefResolver) - the resolver for subschemata as defined in the file itself

        Returns:

        """
        if not isinstance(data, dict):
            raise TypeError("data is not a json/dictionary.")
        if not isinstance(schema, dict):
            raise TypeError("schema is not a json/dictionary.")

        ModflowDataModel.validate(data, schema, resolver)

        return ModflowDataModel(data)

    @staticmethod
    def validate(data, schema, resolver):
        """ Function to validate model data before instantiating

        Args:
            same as in from_data

        Returns:
            None - if data is valid, otherwise certain errors are thrown

        """
        try:
            # if valid returns None
            return Draft7Validator(schema=schema, resolver=resolver).validate(data)
        except ValidationError:
            raise ValidationError("data couldn't be validated.")
        except RefResolutionError:
            raise RefResolutionError("schema references couldn't be solved.")

    @property
    def data(self):
        """ Function to return modflow model data

        :return:
        """
        return self._data

    @property
    def model_ws(self):
        return self._data["mf"]["mf"]["model_ws"]

    @model_ws.setter
    def model_ws(self,
                 new_model_ws: Optional[Union[str, Path]] = None):
        """ Setter for model_ws which has to be used in order to set the correct working folder before the model is
        built and executed

        :param new_model_ws:
        :return:
        """
        if not isinstance(new_model_ws, (str, Path)):
            raise TypeError("model_ws is not a str/Path")

        for package in ["mf", "mt", "swt", "mp"]:
            try:
                # Set model_ws in packages to defined folder
                self._data[package][package]["model_ws"] = new_model_ws
            except KeyError:
                pass

    def get_module(self, mf_module):
        """ Function to return one module from the modflow model data

        :param mf_module:
        :return:
        """
        assert mf_module in ["mf", "mt", "mp"], \
            f"requested module {mf_module} is not one of 'mf', 'mt', 'mp'."

        try:
            return self.data[mf_module]
        except KeyError:
            raise KeyError(f"module {mf_module} is not available in modflow model data.")

    def get_package(self, mf_module, name):
        """ Function to return a specific package of a chosen modflow model module.

        """
        module_data = self.get_module(mf_module)

        try:
            return module_data[name]
        except KeyError:
            raise KeyError(f'package {name} not found in module {mf_module}.')

    @property
    def md5_hash(self) -> str:
        """ Function to create a md5-hash of the model data. We expect the general model to be

        Args:
            self._data (dict) - holds the modflow model data

        Returns:
            md5-hash - a string to identify a unique modflow model

        """

        ordered_model_data = sort_dictionary(self.data, recursive=True)

        return md5(json.dumps(ordered_model_data).encode("utf-8")).hexdigest()

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
            if obj["type"] not in SUPPORTED_OBJECTTYPES_FOR_ADDING:
                raise ValueError(f"object has unknown type {obj['type']}."
                                 f"Currently only 'wel' is supported.")

            if obj["type"] == "wel":
                lay = obj["position"]["lay"]["result"]
                row = obj["position"]["row"]["result"]
                col = obj["position"]["col"]["result"]
                pumping_rates = [obj["flux"][flux_period]["result"] for flux_period in obj["flux"]]

                self.add_well(lay=lay, row=row, col=col, pumping_rates=pumping_rates)

    def add_well(self,
                 lay: int,
                 row: int,
                 col: int,
                 pumping_rates: List[Union[int, float]]):
        if not isinstance(lay, int) or not isinstance(row, int) or not isinstance(col, int):
            raise TypeError(f"type of lay {type(lay)}, type of row {type(row)},"
                            f"type of col {type(col)}, expected int for all.")
        if not isinstance(pumping_rates, list):
            raise TypeError(f"pumping rates are of type {type(pumping_rates)}, should be list.")
        if not all([isinstance(rate, (int, float)) for rate in pumping_rates]):
            raise TypeError("pumping rates should all be of type int/float")

        if lay not in range(self.nlay) or row not in range(self.nrow) or col not in range(self.ncol):
            raise ValueError(f"bounds lay: {lay}, row: {row}, col: {col} are incorrect."
                             f"Model is limited to {self.nlay} layers, {self.nrow} rows and {self.ncol} cols.")
        if len(pumping_rates) != self.nper:
            raise ValueError(f"number of p-rates={len(pumping_rates)} not equal to "
                             f"nper={self.nper}")

        self.data["mf"]["wel"] = FLOPY_PACKAGE_TO_ADAPTER_MAPPER["wel"](self.data["mf"].get("wel", {})).merge()

        self.data["mf"]["wel"]["stress_period_data"] = self.data["mf"]["wel"].get("stress_period_data", {})

        for period, flux in enumerate(pumping_rates):
            period_flux = [lay, row, col, flux]

            try:
                existing_fluxes = self.data["mf"]["wel"]["stress_period_data"][str(period)]
            except KeyError:
                existing_fluxes = []
                self.data["mf"]["wel"]["stress_period_data"][str(period)] = existing_fluxes

            try:
                same_position_flux = [existing_flux
                                      for existing_flux in existing_fluxes
                                      if existing_flux[:3] == period_flux[:3]]
                same_position_flux[0][3] += period_flux[3]
            except IndexError:
                self.data["mf"]["wel"]["stress_period_data"][str(period)].append(period_flux)
