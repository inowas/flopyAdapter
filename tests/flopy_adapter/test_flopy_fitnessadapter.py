import pytest
from copy import deepcopy
from pathlib import Path
from flopyAdapter.flopy_adapter.flopy_fitnessadapter import FlopyFitnessAdapter

CALCULATION_ID = "abc123"
FOLDER = Path(__file__).parent.parent / "test_data" / "test_model"

SAMPLE_OPTIMIZATION_DATA = {
    "parameters": {
      "method": "GA",
      "ngen": 5,
      "pop_size": 10,
      "mutpb": 0.1,
      "cxpb": 0.9,
      "eta": 20,
      "indpb": 0.2,
      "diversity_flg": True,
      "ncls": 3,
      "maxf": 10,
      "qbound": 0.25,
      "number_of_solutions": 3
    },
    "objectives": [
      {
        "type": "head",
        "summary_method": "max",
        "weight": 1,
        "penalty_value": 999,
        "location": {
          "type": "bbox",
          "ts": {
            "min": 0,
            "max": 0
          },
          "lay": {
            "min": 0,
            "max": 0
          },
          "row": {
            "min": 20,
            "max": 20
          },
          "col": {
            "min": 45,
            "max": 45
          }
        }
      }
    ],
    "constraints": [],
    "objects": [
      {
        "id": 0,
        "type": "well",
        "position": {
          "row": {
            "min": 10,
            "max": 39
          },
          "col": {
            "min": 10,
            "max": 74
          },
          "lay": {
            "min": 0,
            "max": 0
          }
        },
        "flux": {
          "0": {
            "min": 1000,
            "max": 1000
          }
        }
      },
      {
        "id": 1,
        "type": "well",
        "position": {
          "row": {
            "min": 10,
            "max": 39
          },
          "col": {
            "min": 10,
            "max": 74
          },
          "lay": {
            "min": 0,
            "max": 0
          }
        },
        "flux": {
          "0": {
            "min": 1000,
            "max": 1000
          }
        }
      }
    ]
  }

# possible constraint with seawat
# {
#         "type": "concentration",
#         "conc_file_name": "MT3D001.UCN",
#         "summary_method": "max",
#         "operator": "less",
#         "value": 2,
#         "location": {
#           "type": "bbox",
#           "ts": {"min": 0, "max": 0},
#           "lay": {"min": 0, "max": 0},
#           "row": {"min": 20, "max": 20},
#           "col": {"min": 20, "max": 20}
#         }
#       }


def test_flopy_fitnessadapter_initialization():
    test_optimization_data = deepcopy(SAMPLE_OPTIMIZATION_DATA)

    # test for: type of calculation_id
    with pytest.raises(TypeError):
        FlopyFitnessAdapter.from_id(test_optimization_data, 123, FOLDER)

    # test for: wrong folder
    with pytest.raises(NotADirectoryError):
        FlopyFitnessAdapter.from_id(test_optimization_data, CALCULATION_ID, "random/folder")

    # test for: missing namfile
    # not working as calculation_id is used as folder and thus would always first throw a
    # NotADirectoryError
    # with pytest.raises(FileNotFoundError):
    #     FlopyFitnessAdapter.from_id(test_optimization_data, "no_valid_calculationid", FOLDER)

    # test for: false optimization_data
    with pytest.raises(KeyError):
        FlopyFitnessAdapter.from_id({}, CALCULATION_ID, FOLDER)


def test_flopy_fitnessadapter_get_fitness():
    test_optimization_data = deepcopy(SAMPLE_OPTIMIZATION_DATA)

    assert FlopyFitnessAdapter.from_id(test_optimization_data, CALCULATION_ID, FOLDER).\
        get_fitness() == [436.8322448730469]

    # test for: false objective type (results in ValueError as one of the values is None)
    test_optimization_data = deepcopy(SAMPLE_OPTIMIZATION_DATA)
    test_optimization_data["objectives"][0]["type"] = "nonsense_type"

    with pytest.raises(ValueError):
        FlopyFitnessAdapter.from_id(test_optimization_data, CALCULATION_ID, FOLDER). \
            get_fitness()

    # test for: false constraint type (results in ValueError as one of the values is None)
    # cant be test atm without sample constraint
    # test_optimization_data = deepcopy(SAMPLE_OPTIMIZATION_DATA)
    # test_optimization_data["constraints"][0]["type"] = "nonsense_type"
    #
    # with pytest.raises(ValueError):
    #     FlopyFitnessAdapter.from_id(test_optimization_data, CALCULATION_ID, FOLDER). \
    #         get_fitness()
