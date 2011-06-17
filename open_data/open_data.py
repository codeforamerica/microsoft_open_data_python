#!/usr/bin/env python

"""Python wrapper for the Microsoft Open Data API."""

from xml.etree import ElementTree

from api import API


class OpenData(API):
    """Python wrapper for the Microsoft Open Data API."""

    def __init__(self, version=1):
        super(OpenData, self).__init__()
        self.base_url = 'http://ogdi.cloudapp.net'
        self.output_format = 'json'
        self.required_params = None
        self.version = 'v%d' % version

    def _resolve_url(self, path='', **kwargs):
        """Internal method to resolve format parameter called."""
        if 'format' not in kwargs:
            # Always default to JSON.
            kwargs['format'] = 'json'
        if 'callback' in kwargs or kwargs['format'] == 'kml':
            # Return the JSON-P data.
            kwargs['output_format'] = None
        if path:
            path = '/'.join([self.version, path])
        else:
            path = self.version
        return self.call_api(path, **kwargs)

    def catalog(self, agency=None):
        """
        Returns the available catalog data from the Microsoft Open Data API.

        >>> od = OpenData()
        >>> od.catalog()
        ['list', 'of', 'available', 'agencies', ...]
        >>> od.catalog('bls')
        ['list', 'of', 'available', 'datasets', ...]
        """
        xml_data = self._resolve_url(agency, output_format=None)
        names = self._parse_xml_catalog(xml_data)
        return names

    def _parse_xml_catalog(self, xml_data):
        """
        Internal method to parse the Microsoft Open Data API catalog
        of either agencies or projects.
        """
        node = ElementTree.XML(xml_data)
        workspace = node.find('{http://www.w3.org/2007/app}workspace')
        collection = workspace.findall('{http://www.w3.org/2007/app}collection')
        names = [element.attrib.get('href') for element in collection]
        return names

    def query(self, agency, dataset, **kwargs):
        """Query a specific agency's dataset."""
        path = '/'.join([agency, dataset])
        return self._resolve_url(path, **kwargs)
