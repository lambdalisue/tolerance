tolerance
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/tolerance.png?branch=master
    :target: http://travis-ci.org/lambdalisue/tolerance
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/tolerance/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/tolerance/
    :alt: Coverage

.. image:: https://pypip.in/d/tolerance/badge.png
    :target: https://pypi.python.org/pypi/tolerance/
    :alt: Downloads

.. image:: https://pypip.in/v/tolerance/badge.png
    :target: https://pypi.python.org/pypi/tolerance/
    :alt: Latest version

.. image:: https://pypip.in/wheel/tolerance/badge.png
    :target: https://pypi.python.org/pypi/tolerance/
    :alt: Wheel Status

.. image:: https://pypip.in/egg/tolerance/badge.png
    :target: https://pypi.python.org/pypi/tolerance/
    :alt: Egg Status

.. image:: https://pypip.in/license/tolerance/badge.png
    :target: https://pypi.python.org/pypi/tolerance/
    :alt: License

Do you often write the fail silent codes like below?

.. code-block:: python

    try:
        # do what ever you need...
        return "foo"
    except:
        # fail silently
        return ""

This kind of codes are often found in Django_ projects or programs which should
not raise any exceptions in product mode.

**tolerance** is a function decorator to make a tolerant function; a function
which does not raise any exceptions even there are exceptions.
This concept is quite useful for making stable product or ``prefer_int`` types
of code described in Usage section.

.. _Django: https://www.djangoproject.com/

Check
`online documentation <http://python-tolerance.readthedocs.org/en/latest/>`_
for more details.

Features
--------

+   Convert a function to a tolerant function
+   The decorated function returns ``substitute`` (Default is ``None``) when it
    is not callable.
    The function returns a "returned value" from ``substitute`` function when
    it is callable.
+   Ignoreing exceptions can be specified as a exception class list with
    ``exceptions`` argument.
+   When ``fail_silently=False`` is passed to the decorated function,
    the function does not ignore exceptions (the argument name can be changed
    with making switch function via ``argument_switch_generator`` function).

Installation
------------
Use pip_ like::

    $ pip install tolerance

.. _pip: https://pypi.python.org/pypi/pip

Usage
-----
Assume that you need a function which convert a string to an integer when it is
possible.
Without tolerance, you need to write a code like below

.. code-block:: python

    >>> # without tolerance
    >>> def prefer_int_withot_tolerance(x):
    ...     try:
    ...         return int(x)
    ...     except:
    ...         # fail silently
    ...         return x
    >>> prefer_int_withot_tolerance(0)
    0
    >>> prefer_int_withot_tolerance('0')
    0
    >>> prefer_int_withot_tolerance('zero')
    'zero'

However, with tolerance, you just need to write a single line code like

.. code-block:: python

    >>> from tolerance import tolerate
    >>> prefer_int = tolerate(lambda x: x)(int)
    >>> prefer_int(0)
    0
    >>> prefer_int('0')
    0
    >>> prefer_int('zero')
    'zero'

Or you can use ``tolerate`` as a function decorator described in PEP-318_

.. code-block:: python

    >>> from tolerance import tolerate
    >>> @tolerate(lambda x: x)
    ... def prefer_int_318(x):
    ...     return int(x)
    >>> prefer_int_318(0)
    0
    >>> prefer_int_318('0')
    0
    >>> prefer_int_318('zero')
    'zero'

The example codes above  specify ``substitute`` argument of ``tolerate``
function to specify the returning value when the function has failed (
``lambda x: x`` part).
``tolerate`` function takes several arguments to configure the function
behavior.
These arguments are explained in Case study and detailed in API documentation.

.. _PEP-318: http://www.python.org/dev/peps/pep-0318/

Change log
----------
Version 0.1.0
    + Initial development
    + Manually tested with Python 2.4, 2.5, 2.7, 3.2, 3.3
Version 0.1.1
    + ``switch`` shortcut feature is added
    + Drop off supporting Python 2.4 and 2.5
    + Support Python 3.2 and 3.3 via 2to3
    + Use tox_ for testing

.. _tox: http://tox.readthedocs.org/en/latest/index.html

Case study
----------

Q. How can I return the default value when the function fail?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``substitute`` argument to specify the default value like

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> @tolerate(substitute='foo')
    ... def raise_exception():
    ...     raise Exception
    >>> raise_exception()
    'foo'

Q. How can I change the default value depends on passed arguments?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Specify ``substitute`` argument as a function

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> def substitute_function(*args, **kwargs):
    ...     # do what ever you need, this example simply return 1st argument
    ...     return args[0]
    >>> @tolerate(substitute=substitute_function)
    ... def raise_exception(*args):
    ...     raise Exception
    >>> raise_exception('bar', 'hoge')
    'bar'

Q. How can I make the function to ignore only several exceptions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``exceptions`` argument to specify exceptions which will be ignored.

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> exceptions_ignored = (
    ...     AttributeError,
    ...     ValueError,
    ... )
    >>> @tolerate(exceptions=exceptions_ignored)
    ... def raise_exception(x):
    ...     if x == 0:
    ...         raise AttributeError
    ...     elif x == 1:
    ...         raise ValueError
    ...     else:
    ...         raise KeyError
    >>> raise_exception(0) is None
    True
    >>> raise_exception(1) is None
    True
    >>> raise_exception(2)
    Traceback (most recent call last):
        ...
    KeyError

