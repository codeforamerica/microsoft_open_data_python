#!/usr/bin/env python

"""Unit tests for the `open_data` module."""

import unittest

from mock import Mock

from open_data.api import api
from open_data import OpenData


class TestOpenDataInit(unittest.TestCase):

    def test_OpenData_init(self):
        od = OpenData()
        self.assertEquals(od.base_url, 'http://ogdi.cloudapp.net')
        self.assertEquals(od.output_format, 'json')
        self.assertEquals(od.version, 'v1')

    def test_different_version_init(self):
        od = OpenData(version=2)
        self.assertEquals(od.version, 'v2')


class TestCatalogMethod(unittest.TestCase):


    def setUp(self):
        xml_catalog = """<?xml version='1.0' encoding='utf-8'?>
            <service xml:base='http://ogdi.cloudapp.net/v1/dc/'
                     xmlns:atom='http://www.w3.org/2005/Atom'
                     xmlns:app='http://www.w3.org/2007/app'
                     xmlns='http://www.w3.org/2007/app'>
              <workspace>
                <atom:title>Default</atom:title>
                <collection href='AmbulatorySurgicalCenters'>
                  <atom:title>AmbulatorySurgicalCenters</atom:title>
                </collection>
                <collection href='BankLocations'>
                  <atom:title>BankLocations</atom:title>
                </collection>
              </workspace>
            </service>"""
        api.urlopen = Mock()
        api.urlopen().read.return_value = xml_catalog
        api.json = Mock()

    def test_url_called_from_default_catalog_method(self):
        OpenData().catalog()
        expected_url = 'http://ogdi.cloudapp.net/v1?format=json'
        api.urlopen.assert_called_with(expected_url)

    def test_url_called_for_catalog_agency(self):
        OpenData().catalog('test')
        expected_url = 'http://ogdi.cloudapp.net/v1/test?format=json'
        api.urlopen.assert_called_with(expected_url)


class TestQueryMethod(unittest.TestCase):

    def setUp(self):
        api.urlopen = Mock()
        api.json = Mock()

    def test_query_method_for_bank_locations(self):
        OpenData().query('dc', 'BankLocations')
        expected_url = ('http://ogdi.cloudapp.net/v1/dc/'
                        'BankLocations?format=json')
        api.urlopen.assert_called_with(expected_url)

    def test_jsonp_callback_keyword(self):
        OpenData().query('dc', 'test', callback='my_callback')
        expected_url = ('http://ogdi.cloudapp.net/v1/dc/'
                        'test?callback=my_callback&format=json')
        api.urlopen.assert_called_with(expected_url)
        self.assertEquals(api.json.call_count, 0)


if __name__ == '__main__':
    unittest.main()
