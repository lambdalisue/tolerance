#!/usr/bin/env nosetests -v
# coding=utf-8
"""
A unit test module of ``tolerance.utils``
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import inspect
from nose.tools import *
from tolerance.utils import argument_switch_generator


def test_argument_switch_generator_specification():
    """
    argument_switch_generator specification
    """
    args, varargs, keywords, defaults = \
        inspect.getargspec(argument_switch_generator)

    eq_(args, ['argument_name', 'default', 'reverse', 'keep'])
    eq_(varargs, None)
    eq_(keywords, None)
    eq_(defaults, (None, True, False, False))

def test_argument_switch_generator_return_function():
    """
    argument_switch_generator return a function
    """
    fn = argument_switch_generator('fail_silently')
    ok_(inspect.isfunction(fn), 'Return value is not a function')

    # version 0.1.1
    fn2 = argument_switch_generator()
    ok_(inspect.isfunction(fn2), 'Return value is not a function')

def test_argument_swith_generators_fn_return_three_item_tuple():
    """
    argument_switch_generator's fn return three item tuple
    """
    fn = argument_switch_generator('fail_silently')
    results = fn()

    ok_(isinstance(results, tuple), 'fn return value is not a tuple')

def test_argument_swith_generators_fn_return_status_args_kwargs_tuple():
    """
    argument_switch_generator's fn return 'status, args, kwargs' tuple
    """
    fn = argument_switch_generator('fail_silently')
    results = fn()
    ok_(len(results) == 3, 'fn return value does not have three items')
    ok_(isinstance(results[0], bool), '1st item is not a boolean')
    ok_(isinstance(results[1], (list, tuple)), '2nd item is not a list/tuple')
    ok_(isinstance(results[2], dict), '3rd item is not a dict')

def test_argument_swith_generators_fn_return_default_status():
    """
    argument_switch_generator's fn return default status
    """
    fn = argument_switch_generator('fail_silently')
    status, args, kwargs = fn()
    ok_(status == True)
    fn = argument_switch_generator('fail_silently', default=False)
    status, args, kwargs = fn()
    ok_(status == False)

def test_argument_swith_generators_fn_return_default_independent_from_reverse():
    """
    argument_switch_generator's fn return status judged by kwargs
    """
    fn = argument_switch_generator('fail_silently')
    status, args, kwargs = fn()
    ok_(status == True)
    fn = argument_switch_generator('fail_silently', default=False)
    status, args, kwargs = fn()
    ok_(status == False)

def test_argument_swith_generators_fn_return_status_judged_by_kwargs():
    """
    argument_switch_generator's fn return status judged by kwargs
    """
    fn = argument_switch_generator('fail_silently')
    status, args, kwargs = fn(fail_silently=False)
    ok_(status == False)
    status, args, kwargs = fn(fail_silently=True)
    ok_(status == True)

def test_argument_swith_generators_fn_return_status_judged_by_kwargs_depends_on_reverse():
    """
    argument_switch_generator's fn return status judge depends on reverse
    """
    fn = argument_switch_generator('fail_silently', reverse=True)
    status, args, kwargs = fn(fail_silently=False)
    ok_(status == True)
    status, args, kwargs = fn(fail_silently=True)
    ok_(status == False)

def test_argument_swith_generators_fn_remove_named_argument():
    """
    argument_switch_generator's fn remove named argument
    """
    fn = argument_switch_generator('fail_silently')
    status, args, kwargs = fn(fail_silently=False)

    ok_('fail_silently' not in kwargs)

def test_argument_swith_generators_fn_keep_named_argument():
    """
    argument_switch_generator's fn keep named argument
    """
    fn = argument_switch_generator('fail_silently', keep=True)
    status, args, kwargs = fn(fail_silently=False)

    ok_('fail_silently' in kwargs)

def test_argument_swith_generators_fn_does_not_treat_args():
    """
    argument_switch_generator's fn does not treat args
    """
    fn = argument_switch_generator('fail_silently')
    args1 = ['a', 'b', 'c', 0, 1, 2, True, False, None]
    # the following simple code fail with python 2.5
    #status, args2, kwargs = fn(*args1, fail_silently=False)
    status, args2, kwargs = fn(*args1, **{'fail_silently': False})

    eq_(list(args1), list(args2))

def test_argument_swith_generators_fn_does_not_treat_kwargs():
    """
    argument_switch_generator's fn does not treat kwargs
    """
    fn = argument_switch_generator('fail_silently')
    kwargs1 = {
        'a': 'a',
        'b': 'b',
        'c': 'c',
    }
    status, args, kwargs2 = fn(**kwargs1)

    eq_(kwargs1, kwargs2)
