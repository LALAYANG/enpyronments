"""Tests for the Settings class"""
import os
import re

import pytest

from enpyronments.settings import Sensitive, Settings


def test_empty():
    """ Ensure an empty object doesn't error out (shouldn't be an issue, but makes me feel better) """

    settings = Settings()
    return settings


def test_masked(test_key, test_setting, is_sensitive, actual_value):
    """ Ensure accessing Settings.masked() elements via __getitem__ returns the underlying value when the test_key points
    to a Sensitive object"""

    masked_settings = test_setting.masked()

    if is_sensitive:
        assert (
            masked_settings.get(test_key) != actual_value
        ), "Shouldn't get a sensitive value back from masked settings"
        assert re.match(
            r"\*+", masked_settings.get(test_key)
        ), "Should get a bunch of stars back from a sensitive value in masked settings"
    else:
        assert masked_settings.get(test_key) == actual_value


def test_getitem(test_setting, test_key, actual_value):
    with pytest.raises(KeyError):
        test_setting[test_key]
    """ Ensure Sensitive objects return their underlying value """
    assert test_setting[test_key] == actual_value


def test_get(test_setting, test_key, actual_value):
    assert test_setting.get(test_key) == actual_value


def test_setitem(test_setting, test_key, actual_value, is_sensitive):
    test_setting[test_key] = actual_value

    assert test_setting[test_key] == actual_value

    if is_sensitive:
        assert isinstance(test_setting.data[test_key], Sensitive)


def test_getattr(test_setting, test_key, bad_key, actual_value):
    with pytest.raises(KeyError):
        getattr(test_setting, bad_key)
    assert getattr(test_setting, test_key) == actual_value
    # make sure lower case accessors work too
    assert getattr(test_setting, str(test_key).lower()) == actual_value


def test_delitem(test_setting, test_key):
    del test_setting[test_key]
    with pytest.raises(KeyError):
        test_setting[test_key]


def test_iter(test_setting, test_key):
    for key in test_setting:
        assert key == test_key
        
def test_keys(test_setting, test_key):
    for key in test_setting.keys():
        assert key == test_key


def test_len(test_setting):
    assert len(test_setting) == len(test_setting.data)


def test_items(test_setting, test_key, actual_value):
    for key, val in test_setting.items():
        assert key == test_key
        assert val == actual_value


def test_values(test_setting, actual_value):
    for val in test_setting.values():
        assert val == actual_value


def test_save_to_environ(test_setting, test_key, actual_value):
    test_setting.save_to_environ()
    # breaks if not serializable, but that's ok
