from abc import ABC, abstractmethod


class ModflowPackageAdapterBase(ABC):
    def __init__(self, data):
        self._data = data

    def validate(self):
        # should be implemented
        # for key in content:
        #   do something
        #   return some hints
        pass

    def is_valid(self):
        # should be implemented
        # for key in content:
        #   do something
        #   return true or false
        return True

    @staticmethod
    @abstractmethod
    def default():
        pass

    @staticmethod
    @abstractmethod
    def read_package(package):
        pass

    def merge(self):
        default = self.default()
        for key in self._data:
            if key.startswith('_'):
                continue

            try:
                if key == 'stress_period_data':
                    default[key] = self.to_dict(self._data[key])
                    continue

                default[key] = self._data[key]
            except KeyError:
                pass
        return default

    @staticmethod
    def to_dict(data):
        if type(data) is not list:
            return data

        stress_period_data = {}
        for stress_period, record in enumerate(data):
            stress_period_data[stress_period] = record

        return stress_period_data
