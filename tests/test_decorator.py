#!/usr/bin/env nosetests -v
# coding=utf-8
"""
A unit test module of ``tolerance.decorators``
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import inspect
from nose.tools import *
from tolerance.decorators import tolerate
from tolerance.decorators import DEFAULT_TOLERATE_SWITCH


def test_tolerate_specification():
    """
    tolerance specification
    """
    args, varargs, keywords, defaults = \
        inspect.getargspec(tolerate)

    eq_(args, ['substitute', 'exceptions', 'switch'])
    eq_(varargs, None)
    eq_(keywords, None)
    eq_(defaults, (None, None, DEFAULT_TOLERATE_SWITCH))

def test_tolerate_return_function_decorator():
    """
    tolerance return function decorator (function which take one argument)
    """
    decorator = tolerate()
    ok_(inspect.isfunction(decorator))

    args, varargs, keywords, defaults = inspect.getargspec(decorator)
    eq_(len(args), 1, 'Return function should take one argument for function')

def test_tolerate_decorated_function_return_value():
    """
    tolerance decorated function return value
    """
    def test_function():
        return "foobar"
    fn = tolerate()(test_function)
    eq_(fn(), "foobar")

def test_tolerate_decorated_function_fail_silently():
    """
    tolerance decorated function fail silently
    """
    def test_function():
        raise Exception()
    fn = tolerate()(test_function)
    fn()

def test_tolerate_decorated_function_return_substitute_when_fail():
    """
    tolerance decorated function return substitute when fail
    """
    def test_function():
        raise Exception()
    fn = tolerate(substitute='foobar')(test_function)
    eq_(fn(), "foobar")

def test_tolerate_decorated_function_call_substitute_when_fail():
    """
    tolerance decorated function call substitute when fail
    """
    def test_function():
        raise Exception()
    def test_substitute(*args, **kwargs):
        return "foobar"
    fn = tolerate(substitute=test_substitute)(test_function)
    eq_(fn(), "foobar")

def test_tolerate_decorated_function_fail_silently_if_exception_is_found():
    """
    tolerance decorated function fail silently if exception is found in exceptions
    """
    def test_function():
        raise AttributeError()
    fn = tolerate(exceptions=[AttributeError])(test_function)
    fn()

@raises(AttributeError)
def test_tolerate_decorated_function_raise_if_exception_is_not_found():
    """
    tolerance decorated function raise if exception is not found in exceptions
    """
    def test_function():
        raise AttributeError()
    fn = tolerate(exceptions=[KeyError])(test_function)
    fn()

@raises(AttributeError)
def test_tolerate_decorated_function_raise_if_switch_fail():
    """
    tolerance decorated function raise if switch fail
    """
    def test_function():
        raise AttributeError()
    def test_switch(*args, **kwargs):
        return False, args, kwargs
    fn = tolerate(switch=test_switch)(test_function)
    fn()

@raises(AttributeError)
@with_setup(teardown=lambda : setattr(tolerate, 'disabled', False))
def test_tolerate_decorated_function_raise_if_disabled():
    """
    tolerance decorated function raise if disabled
    """
    def test_function():
        raise AttributeError()
    fn = tolerate()(test_function)
    # disable
    tolerate.disabled = True
    fn()
