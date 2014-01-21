# coding=utf-8
"""
tolerance decorator module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import sys
from tolerance.utils import argument_switch_generator
from tolerance.functional import wraps


DEFAULT_TOLERATE_SWITCH = argument_switch_generator('fail_silently')
"""Default tolerate switch function"""


def tolerate(substitute=None, exceptions=None,
             switch=DEFAULT_TOLERATE_SWITCH):
    """
    A function decorator which makes a function fail silently

    To disable fail silently in a decorated function, specify
    ``fail_silently=False``.
    To disable fail silenlty in decorated functions globally, specify
    ``tolerate.disabled``.

    Parameters
    ----------
    fn : function
        A function which will be decorated.
    substitute : function or returning value
        A function used instead of :attr:`fn` or returning value
        when :attr:`fn` failed.
    exceptions : list of exceptions or None
        A list of exception classes or None. 
        If exceptions is specified, ignore exceptions only listed in this
        parameter and raise exception if the exception is not listed.
    switch : string, list/tuple, dict, function or None
        A switch function which determine whether silent the function failar.
        The function receive ``*args`` and ``**kwargs`` which will specified
        to :attr:`fn` and should return status (bool), args, and kwargs.
        If the function return ``False`` then agggressive decorated function
        worked as normal function (raise exception when there is exception).
        Default switch function is generated by
        :func:`argument_switch_generator` with
        ``argument_switch_generator('fail_silently')``
        so if ``fail_silently=False`` is specified to the function, the function
        works as noramlly.  
        
        **From Version 0.1.1**, when switch is specified as non functional value,
        :func:`argument_switch_generator` will be called with switch as
        arguments.
        If string is specified, the switch generator will be called as
        ``argument_switch_generator(switch)``.
        If list or tuple is specified, the switch generator will be called as
        ``argument_switch_generator(*switch)``.
        If dict is specified, the switch generator will be called as
        ``argument_switch_generator(**switch)``.


    Returns
    -------
    function
        A decorated function
        
    Examples
    --------
    >>> #
    >>> # use tolerate as a function wrapper
    >>> #
    >>> parse_int = tolerate()(int)
    >>> parse_int(0)
    0
    >>> parse_int("0")
    0
    >>> parse_int("zero") is None
    True
    >>> #
    >>> # use tolerate as a function decorator (PIP-318)
    >>> #
    >>> @tolerate(lambda x: x)
    ... def prefer_int(x):
    ...     return int(x)
    >>> prefer_int(0)
    0
    >>> prefer_int("0")
    0
    >>> prefer_int("zero")
    'zero'
    >>> #
    >>> # filter exceptions be ignored
    >>> #
    >>> @tolerate(exceptions=(KeyError, ValueError))
    ... def force_int(x):
    ...     string_numbers = {
    ...         'zero': 0,
    ...         'one': 1,
    ...         'two': 2,
    ...         'three': 3,
    ...         'four': 4,
    ...         'five': 5,
    ...         'six': 6,
    ...         'seven': 7,
    ...         'eight': 8,
    ...         'nine': 9
    ...     }
    ...     if isinstance(x, (int, float)):
    ...         return int(x)
    ...     elif isinstance(x, str):
    ...         if x in string_numbers:
    ...             return string_numbers[x]
    ...         elif x in ('ten', 'hundred', 'thousand'):
    ...             raise KeyError
    ...         raise ValueError
    ...     else:
    ...         raise AttributeError
    >>> force_int('zero')
    0
    >>> force_int('ten') is None    # KeyError
    True
    >>> force_int('foo') is None    # ValueError
    True
    >>> force_int(object)           # AttributeError
    Traceback (most recent call last):
        ...
    AttributeError
    >>> #
    >>> # disable tolerance by passing `fail_silently=False`
    >>> #
    >>> force_int('ten', fail_silently=False)   # KeyError
    Traceback (most recent call last):
        ...
    KeyError
    >>> #
    >>> # disable tolerance globally by setting `tolerate.disabled=True`
    >>> #
    >>> tolerate.disabled = True
    >>> force_int('foo')    # ValueError
    Traceback (most recent call last):
        ...
    ValueError
    >>> tolerate.disabled = False   # rollback
    >>> #
    >>> # Features from Version 0.1.1
    >>> # 
    >>> # specify switch as a string
    >>> parse_int_string = tolerate(switch='patient')(int)
    >>> parse_int_string('zero') is None
    True
    >>> parse_int_string('zero', patient=False)
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> # specify switch as a list
    >>> parse_int_list = tolerate(switch=['fail_silently', False])(int)
    >>> parse_int_list('zero')
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> parse_int_string('zero', fail_silently=True) is None
    True
    >>> # specify switch as a dict
    >>> parse_int_dict = tolerate(switch={'argument_name': 'aggressive',
    ...                                   'reverse': True})(int)
    >>> parse_int_dict('zero') is None
    True
    >>> parse_int_dict('zero', aggressive=False) is None
    True
    >>> parse_int_dict('zero', aggressive=True) is None
    Traceback (most recent call last):
        ...
    ValueError: ...
    """
    if switch:
        # create argument switch if switch is string or list or dict
        if isinstance(switch, basestring):
            switch = argument_switch_generator(switch)
        elif isinstance(switch, (list, tuple)):
            switch = argument_switch_generator(*switch)
        elif isinstance(switch, dict):
            switch = argument_switch_generator(**switch)
    # callable alternative because callable is removed in python 3
    is_callable = lambda x: hasattr(x, '__call__')
    def decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            if getattr(tolerate, 'disabled', False):
                # the function has disabled so call normally.
                return fn(*args, **kwargs)
            if switch is not None:
                status, args, kwargs = switch(*args, **kwargs)
                if not status:
                    # the switch function return `False` so call noramlly.
                    return fn(*args, **kwargs)
            try:
                return fn(*args, **kwargs)
            except:
                e = sys.exc_info()[1]
                if exceptions is None or e.__class__ in exceptions:
                    if is_callable(substitute):
                        return substitute(*args, **kwargs)
                    return substitute
                raise e
        return inner
    return decorator

if __name__ == '__main__':
    import doctest; doctest.testmod()
