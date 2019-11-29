"""This module holds a class to build and run flopy models based on the given modflowdatamodel.

Author: Ralf Junghanns / Benjamin Gutzmann
EMail: ralf.junghanns@gmail.com

"""


from flopyAdapter.datamodel.modflowdatamodel import ModflowDataModel
from flopyAdapter.mapping.flopy_package_to_adapter_mapping import FLOPY_PACKAGE_TO_ADAPTER_MAPPER
from flopyAdapter.flopy_adapter.flopy_calculationadapter import FlopyCalculationAdapter
from flopyAdapter.flopy_adapter.statistics.hobstatistics import HobStatistics


class FlopyModelManager:
    """

    """

    def __init__(self,
                 modflowdatamodel: ModflowDataModel,
                 version: str = None,
                 uuid: str = None):

        self._modflowdatamodel = modflowdatamodel

        self._regular_order = ["mf", "mt", "mp"]
        self._flopy_packageorder = ["swt", *self._regular_order]

        self._version = version
        self._uuid = uuid

        self._flopy_packages = {}
        self._flopy_packages_success = {}

        # self._report = ''

        self.package_orders = {
            "mf": [
                'mf', 'dis', 'bas', 'bas6',
                'chd', 'evt', 'drn', 'ghb', 'hob', 'rch', 'riv', 'wel',
                'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6'
            ],
            "mt": [
                "mt", "btn", "adv", "dsp", "gcg", "ssm", "lkt",
                "phc", "rct", "sft", "tob", "uzt"
            ],
            "swt": [  # Modflow
                'swt', 'dis', 'bas', 'bas6', 'riv', 'wel', 'rch', 'chd', 'ghb', 'hob',
                'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6',
                # Mt3D
                'btn', 'adv', 'dsp', 'gcg', 'ssm', 'lkt', 'phc', 'rct', 'sft', 'tob', 'uzt',
                # Seawat
                'vdf', 'vsc'
            ],
            "mp": [
                'mp', 'bas', 'sim'
            ]
        }

    @staticmethod
    def from_modflowdatamodel(model: ModflowDataModel):
        if not isinstance(model, ModflowDataModel):
            raise TypeError("Error: model is not a ModflowDataModel.")

        return FlopyModelManager(model)
    #
    # @staticmethod
    # def from_hash(hash: str,
    #               model_ws: str = "./"):
    #     if not isinstance(hash, str):
    #         raise TypeError("Error: hash is not a string.")

    @property
    def flopy_packages(self):
        return self._flopy_packages

    def build_flopymodel(self):
        """Builds the flopy models based on what's found in the model data. The existing packages also
        have impact on which flopy models are created (either only swt or a followup of mf, mt, mp)

        Args:
            self - the class holds the modflow model data which powers the different flopy models

        Returns:
            None - the models are written to a class attribute setup as a dictionary with the name and
            the corresponding flopy model class

        """

        if "swt" in self._modflowdatamodel.data:  # if data has "swt"
            package_data = {
                **self._modflowdatamodel.data["mf"],
                **self._modflowdatamodel.data["mt"],
                **self._modflowdatamodel.data["swt"],
                'packages': [*self._modflowdatamodel.data["mf"]['packages'],
                             *self._modflowdatamodel.data["mt"]['packages'],
                             *self._modflowdatamodel.data["swt"]['packages']]
            }

            package_content = self.read_packages(package_data)

            self._flopy_packages["swt"] = self.create_flopy_package(self.package_orders["swt"], package_content)

        else:
            for model in self._regular_order:
                if model in self._modflowdatamodel.data:
                    # Basic data model is needed by both mt and mp
                    package_content = self.read_packages(self._modflowdatamodel.data[model])

                    self._flopy_packages[model] = self.create_flopy_package(self.package_orders[model], package_content)

    @staticmethod
    def read_packages(data: dict):
        package_content = {}
        for package in data['packages']:
            print(f'Read Flopy package data: {package}')
            package_content[package.lower()] = data[package]
        return package_content

    def create_flopy_package(self,
                             package_order: dict,
                             package_content: dict):
        model = None
        for package in package_order:
            if package in ['mf', 'mt', 'mp', 'swt']:
                print(f'Create Flopy Model: {package}')
                if package == "mf":
                    # In opposition to the other main packages mf is the basis for all and needs no basemodel
                    model = self.create_package(package, package_content[package])
                else:
                    # Others need mf as main package
                    assert self._flopy_packages["mf"], \
                         "Modflow model isn't yet build but needed for package {package}."
                    model = self.create_package(package, package_content[package], self._flopy_packages["mf"])
            elif package in package_content:
                print(f'Create Flopy Package: {package}')
                # Subpackages are based on their relative main package
                self.create_package(package, package_content[package], model)

        return model

    @staticmethod
    def create_package(name: str,
                       content: dict,
                       *model):
        # Modflow packages
        adapter = FLOPY_PACKAGE_TO_ADAPTER_MAPPER[name]

        package = adapter(content).get_package(*model)

        return package

    # @staticmethod
    # def write_input_model(model):
    #     print('Write input files.')
    #     model.write_input()

    def run_model(self):
        for package_type, package in self._flopy_packages.items():
            calculation_adapter = FlopyCalculationAdapter(package)  # includes check

            calculation_adapter.write_input_model()

            calculation_adapter.run_calculation()

            if package_type in ["swt", "mf"] and 'hob' in self._modflowdatamodel.data["mf"]['packages']:
                print(f'Calculate hob-statistics and write to file {self._uuid}.hob.stat')
                self.run_hob_statistics(package)

            calculation_success, calculation_report = calculation_adapter.get_success_and_report()

            self._flopy_packages_success[package_type] = calculation_success

    @staticmethod
    def run_hob_statistics(model):
        print(f'Calculate hob-statistics for data model {model.name}')
        HobStatistics(model.model_ws, model.name).write_to_file()
