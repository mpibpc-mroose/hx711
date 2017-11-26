=====
HX711
=====


.. image:: https://img.shields.io/pypi/v/hx711.svg
        :target: https://pypi.python.org/pypi/hx711

.. image:: https://img.shields.io/travis/mpibpc_mroose/hx711.svg
        :target: https://travis-ci.org/mpibpc_mroose/hx711

.. image:: https://readthedocs.org/projects/hx711/badge/?version=latest
        :target: https://hx711.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mpibpc_mroose/hx711/shield.svg
     :target: https://pyup.io/repos/github/mpibpc_mroose/hx711/
     :alt: Updates


HX711
=====
This library allows to drive a HX711 on a Raspberry Pi. It just provides the capabilities:

* to set channel an gain and
* to read raw values

Example implementation:
```
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


* Free software: MIT license
* Documentation: https://hx711.readthedocs.io.



Credits
---------
I used https://github.com/gandalf15/HX711/ as base.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

