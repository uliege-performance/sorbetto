import pytest

from sorbetto.core.importance import Importance


def test_properties():
    importance_object = Importance(1.0, 0.5, 0.2, 0.8, name="TestName")
    assert importance_object.itn == 1.0
    assert importance_object.ifp == 0.5
    assert importance_object.ifn == 0.2
    assert importance_object.itp == 0.8
    assert importance_object.name == "TestName"


def test_equality():
    importance1 = Importance(1.0, 0.5, 0.2, 0.8, name="Prefs1")
    importance2 = Importance(1.0, 0.5, 0.2, 0.8, name="Prefs2")

    assert importance1 == importance2


def test_inequality():
    importance1 = Importance(1.0, 0.5, 0.2, 0.8, name="Prefs1")
    importance3 = Importance(1.1, 0.5, 0.2, 0.8, name="Prefs3")

    assert importance1 != importance3
    assert importance1 != "not an Importance object"


def test_invalid_values():
    with pytest.raises(ValueError):
        Importance(-1.0, 0.5, 0.2, 0.8)

    with pytest.raises(ValueError):
        Importance(1.0, -0.5, 0.2, 0.8)

    with pytest.raises(ValueError):
        Importance(1.0, 0.5, -0.2, 0.8)

    with pytest.raises(ValueError):
        Importance(1.0, 0.5, 0.2, -0.8)

    with pytest.raises(ValueError):
        Importance(0, 0, 0, 0)
