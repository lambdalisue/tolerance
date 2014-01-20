# coding=utf-8
"""
tolerance utility module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


def argument_switch_generator(argument_name, default=True, reverse=False,
                              keep=False):
    """
    Create switch function which return the status from specified named argument

    Parameters
    ----------
    argument_name : string
        An argument name which is used to judge the status
    default : boolean
        A default value of this switch function.
        It is used when specifid ``**kwargs`` does not have named argument
    reverse : boolean
        Reverse the status (Default: ``False``)
    keep : boolean
        If it is ``True``, keep named argument in ``**kwargs``.

    Returns
    -------
    function
        A switch function which return status, args, and kwargs respectively.

    Examples
    --------
    >>> #
    >>> # generate switch function with default parameters
    >>> #
    >>> fn = argument_switch_generator('fail_silently')
    >>> # return `default` value and specified *args and **kwargs when
    >>> # `fail_silently` is not specified in **kwargs
    >>> fn() == (True, tuple(), {})
    True
    >>> # return `fail_silently` value when it is specified
    >>> fn(fail_silently=True) == (True, tuple(), {})
    True
    >>> fn(fail_silently=False) == (False, tuple(), {})
    True
    >>> #
    >>> # generate switch function with `default=False`
    >>> #
    >>> fn = argument_switch_generator('fail_silently', default=False)
    >>> # return `default` value so `False` is returned back
    >>> fn() == (False, tuple(), {})
    True
    >>> #
    >>> # generate switch function with `reverse=True`
    >>> #
    >>> fn = argument_switch_generator('fail_silently', reverse=True)
    >>> # `default` value is independent from `reverse=True`
    >>> fn() == (True, tuple(), {})
    True
    >>> # `fail_silently` value is influenced by `reverse=True`
    >>> fn(fail_silently=True) == (False, tuple(), {})
    True
    >>> fn(fail_silently=False) == (True, tuple(), {})
    True
    >>> #
    >>> # generate switch function with `keep=True`
    >>> #
    >>> fn = argument_switch_generator('fail_silently', keep=True)
    >>> # `fail_silently` attribute remains even in returned back kwargs
    >>> status, args, kwargs = fn(fail_silently=True)
    >>> 'fail_silently' in kwargs
    True
    """
    def switch_function(*args, **kwargs):
        if argument_name in kwargs:
            if keep:
                status = kwargs.get(argument_name)
            else:
                status = kwargs.pop(argument_name)
            if reverse:
                status = not status
        else:
            status = default
        return bool(status), args, kwargs
    return switch_function


if __name__ == '__main__':
    import doctest; doctest.testmod()