Q. How can I disable ignoreing exceptions in the decorated function?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Pass ``fail_silently=False`` to the decorated function.

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> @tolerate()
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> raise_exception(fail_silently=False)
    Traceback (most recent call last):
        ...
    KeyError

You can change the attribute name with specifing new switch function.
It will be explained below.

Q. How can I disable ignoreing exceptions globally?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Set ``tolerate.disabled = True`` to disable tolerance globally.

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> @tolerate()
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> tolerate.disabled = True
    >>> raise_exception()
    Traceback (most recent call last):
        ...
    KeyError
    >>> # rollback
    >>> tolerate.disabled = False

Q. How can I disable ignoreing exceptions in complex mannar?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``switch`` argument to specify switch function.

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> DEBUG = False
    >>> def switch_function(*args, **kwargs):
    ...     # do what ever you need, this sample check kwargs and DEBUG
    ...     # remove 'fail_silently' attribute and store
    ...     fail_silently = kwargs.pop('fail_silently', True)
    ...     if DEBUG or not fail_silently:
    ...         # do not ignore exceptions. note that kwargs which does not
    ...         # have 'fail_silently' is returned back.
    ...         return False, args, kwargs
    ...     # do ignore exceptions. note that kwargs which does not have
    ...     # 'fail_silently' is returned back.
    ...     return True, args, kwargs
    >>> @tolerate(switch=switch_function)
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> raise_exception(fail_silently=False)
    Traceback (most recent call last):
        ...
    KeyError
    >>> DEBUG = True
    >>> raise_exception()
    Traceback (most recent call last):
        ...
    KeyError

Q. I just want to change the attribute name, making switch function is too complicated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``argument_switch_generator`` to make switch function.

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> from tolerance import argument_switch_generator
    >>> switch_function = argument_switch_generator('quiet')
    >>> @tolerate(switch=switch_function)
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> # you can use `quiet=False` instead of `fail_silently`
    >>> raise_exception(quiet=False)
    Traceback (most recent call last):
        ...
    KeyError
    >>> # raise_exception does not know fail_silently so ignore
    >>> raise_exception(fail_silently=False) is None
    True
    >>> #
    >>> # From Version 0.1.1
    >>> #
    >>> @tolerate(switch='quiet')
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> raise_exception(quiet=False)
    Traceback (most recent call last):
        ...
    KeyError
    >>> raise_exception(fail_silently=False) is None
    True

.. note::
    From Version 0.1.1, you can simply specify the argument name to ``switch``
    argument and then  ``tolerant`` function will call
    ``argument_switch_generator`` internally with the specified name.

    See detailed informations on API documentation

Q. I want to make the function ignoreing exceptions only when ``fail_silently=True`` is passed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``default`` argument to tell ``argument_switch_generator`` function

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> from tolerance import argument_switch_generator
    >>> switch_function = argument_switch_generator('fail_silently', default=False)
    >>> @tolerate(switch=switch_function)
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    Traceback (most recent call last):
        ...
    KeyError
    >>> raise_exception(fail_silently=True) is None
    True
    >>> #
    >>> # From Version 0.1.1
    >>> #
    >>> @tolerate(switch=[None, False])
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    Traceback (most recent call last):
        ...
    KeyError
    >>> @tolerate(switch={'default': False})
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    Traceback (most recent call last):
        ...
    KeyError

.. note::
    From Version 0.1.1, you can simply specify ``*args`` or ``**kwargs`` of
    ``argument_switch_generator`` to ``switch`` argument and ``tolerant``
    function will call ``argument_switch_generator`` internally with the
    specified arguments.

    See detailed informations on API documentation

Q. I want to disable the ignoreing exceptions when ``verbose=False`` is passed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``reverse`` argument to tell ``argument_switch_generator`` function

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> from tolerance import argument_switch_generator
    >>> switch_function = argument_switch_generator('verbose', reverse=True)
    >>> @tolerate(switch=switch_function)
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> raise_exception(verbose=True)
    Traceback (most recent call last):
        ...
    KeyError
    >>> #
    >>> # From Version 0.1.1
    >>> #
    >>> @tolerate(switch={'argument_name': 'verbose', 'reverse': True})
    ... def raise_exception():
    ...     raise KeyError
    >>> raise_exception() is None
    True
    >>> raise_exception(verbose=True)
    Traceback (most recent call last):
        ...
    KeyError

Q. I want to use ``fail_silently`` argument even in decorated function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A. Use ``keep`` argument to tell ``argument_switch_generator`` function

.. code-block:: python
    
    >>> from tolerance import tolerate
    >>> from tolerance import argument_switch_generator
    >>> switch_function = argument_switch_generator('fail_silently', keep=True)
    >>> @tolerate(switch=switch_function)
    ... def raise_exception(**kwargs):
    ...     if 'fail_silently' in kwargs:
    ...         raise KeyError
    ...     return 'Failed!'
    >>> raise_exception(fail_silently=True) is None
    True
    >>> raise_exception(fail_silently=False)
    Traceback (most recent call last):
        ...
    KeyError
    >>> #
    >>> # From Version 0.1.1
    >>> #
    >>> @tolerate(switch={'keep': True})
    ... def raise_exception(**kwargs):
    ...     if 'fail_silently' in kwargs:
    ...         raise KeyError
    ...     return 'Failed!'
    >>> raise_exception(fail_silently=True) is None
    True
    >>> raise_exception(fail_silently=False)
    Traceback (most recent call last):
        ...
    KeyError
