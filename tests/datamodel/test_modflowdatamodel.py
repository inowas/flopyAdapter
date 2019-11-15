"""Test for 'add_wells' function of the FlopyDataModel class
 """
from pathlib import PurePosixPath
import json
from jsonschema import RefResolver, ValidationError
from copy import deepcopy
from urllib.request import urlopen
import pytest

from flopyAdapter.datamodel.modflowdatamodel import sort_dictionary, ModflowDataModel

HTTPS_STRING = "https://"
SCHEMA_MODFLOW_MODEL_DATA = PurePosixPath("schema.inowas.com/modflow/packages/modflow_model_data.json")

with urlopen(f"{HTTPS_STRING}{SCHEMA_MODFLOW_MODEL_DATA}") as f:
    modflowmodeldata_schema = json.load(f)

resolver = RefResolver(f"{HTTPS_STRING}{SCHEMA_MODFLOW_MODEL_DATA}",
                       referrer=modflowmodeldata_schema)

SAMPLE_FILE_WELL_WITH_SAME_POSITION = "tests/test_data/modflow_model_data.json"

with open(SAMPLE_FILE_WELL_WITH_SAME_POSITION) as f:
    modflowmodeldata = json.load(f)

FILE_TEST1_TEST2 = "tests/test_data/data_test1_test2.json"
FILE_TEST3 = "tests/test_data/data_test3.json"
FILE_TEST4 = "tests/test_data/data_test4.json"


def test_function_sort_dictionary():
    # test for: no dictionary passed
    with pytest.raises(TypeError):
        sort_dictionary("abc", False)

    # test for: empty dictionary
    assert sort_dictionary({}, False) == {}

    # test for: multilayer dictionary sorting
    assert sort_dictionary({"b": 2, "a": {"d": 4, "c": 3}}, recursive=True) == {"a": {"c": 3, "d": 4}, "b": 2}

    # test for: different key types
    with pytest.raises(TypeError):
        sort_dictionary({"a": 1, 2: 2}, recursive=False)


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
                "ipakcb": 0,
                "stress_period_data": {
                        "0": [[0, 0, 0, 0]]
                    },
                "dtype": None,
                "extension": 'wel',
                "unitnumber": 20,
                "options": None
            }
        }})

    model.add_well(0, 0, 0, [1000])

    assert model.data == {"mf": {"dis": {"nlay": 1, "nrow": 1, "ncol": 1, "nper": 1},
                                 "wel": {
                                    "ipakcb": 0,
                                    "stress_period_data": {
                                            "0": [[0, 0, 0, 1000]]
                                        },
                                    "dtype": None,
                                    "extension": 'wel',
                                    "unitnumber": 20,
                                    "options": None
                                 }
                                }}

    # model.add_well(0, 0, 0, [-1000])
    #
    # assert model.data == {"mf": {"dis": {"nlay": 1, "nrow": 1, "ncol": 1, "nper": 1},
    #                              "wel": {"stress_period_data": {"0": [[0, 0, 0, 0000]]}}}}


def test_modflowdatamodel_add_well_out_of_bounds():
    """ Test for adding a well which is not sticking to the model bounds
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

    # Test for: out of bounds lay, row, col
    with pytest.raises(ValueError):
        model.add_well(1, 1, 1, [1000])

    # test for: out of bounds pumping rates
    with pytest.raises(ValueError):
        model.add_well(0, 0, 0, [1000, 1000.0])

    # test for: types
    with pytest.raises(TypeError):
        model.add_well(0, 0, 0, ["1000"])

    with pytest.raises(TypeError):
        model.add_well("1", 0, 0, [1000])


def test_modflowdatamodel_add_objects():
    """ Test for adding several objects at once
    """

    model = ModflowDataModel(
        {"mf": {
            "dis": {"nlay": 2, "nrow": 2, "ncol": 2, "nper": 1},
            "wel": {
                "stress_period_data": {
                    "0": [[0, 0, 0, 0]]
                }
            }
        }}
    )

    # test for: KeyError not finding "result" in lay, row, col, flux
    with pytest.raises(KeyError):
        model.add_objects([
          {
            "id": "e47d91d9-332e-45f0-8c67-b6e9cdf1c5ad",
            "type": "wel",
            "position": {
              "row": {
                "min": 0,
                "max": 1
              },
              "col": {
                "min": 0,
                "max": 1
              },
              "lay": {
                "min": 0,
                "max": 1
              }
            },
            "flux": {
              "0": {
                "min": 1000,
                "max": 1000
              }
            }
          }
        ])

    model.add_objects([
        {
            "id": "e47d91d9-332e-45f0-8c67-b6e9cdf1c5ad",
            "type": "wel",
            "position": {
                "row": {
                    "min": 0,
                    "max": 1,
                    "result": 0
                },
                "col": {
                    "min": 0,
                    "max": 1,
                    "result": 0
                },
                "lay": {
                    "min": 0,
                    "max": 1,
                    "result": 0
                }
            },
            "flux": {
                "0": {
                    "min": 1000,
                    "max": 1000,
                    "result": 1000
                }
            }
        },
        {
            "id": "732c2c05-3510-4cb4-826f-ea2ce4c487e1",
            "type": "wel",
            "position": {
                "row": {
                    "min": 0,
                    "max": 1,
                    "result": 1
                },
                "col": {
                    "min": 0,
                    "max": 1,
                    "result": 1
                },
                "lay": {
                    "min": 0,
                    "max": 1,
                    "result": 1
                }
            },
            "flux": {
                "0": {
                    "min": 1000,
                    "max": 1000,
                    "result": 1000
                }
            }
        }
    ])

    assert model.data == {"mf": {
            "dis": {"nlay": 2, "nrow": 2, "ncol": 2, "nper": 1},
            "wel": {
                "ipakcb": 0,
                "stress_period_data": {
                    "0": [[0, 0, 0, 1000], [1, 1, 1, 1000]]
                },
                "dtype": None,
                "extension": 'wel',
                "unitnumber": 20,
                "options": None
            }
        }}


def test_modflowdatamodel_md5_hash():
    test_data = deepcopy(modflowmodeldata)

    # test for: md5 hash of sorted model (encoded with utf-8)
    assert ModflowDataModel(test_data).md5_hash == "1a767e066f862b61a9cb172ef95401ef"
