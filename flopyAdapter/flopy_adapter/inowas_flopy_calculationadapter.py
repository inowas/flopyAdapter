"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format.

Author: Ralf Junghanns
EMail: ralf.junghanns@gmail.com
"""

from flopyAdapter.flopy_adapter.flopy_read_classes.readbudget import ReadBudget
from flopyAdapter.flopy_adapter.flopy_read_classes.readconcentration import ReadConcentration
from flopyAdapter.flopy_adapter.flopy_read_classes.readdrawdown import ReadDrawdown
from flopyAdapter.flopy_adapter.flopy_read_classes.readhead import ReadHead

from flopyAdapter.flopy_adapter.statistics.hobstatistics import HobStatistics


class InowasFlopyCalculationAdapter:
    """The Flopy Class"""

    _report = None
    _success = None

    def __init__(self,
                 model,
                 model_type):
        # todo checks for input

        self.model = model
        self.model_type = model_type

    def check_model(self):
        if self.model:
            self.model.check()

    def write_input_model(self):
        print('Write input files.')
        self.model.write_input()

    def run_model(self):
        normal_msg = 'Normal termination'
        if self.model_type == 'mt':
            normal_msg = 'Program completed'

        print('Run datamodel.')
        print(f'Model nam-file: {self.model.namefile}.')
        print(f'Model executable: {self.model.exe_name}.')
        self._success, report = self.model.run_model(report=True, silent=True, normal_msg=normal_msg)

        self._report = ' \n'.join(str(e) for e in report)

    def get_success_and_report(self):
        return self._success, self._report

    # def response(self):
    #     #     key = 'mf'
    #     #     if 'MF' in self._mf_data:
    #     #         key = 'MF'
    #     #
    #     #     budgets = ReadBudget(self._mf_data[key]['model_ws'])
    #     #     concentrations = ReadConcentration(self._mf_data[key]['model_ws'])
    #     #     drawdowns = ReadDrawdown(self._mf_data[key]['model_ws'])
    #     #     heads = ReadHead(self._mf_data[key]['model_ws'])
    #     #
    #     #     return {
    #     #         'budgets': budgets.read_times(),
    #     #         'concentrations': concentrations.read_times(),
    #     #         'drawdowns': drawdowns.read_times(),
    #     #         'heads': heads.read_times(),
    #     #         'number_of_layers': heads.read_number_of_layers()
    #     #     }

    # def success(self):
    #     return self._success
    #
    # def response_message(self):
    #     return self._report
