"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format.

Author: Ralf Junghanns
EMail: ralf.junghanns@gmail.com
"""


class FlopyCalculationAdapter:
    """The Flopy Class"""

    def __init__(self,
                 model):

        self._model = model

        self._report = None
        self._success = None

    @staticmethod
    def from_flopymodel(model):
        try:
            # Check model consistency
            model.check()
        except AttributeError:
            raise AttributeError(f"Error: model expected to have attributes 'name' and 'model_ws' and 'check' method \n"
                                 f"model is of type {type(model)}, expected Modflow/Modpath/Mt3dms.")
        except Exception:
            raise Exception("The model check must have detected some problems. Check your model.")

        return FlopyCalculationAdapter(model)

    def check_model(self):
        if self._model:
            self._model.check()

    def write_input_model(self):
        print('Write input files.')
        self._model.write_input()

    def run_calculation(self):
        normal_msg = 'Normal termination'

        print('Run datamodel.')
        print(f'Model nam-file: {self._model.namefile}.')
        print(f'Model executable: {self._model.exe_name}.')
        self._success, report = self._model.run_model(report=True, silent=True, normal_msg=normal_msg)

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
