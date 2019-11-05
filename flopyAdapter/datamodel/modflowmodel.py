import json
from jsonschema import Draft7Validator
import urllib.request

SCHEMA_SERVER_URL = 'https://schema.inowas.com'


class ModflowModel:
    _data = None

    def __init__(self, data):
        self._data = data
        pass

    @staticmethod
    def from_data(data):
        ModflowModel.validate(data)
        return ModflowModel(data)

    @staticmethod
    def validate(data):
        mf_schema_data = urllib.request.urlopen('{}/modflow/packages/mfPackages.json'.format(SCHEMA_SERVER_URL))
        mf_schema = json.loads(mf_schema_data.read())
        Draft7Validator(schema=mf_schema).validate(data)

    def data(self):
        return self._data

    def get_package(self, name):
        if name not in self.data():
            raise Exception('Package not found')

        return self.data()[name]

    def nlay(self):
        return self.get_package('dis')['nlay']

    def nrow(self):
        return self.get_package('dis')['nrow']

    def ncol(self):
        return self.get_package('dis')['ncol']

    def nper(self):
        return self.get_package('dis')['nper']

    def add_well(self, lay, row, col, pumping_rates):
        # is_valid_lay
        # is_valid_row
        # is_valid_col
        # is_valid_#_stress_periods

        stress_period_data = self._data.wel.stress_period_data
        if self.nper() != len(pumping_rates):
            raise Exception

        # well_already_exists =>
        # new_well

        return self
