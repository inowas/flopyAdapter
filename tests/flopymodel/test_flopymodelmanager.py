import json
from flopyAdapter.datamodel.modflowdatamodel import ModflowDataModel
from flopyAdapter.flopymodel.flopymodelmanager import FlopyModelManager

SAMPLE_FILE_WELL_WITH_SAME_POSITION = "tests/test_data/modflow_model_data.json"

with open(SAMPLE_FILE_WELL_WITH_SAME_POSITION) as f:
    modflowmodeldata = json.load(f)


def test_flopymodel():
    flopymodelmanager = FlopyModelManager(ModflowDataModel(modflowmodeldata))

    assert flopymodelmanager.flopy_packages == {}

    flopymodelmanager.build_flopymodel()

    assert flopymodelmanager.flopy_packages.get("mf").get_package_list() == \
        ["DIS", "BAS6", "GHB", "WEL",  "LPF", "PCG", "OC"]
