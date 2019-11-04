"""Test for 'add_wells' function of the FlopyDataModel class
 """

import pytest
from copy import deepcopy
import json
from flopyAdapter.datamodel.flopydatamodel import FlopyDataModel

SAMPLE_FILE_WELL_WITH_SAME_POSITION = "tests/test_data/request-well-with-same-position.json"

with open(SAMPLE_FILE_WELL_WITH_SAME_POSITION) as f:
    request_data = json.load(f)

FILE_TEST1_TEST2 = "tests/test_data/data_test1_test2.json"
FILE_TEST3 = "tests/test_data/data_test3.json"
FILE_TEST4 = "tests/test_data/data_test4.json"


def test_add_well_1():
    """ Test for adding a well to not existing stress period data (default)
    """

    test_data = deepcopy(request_data)

    # Modify
    test_data["data"]["mf"]["wel"]["stress_period_data"] = None

    with open(FILE_TEST1_TEST2) as f:
        expected_data = json.load(f)

    flopy_data_model = FlopyDataModel(version=test_data["version"],
                                      data=test_data["data"],
                                      uuid=test_data["optimization_id"])

    flopy_data_model.add_wells(test_data["optimization"]["objects"])

    assert flopy_data_model.flopy_models_data["mf"]["wel"] == expected_data["wel"]


def test_add_well_2():
    """ Test for adding a well to empty stress period data (-> {})
        """

    test_data = deepcopy(request_data)

    # Modify
    test_data["data"]["mf"]["wel"]["stress_period_data"] = {}

    with open(FILE_TEST1_TEST2) as f:
        expected_data = json.load(f)

    flopy_data_model = FlopyDataModel(version=test_data["version"],
                                      data=test_data["data"],
                                      uuid=test_data["optimization_id"])

    flopy_data_model.add_wells(test_data["optimization"]["objects"])

    assert flopy_data_model.flopy_models_data["mf"]["wel"] == expected_data["wel"]


def test_add_well_3():
    """ Test for adding an additional well on an existing position in wel package
    """

    # No further changes
    test_data = deepcopy(request_data)

    with open(FILE_TEST3) as f:
        expected_data = json.load(f)

    flopy_data_model = FlopyDataModel(version=test_data["version"],
                                      data=test_data["data"],
                                      uuid=test_data["optimization_id"])

    flopy_data_model.add_wells(test_data["optimization"]["objects"])

    assert flopy_data_model.flopy_models_data["mf"]["wel"] == expected_data["wel"]


def test_add_well_4():
    """ Test for adding an additional well on a different position then the ones existing
    """

    test_data = deepcopy(request_data)

    # Modify the location of the added well
    well = test_data["optimization"]["objects"][0]
    well["position"]["row"]["result"] = 39
    well["position"]["col"]["result"] = 74
    well["position"]["lay"]["result"] = 0

    with open(FILE_TEST4) as f:
        expected_data = json.load(f)

    flopy_data_model = FlopyDataModel(version=test_data["version"],
                                      data=test_data["data"],
                                      uuid=test_data["optimization_id"])

    flopy_data_model.add_wells(test_data["optimization"]["objects"])

    assert flopy_data_model.flopy_models_data["mf"]["wel"] == expected_data["wel"]
