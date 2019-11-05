import pytest
import json
from jsonschema import ValidationError
from flopyAdapter.datamodel.modflowmodel import ModflowModel

DATA_FILE = "./modflowmodel_test_data.json"


def test_instantiate_modflowmodel():
    with pytest.raises(ValidationError):
        ModflowModel.from_data('abc')


def test_instantiate_with_valid_data():
    with open(DATA_FILE) as f:
        data = json.load(f)
    model = ModflowModel.from_data(data)
    assert isinstance(model, ModflowModel)


def test_add_well():
    model = ModflowModel({
        "wel": {
            "stress_period_data": {
                "0": [
                    [
                        0,
                        14,
                        39,
                        -4000
                    ],
                    [
                        0,
                        20,
                        36,
                        -5000
                    ]
                ]
            },
        },
    })

    model.add_well(0, 14, 39, 4000)

    assert model.data() == {
        "wel": {
            "stress_period_data": {
                "0": [
                    [
                        0,
                        14,
                        39,
                        0
                    ],
                    [
                        0,
                        20,
                        36,
                        -5000
                    ]
                ]
            },
        },
    }
