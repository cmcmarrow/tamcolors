# built in library
import inspect

# Charles McMarrow

"""
tools to check if the right data has been given
tools will return True if data is valid
tools will raise error if data is not valid
"""


class ChecksError(Exception):
    pass


def range_check(number,
                min_number=None,
                max_number=None,
                error=ChecksError):
    """
    info: True if number in range Exception if not
    :param number: int: number in range
    :param min_number: None, int: min of range
    :param max_number: None, int: max of range
    :param error: Exception
    :return: True
    """
    if not isinstance(number, int):
        raise error("{0} is out of range".format(repr(number)))

    if min_number is not None:
        if min_number > number:
            raise error("{0} is out of range".format(repr(number)))

    if max_number is not None:
        if number >= max_number:
            raise error("{0} is out of range".format(repr(number)))

    return True


def char_check(char,
               error=ChecksError):
    """
    info: True if Char Exception if not Char
    :param char: str: len of 1
    :param error: Exception
    :return: True
    """
    if isinstance(char, str):
        if len(char) == 1:
            return True

    raise error("{0} is not a char".format(repr(char)))


def function_check(function,
                   parameter_count,
                   args,
                   kwargs,
                   error=ChecksError):
    """
    info: True if faction with right requirements Exception if not
    :param function: function
    :param parameter_count: 0 - inf
    :param args: bool or None
    :param kwargs: bool or None
    :param error: Exception
    :return: True
    """
    if not callable(function):
        raise error("{0} does not meet function requirements".format(repr(function)))

    function_details = inspect.getfullargspec(function)

    if len(function_details.args) != parameter_count:
        raise error("{0} does not meet function requirements. args most be {1}".format(repr(function),
                                                                                       parameter_count))

    varargs_tf = function_details.varargs is not None
    if varargs_tf != args is not None:
        raise error("{0} does not meet function requirements. varargs most be {1}".format(repr(function),
                                                                                          args))
    varkw_tf = function_details.varkw is not None
    if varkw_tf != kwargs is not None:
        raise error("{0} does not meet function requirements. kwargs most be {1}".format(repr(function),
                                                                                         kwargs))

    return True


def list_key_check(list_of_dicts,
                   keys,
                   error=ChecksError):
    """
    info: True if list_of_dicts has the keys need it Exception if not
    :param list_of_dicts: list: [dict, ...]
    :param keys: list: [str, ...]
    :param error: Exception
    :return: True
    """
    if not isinstance(list_of_dicts, list):
        raise error("list of dicts does not meet requirements")

    for item in list_of_dicts:
        if not isinstance(item, dict):
            raise error("list of dicts does not meet requirements")
        for key in keys:
            if key not in item:
                raise error("list of dicts does not meet requirements")

    return True


def type_check(a_object,
               a_type,
               error=ChecksError):
    """
    info: True if a_object is instance of a_type Exception if not
    :param a_object: object
    :param a_type: type
    :param error: Exception
    :return: True
    """
    if isinstance(a_object, a_type):
        return True
    raise error("{0} is not a instance of {1}".format(repr(a_object), repr(a_type)))


def item_in_object(item,
                   a_object,
                   error=ChecksError):
    """
    info: True if item in a_object Exception if not
    :param item: object
    :param a_object: object
    :param error: Exception
    :return: True
    """
    if item in a_object:
        return True
    raise error("{0} is not in {1}".format(repr(item), repr(a_object)))


def instance_check(a_object,
                   instance,
                   error=ChecksError):
    """
    info: True if a_object isinstance of instance Exception if not
    :param a_object: object
    :param instance: object
    :param error: Exception
    :return: True
    """
    if isinstance(a_object, instance):
        return True
    raise error("{0} is not an instance of {1}".format(repr(a_object), repr(instance)))


def in_instances_check(a_object,
                       instances,
                       error=ChecksError):
    """
    info: True if a_object is a isinstance of at lest one of the instances Exception if not
    :param a_object: object
    :param instances: list, tuple
    :param error: Exception
    :return: True
    """

    for instance in instances:
        if isinstance(a_object, instance):
            return True
    raise error("{0} is not in the list of instances {1}".format(repr(a_object), repr(instances)))


def single_block_char_check(char,
                            error=ChecksError):
    """
    info: True if Char Exception if not Char
    :param char: str: len of 1
    :param error: Exception
    :return: True
    """
    if isinstance(char, str):
        if len(char) == 1 and char not in ("\t", "\n", "\r", "\v", "\f"):
            return True

    raise error("{0} is not a single char block".format(repr(char)))


def has_method_check(a_object,
                     method,
                     error=ChecksError):

    if hasattr(a_object, method):
        return True

    raise error("{0} is not a method of {1}".format(a_object, method))


def is_equal_check(object1,
                   object2,
                   error=ChecksError):
    """
    info: sees if two object is equal to each other
    :param object1: object
    :param object2: object
    :param error: Exception
    :return: True
    """
    if object1 == object2:
        return True

    raise error("{0} is not equal to {1}".format(object1, object2))


def any_check(*args, error=ChecksError):
    """
    info: see if any of the args are True
    :param args: list: list of Objects
    :param error: Exception
    :return: True
    """
    ret = any(args)
    if ret:
        return True

    raise error("{0} none are True".format(args))


def is_function_check(function,  error=ChecksError):
    """
    info: checks if function is a callable
    :param function: function
    :param error: Exception
    :return: True
    """

    if not callable(function):
        raise error("{0} is not a function".format(repr(function)))
    return True


def is_json(data, allowed_types=None, error=ChecksError):
    """
    info: checks if data is json and is a allowed type
    :param data: object
    :param allowed_types: list or None or class: [list, dict, ...]
    :param error: Exception
    :return: True
    """
    json_classes = {int, float, bool, type(None), dict, list, tuple, str}

    if allowed_types is None:
        if type(data) not in json_classes:
            raise error("{0} can not be made into json".format(data))
    elif type(allowed_types) in {list, tuple, set}:
        if type(data) not in json_classes or type(data) not in allowed_types:
            raise error("{0} can not be made into json".format(data))
    elif type(allowed_types) == type:
        if type(data) not in json_classes or type(data) != allowed_types:
            raise error("{0} can not be made into json".format(data))
    else:
        raise error("Bad allowed_types={0}".format(allowed_types))

    if type(data) == dict:
        for key in data:
            if type(key) != str:
                raise error("key must be str but got {0}".format(type(key)))
            is_json(data[key], None, error)
    elif type(data) in {list, tuple}:
        for item in data:
            is_json(item, None, error)

    return True
