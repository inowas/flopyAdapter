import json
from flopyAdapter.flopymodel.flopymodelmanager import FlopyModelManager
from flopyAdapter.flopy_adapter.flopy_calculationadapter import FlopyCalculationAdapter

SAMPLE_FILE_WELL_WITH_SAME_POSITION = "tests/test_data/modflow_model_data.json"

with open(SAMPLE_FILE_WELL_WITH_SAME_POSITION) as f:
    modflowmodeldata = json.load(f)



def test_flopy_calculation_adapter():
    flopymodelmanager = FlopyModelManager(modflowmodeldata)

    FlopyCalculationAdapter.from_flopymodel(model=flopymodelmanager.flopy_packages["mf"])

    pass
