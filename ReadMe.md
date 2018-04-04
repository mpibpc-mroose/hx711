HX711
=====

[![PyPi](https://img.shields.io/pypi/v/hx711.svg)](https://pypi.python.org/pypi/hx711)

[![Travis](https://img.shields.io/travis/mpibpc_mroose/hx711.svg)](https://travis-ci.org/mpibpc_mroose/hx711)

Description
-----------
This library allows to drive a HX711 load cess amplifier with a Raspberry Pi. It just provides the capabilities:

* to set channel an gain and
* to read raw values

**This package requires RPi.GPIO to be installed in Python 3.**

Getting started
---------------

Just install by ```pip3 install HX711```. A basic usage example is given below:

```python
    #!/usr/bin/python3
    from hx711 import HX711

    try:
        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel='A',
            gain=64
        )

        hx711.reset()   # Before we start, reset the HX711 (not obligate)
        measures = hx711.get_raw_data(num_measures=3)
    finally:
        GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

    print("\n".join(measures))
```


License
-------
* Free software: MIT license



Credits
---------
I used https://github.com/gandalf15/HX711/ as base.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
