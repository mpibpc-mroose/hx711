#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from unittest import TestCase
from unittest.mock import (
    MagicMock,
    patch
)

MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from hx711 import (
    HX711,
    ParameterValidationError
)


class TestHx711(TestCase):
    """Tests for `hx711` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_01_initialization_with_default_values(self):
        """Test something."""
        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6
        )
        self.assertEqual(
            "A",
            hx711.channel
        )
        self.assertEqual(
            128,
            hx711.channel_a_gain
        )

    def test_02_pins_have_to_be_integers(self):
        test_mapping = {
            "dout_pin_as_string": {
                "dout_pin": "foo",
                "pd_sck_pin": 6
            },
            "pd_sck_pin_as_string": {
                "dout_pin": 5,
                "pd_sck_pin": "bar"
            }
        }
        for name, kwargs in test_mapping.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    HX711(
                        **kwargs
                    )

    def test_03_set_a_channel(self):
        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel="A"
        )
        hx711.channel = "B"
        self.assertTrue(
            "B",
            hx711.channel
        )

    def test_04_set_a_gain(self):
        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel="A",
            gain=128
        )
        hx711.channel_a_gain = 64
        self.assertTrue(
            64,
            hx711.channel_a_gain
        )

    def test_05_channel_name_validation(self):
        test_mapping = {
            "wrong_name": "C",
            "integer": 1,
            "long_string": "channel_A"
        }

        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel="A",
            gain=128
        )

        for name, channel in test_mapping.items():
            with self.subTest(name):
                with self.assertRaises(ParameterValidationError):
                    hx711.channel = channel

        for channel in hx711._valid_channels:
            with self.subTest(
                "valid gain {channel} should ot raise an error".format(
                    channel=channel
                )
            ):
                try:
                    hx711.channel = channel
                except Exception as exception:
                    self.fail("{exception} was raised".format(exception=exception))

    def test_06_gain_validation(self):
        test_mapping = {
            "wrong_gain_raises_error": (256),
            "string_raises_error": ("128")
        }

        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel="A",
            gain=128
        )

        for name, gain in test_mapping.items():
            with self.subTest(name):
                with self.assertRaises(ParameterValidationError):
                    hx711.channel_a_gain = gain

        for value in hx711._valid_gains_for_channel_A:
            with self.subTest(
                "valid gain {value} should not raise".format(
                    value=value
                )
            ):
                try:
                    hx711.channel_a_gain = value
                except Exception as exception:
                    self.fail("{exception} was raised".format(exception=exception))

    def test_07_measure_count_validation(self):
        measure_count_borders = {
            "min": 3,
            "max": 10
        }
        mapping = {
            "negative_count": -10,
            "zero": 0,
            "to low": measure_count_borders["min"] - 1,
            "to high": measure_count_borders["max"] + 1
        }
        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6
        )
        hx711.min_measures = measure_count_borders["min"]
        hx711.max_measures = measure_count_borders["max"]

        for name, count in mapping.items():
            with self.subTest(name):
                with self.assertRaises(ParameterValidationError):
                    hx711._validate_measure_count(times=count)

        # randomly pick three valid values and test
        valid_measure_counts = list(range(measure_count_borders["min"], measure_count_borders["max"] + 1))
        random.shuffle(valid_measure_counts)
        for index in range(1, 4):
            count = valid_measure_counts[index]
            with self.subTest(
                "valid measure count {count} should not raise an error".format(
                    count=count
                )
            ):
                try:
                    hx711._validate_measure_count(count)
                except Exception as exception:
                    self.fail("{exception} was raised".format(exception=exception))
