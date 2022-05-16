
pySuez
=======
Get your consumption data from your Suez account (www.toutsurmoneau.fr) 

This work is inspired by the [Sirus](https://github.com/Sirus10)'s [domoticz sensor](https://github.com/Sirus10/domoticz).
It is also inspired by [`pyLinky`](https://github.com/pirionfr/pyLinky) code from [`Pirionfr`](https://github.com/pirionfr).

Installation
------------

The easiest way to install the library is using [`pip`](https://pip.pypa.io/en/stable/):

    pip install pySuez

You can also download the source code and install it manually::

    cd /path/to/pySuez/
    python setup.py install

Usage
-----
Print your current and history data

    pySuez -u <USERNAME> -p <PASSWORD> -c <COUNTER_ID> -P <PROVIDER_NAME>

You need to get your `COUNTER_ID` either from your bill or from your history consumption on your Suez's website. You can find it in the source code of this webpage, right after `.../mon-compte-en-ligne/statMData/xxxxxxx?...`.
If no provider name is given, `Tout sur mon eau` will be used. The only one supported here is `Eau Olivet`.

Dev env
-------
create virtual env and install requirements

    virtualenv -p /usr/bin/python3.4 env
    pip install -r requirements.txt
