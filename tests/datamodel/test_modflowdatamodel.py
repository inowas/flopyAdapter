"""Test for 'add_wells' function of the FlopyDataModel class
 """
from pathlib import PurePosixPath
import json
from jsonschema import Draft7Validator, RefResolver
from jsonschema.exceptions import ValidationError
from copy import deepcopy
from urllib.request import urlopen
import pytest

from flopyAdapter.datamodel.modflowdatamodel import sort_dictionary, ModflowDataModel

HTTPS_STRING = "https://"
SCHEMA_MODFLOW_MODEL_DATA = PurePosixPath("schema.inowas.com/modflow/packages/modflow_model_data.json")

with urlopen(f"{HTTPS_STRING}{SCHEMA_MODFLOW_MODEL_DATA}") as f:
    modflowmodeldata_schema = json.load(f)

resolver = RefResolver(f"{HTTPS_STRING}{SCHEMA_MODFLOW_MODEL_DATA.parent}",
                       referrer=modflowmodeldata_schema)

SAMPLE_FILE_WELL_WITH_SAME_POSITION = "tests/test_data/modflow_model_data.json"

with open(SAMPLE_FILE_WELL_WITH_SAME_POSITION) as f:
    modflowmodeldata = json.load(f)

FILE_TEST1_TEST2 = "tests/test_data/data_test1_test2.json"
FILE_TEST3 = "tests/test_data/data_test3.json"
FILE_TEST4 = "tests/test_data/data_test4.json"


def test_function_sort_dictionary():
    # test for: no dictionary passed
    with pytest.raises(AssertionError):
        sort_dictionary("bla", False)

    # test for: empty dictionary
    assert sort_dictionary({}, False) == {}

    # test for: multilayer dictionary sorting
    assert sort_dictionary({"b": 2, "a": {"d": 4, "c": 3}}, recursive=True) == {"a": {"c": 3, "d": 4}, "b": 2}


def test_modflowdatamodel_schemavalidation():
    # test for: valid schema
    test_data = deepcopy(modflowmodeldata)

    assert ModflowDataModel.from_data(test_data, modflowmodeldata_schema, resolver)  # expect a instance of object

    # test for: invalid schema
    del test_data["mf"]  # remove mf package from data

    with pytest.raises(ValidationError):
        ModflowDataModel.from_data(test_data, modflowmodeldata_schema, resolver)


def test_modflowdatamodel_add_well_to_existing_wells():
    """ Test for adding a well to not existing stress period data (default)
    """

    model = ModflowDataModel(
        {"mf": {
            "dis":{"nlay": 1, "nrow": 1, "ncol": 1, "nper": 1},
            "wel": {
                "stress_period_data": {
                    "0": [[0, 0, 0, 0]]
                }
            }
        }})
    model.add_well(0, 0, 0, [1000])

    assert model.data == {"mf": {"dis": {"nlay": 1, "nrow": 1, "ncol": 1, "nper": 1},
                                 "wel": {"stress_period_data": {"0": [[0, 0, 0, 1000]]}}}}

    model.add_well(0, 0, 0, [-1000])

    assert model.data == {"mf": {"dis": {"nlay": 1, "nrow": 1, "ncol": 1, "nper": 1},
                                 "wel": {"stress_period_data": {"0": [[0, 0, 0, 0000]]}}}}


# def test_add_well_2():
#     """ Test for adding a well to empty stress period data (-> {})
#         """
#
#     test_data = deepcopy(request_data)
#
#     # Modify
#     test_data["data"]["mf"]["wel"]["stress_period_data"] = {}
#
#     with open(FILE_TEST1_TEST2) as f:
#         expected_data = json.load(f)
#
#     flopy_data_model = ModflowDataModel(data=test_data["data"])
#
#     flopy_data_model.add_objects(test_data["optimization"]["objects"])
#
#     assert flopy_data_model.get_package("mf", "wel") == expected_data["wel"]
#
#
# def test_add_well_3():
#     """ Test for adding an additional well on an existing position in wel package
#     """
#
#     # No further changes
#     test_data = deepcopy(request_data)
#
#     with open(FILE_TEST3) as f:
#         expected_data = json.load(f)
#
#     flopy_data_model = ModflowDataModel(data=test_data["data"])
#
#     flopy_data_model.add_objects(test_data["optimization"]["objects"])
#
#     assert flopy_data_model.get_package("mf", "wel") == expected_data["wel"]
#
#
# def test_add_well_4():
#     """ Test for adding an additional well on a different position then the ones existing
#     """
#
#     test_data = deepcopy(request_data)
#
#     # Modify the location of the added well
#     well = test_data["optimization"]["objects"][0]
#     well["position"]["row"]["result"] = 39
#     well["position"]["col"]["result"] = 74
#     well["position"]["lay"]["result"] = 0
#
#     with open(FILE_TEST4) as f:
#         expected_data = json.load(f)
#
#     flopy_data_model = ModflowDataModel(data=test_data["data"])
#
#     flopy_data_model.add_objects(test_data["optimization"]["objects"])
#
#     assert flopy_data_model.get_package("mf", "wel") == expected_data["wel"]
