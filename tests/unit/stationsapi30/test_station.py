#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pyowm.commons.exceptions
from pyowm.stationsapi30.station import Station


class TestStation(unittest.TestCase):

    _test_instance = Station("583436dd9643a9000196b8d6",
                             "2016-11-22T12:15:25.967Z",
                             "2016-11-22T12:15:25.967Z",
                             "SF_TEST001",
                             "San Francisco Test Station",
                             -122.43, 37.76, 150, 0)

    def test_format_micros(self):
        # micros are present and must be padded
        input_string = "2016-11-22T12:15:25.967Z"
        expected = "2016-11-22T12:15:25.000967Z"
        result = self._test_instance._format_micros(input_string)
        self.assertEquals(expected, result)

        # micros are present but too many digits
        input_string = "2017-08-25T18:16:16.487887736Z"
        expected = "2017-08-25T18:16:16.487887Z"
        result = self._test_instance._format_micros(input_string)
        self.assertEquals(expected, result)

        # no micros at all
        input_string = "2016-11-22T12:15:25Z"
        expected = "2016-11-22T12:15:25.000000Z"
        result = self._test_instance._format_micros(input_string)
        self.assertEquals(expected, result)

        # no micros at all n.2
        input_string = "2016-11-22T12:15:25"
        expected = "2016-11-22T12:15:25.000000Z"
        result = self._test_instance._format_micros(input_string)
        self.assertEquals(expected, result)

    def test_failing_instantiations(self):
        with self.assertRaises(AssertionError):
            Station(None,
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    None,
                    "San Francisco Test Station",
                    -122.43, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    None, 37.76, 150, 0)
        with self.assertRaises(AssertionError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, None, 150, 0)

    def test_instantiations_failing_upon_wrong_geocoords(self):
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -422.43, 37.76, 150, 0)
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, -97.76, 150, 0)
        with self.assertRaises(ValueError):
            Station("583436dd9643a9000196b8d6",
                    "2016-11-22T12:15:25.967Z",
                    "2016-11-22T12:15:25.967Z",
                    "SF_TEST001",
                    "San Francisco Test Station",
                    -122.43, 37.76, -56.9, 0)

    def test_repr(self):
        print(self._test_instance)

    def test_from_dictionary(self):
        the_dict = {
            'id': '583436dd9643a9000196b8d6',
            'altitude': 150,
            'created_at': '2016-11-22T12:15:25.967Z',
            'external_id': 'SF_TEST001',
            'latitude': 37.76,
            'longitude': -122.43,
            'name': 'San Francisco Test Station',
            'rank': 0,
            'updated_at': '2016-11-22T12:15:25.967Z'}

        result = Station.from_dict(the_dict)
        self.assertTrue(isinstance(result, Station))
        self.assertEqual(self._test_instance.id, result.id)
        self.assertEqual(self._test_instance.created_at, result.created_at)
        self.assertEqual(self._test_instance.updated_at, result.updated_at)
        self.assertEqual(self._test_instance.name, result.name)
        self.assertEqual(self._test_instance.lon, result.lon)
        self.assertEqual(self._test_instance.lat, result.lat)
        self.assertEqual(self._test_instance.alt, result.alt)
        self.assertEqual(self._test_instance.rank, result.rank)

        with self.assertRaises(pyowm.commons.exceptions.ParseAPIResponseError):
            Station.from_dict(None)

    def test_to_dict(self):
        expected = {
            'id': '583436dd9643a9000196b8d6',
            'altitude': 150,
            'created_at': '2016-11-22 12:15:25+00',
            'external_id': 'SF_TEST001',
            'latitude': 37.76,
            'longitude': -122.43,
            'name': 'San Francisco Test Station',
            'rank': 0,
            'updated_at': '2016-11-22 12:15:25+00'}
        result = self._test_instance.to_dict()
        self.assertEqual(expected, result)
