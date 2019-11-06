"""This module holds a class to build and run flopy models based on the given modflowdatamodel.

Author: Ralf Junghanns / Benjamin Gutzmann
EMail: ralf.junghanns@gmail.com

"""


class FlopyModel:
    _regular_order = ["mf", "mt", "mp"]
    _flopy_model_order = ["swt", *_regular_order]

    _version = None
    _uuid = None

    _flopy_models = {}
    _flopy_models_success = {}

    _report = ''

    package_orders = {
        "mf": ['mf', 'dis', 'bas', 'bas6',
               'chd', 'evt', 'drn', 'ghb', 'hob', 'rch', 'riv', 'wel',
               'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6'],
        "mt":  ['mf', 'dis', 'bas', 'bas6',
                'chd', 'evt', 'drn', 'ghb', 'hob', 'rch', 'riv', 'wel',
                'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6'],
        "swt": [# Modflow
                'swt', 'dis', 'bas', 'bas6', 'riv', 'wel', 'rch', 'chd', 'ghb', 'hob',
                'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6',
                # Mt3D
                'btn', 'adv', 'dsp', 'gcg', 'ssm', 'lkt', 'phc', 'rct', 'sft', 'tob', 'uzt',
                # Seawat
                'vdf', 'vsc'],
        "mp": ['mp', 'bas', 'sim']
    }

    def __init__(self):
        pass

    def build_flopy_models(self):
        """Builds the flopy models based on what's found in the model data. The existing packages also
        have impact on which flopy models are created (either only swt or a followup of mf, mt, mp)

        Args:
            self - the class holds the modflow model data which powers the different flopy models

        Returns:
            None - the models are written to a class attribute setup as a dictionary with the name and
            the corresponding flopy model class

        """

        if self.flopy_models_data["swt"]:
            package_data = {
                **self.flopy_models_data["mf"],
                **self.flopy_models_data["mt"],
                **self.flopy_models_data["swt"],
                'packages': [*self.flopy_models_data["mf"]['packages'],
                             *self.flopy_models_data["mt"]['packages'],
                             *self.flopy_models_data["swt"]['packages']]
            }

            package_content = self.read_packages(package_data)

            self._flopy_models["swt"] = self.create_model(self.package_orders["swt"], package_content)

        else:
            for model in self._regular_order:
                if self.flopy_models_data[model]:
                    # Basic data model is needed by both mt and mp
                    package_content = self.read_packages(self.flopy_models_data[model])

                    self._flopy_models[model] = self.create_model(self.package_orders[model], package_content)

    @staticmethod
    def read_packages(data):
        package_content = {}
        for package in data['packages']:
            print(f'Read Flopy package data: {package}')
            package_content[package.lower()] = data[package]
        return package_content

    def create_model(self, package_order, package_content):
        model = None
        for package in package_order:
            if package in package_content:
                if package in ['mf', 'mt', 'mp', 'swt']:
                    print(f'Create Flopy Model: {package}')
                    if model == "mt":
                        # In opposition to the other models mt needs the modflow mf data model as basis
                        model = self.create_package(package, package_content[package], self._flopy_models["mf"])
                    else:
                        model = self.create_package(package, package_content[package])
                else:
                    print(f'Create Flopy Package: {package}')
                    # Subpackages are based on main models
                    self.create_package(package, package_content[package], model)

        return model

    @staticmethod
    def create_package(name, content, *model):
        # Modflow packages
        adapter = FLOPY_PACKAGE_TO_ADAPTER_MAPPER[name]

        if name in ['mf', 'mt', 'mp', 'swt']:
            return adapter(content).get_package()
        else:
            adapter(content).get_package(*model)

    @staticmethod
    def write_input_model(model):
        print('Write input files.')
        model.write_input()

    def run_models(self):
        for model_type, model in self._flopy_models.items():
            calculation_adapter = InowasFlopyCalculationAdapter(model, model_type)

            calculation_adapter.check_model()

            calculation_adapter.write_input_model()

            calculation_adapter.run_model()

            if model_type in ["swt", "mf"] and 'hob' in self.flopy_models_data["mf"]['packages']:
                print(f'Calculate hob-statistics and write to file {self._uuid}.hob.stat')
                self.run_hob_statistics(model)

            calculation_success, calculation_report = calculation_adapter.get_success_and_report()

            self._flopy_models_success[model_type] = calculation_success

            self._report += calculation_report

    def get_fitness(self,
                    objectives: list,
                    constraints: list,
                    objects: list) -> Optional[float]:
        overall_success = [self._flopy_models_success[model_type] for model_type in self._flopy_models]

        if all(overall_success):
            fitness_adapter = InowasFlopyReadFitness(objectives, constraints, objects, self._flopy_models["mf"])

            return fitness_adapter.get_fitness()
        else:
            return None

    @staticmethod
    def run_hob_statistics(model):
        print(f'Calculate hob-statistics for data model {model.name}')
        HobStatistics(model.model_ws, model.name).write_to_file()