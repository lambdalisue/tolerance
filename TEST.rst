How to run the tests
=====================
1.  Install requirement packages with ``requirements-test.txt``::

        $ pip install -r requirements-test

2.  Run tests with ``nosetests`` command provided by nose_ (it is automatically
    installed via ``requirements-test.txt``)

        $ nosetests

All configuration for running tests can be found at ``[nosetests]`` section of
``setup.cfg`` file.

.. _nose: https://nose.readthedocs.org/en/latest/index.html
