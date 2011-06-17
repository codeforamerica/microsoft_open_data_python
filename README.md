Microsoft Open Data Python API
==============================

A Python wrapper for the Microsoft Open Data API.


Usage
-----

    >>> from open_data import OpenData
    >>> od = OpenData()
    >>> od.catalog()
    ['bls', 'dc', ... ]

    >>> od.catalog('dc')
    ['BankLocations', 'TrafficCameras', 'ZoningPermits', ... ]

    >>> data = od.query('dc', 'BankLocations')
    >>> print data
    {'all': ['of', 'your', 'data']}

    >>> # Data returned in XML format.
    ... od.query('dc', 'BankLocations', format='xml')

    >>> # JSON-P data is also available.
    ... od.query('dc', 'BankLocations', callback='my_callback')


Copyright
---------

Copyright (c) 2011 Code for America Laboratories.

See LICENSE for details.
