
pySuez
=======

.. image:: https://travis-ci.org/ooii/pySuez.svg?branch=master
    :target: https://travis-ci.org/ooii/pySuez

.. image:: https://img.shields.io/pypi/v/pySuez.svg
    :target: https://pypi.python.org/pypi/pySuez

.. image:: https://img.shields.io/pypi/pyversions/pySuez.svg
    :target: https://pypi.python.org/pypi/pySuez

.. image:: https://requires.io/github/ooii/pySuez/requirements.svg?branch=master
    :target: https://requires.io/github/ooii/pySuez/requirements/?branch=master
    :alt: Requirements Status

Get your consumption data from your Suez account (www.toutsurmoneau.fr) 

This work is inspired by the domoticz sensor (https://github.com/Sirus10/domoticz), created by Sirus10 (https://github.com/Sirus10)

Installation
------------

The easiest way to install the library is using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install pySuez

You can also download the source code and install it manually::

    cd /path/to/pySuez/
    python setup.py install

Usage
-----
Print your current and history data

    pySuez -u <USERNAME> -p <PASSWORD> -c <COUNTER_ID>

You need to get your `COUNTER_ID` either from your bill or from your history consumption on your Suez's website. You can find it in the source code of this webpage, right after `.../mon-compte-en-ligne/statMData/xxxxxxx?...`.

Dev env
-------
create virtual env and install requirements

    virtualenv -p /usr/bin/python3.5 env
    pip install -r requirements.txt
