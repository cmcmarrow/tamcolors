import json
import zlib


class ObjectJsonError(Exception):
    pass


def loads(data, classes=None, encoding="utf-8", decompress=True):
    if classes is None:
        classes = ()
    classes = {c.__name__: c for c in classes}

    if decompress:
        data = zlib.decompress(data)
    data = str(data, encoding=encoding)

    return _loads(json.loads(data), classes)


def _loads(data, classes):
    if data[0] in ("None", "int", "float", "str", "bool"):
        return data[1]
    elif data[0] in classes:
        c = classes[data[0]]
        c = c.__new__(c)

        c_dict = dict([[_loads(key, classes), _loads(obj, classes)] for key, obj in data[1]])
        for key in c_dict:
            c.__dict__[key] = c_dict[key]

        c_slots = dict([[_loads(key, classes), _loads(obj, classes)] for key, obj in data[2]])
        for key in c_slots:
            setattr(c, key, c_slots[key])
        return c
    elif data[0] == "tuple":
        return tuple([_loads(obj, classes) for obj in data[1]])
    elif data[0] == "list":
        return [_loads(obj, classes) for obj in data[1]]
    elif data[0] == "set":
        return set([_loads(obj, classes) for obj in data[1]])
    elif data[0] == "dict":
        return dict([[_loads(key, classes), _loads(obj, classes)] for key, obj in data[1]])
    raise ObjectJsonError("Can not load {}".format(data.__class__.__name__))


def dumps(data, classes=None, encoding="utf-8", compress=True):
    if classes is None:
        classes = ()

    ret = json.dumps(_dumps(data, classes)).encode(encoding)

    if compress:
        ret = zlib.compress(ret)

    return ret


def _dumps(data, classes):
    if classes is None:
        classes = ()

    if data is None:
        return "None", data
    elif type(data) in (str, float, int, bool):
        return data.__class__.__name__, data
    elif type(data) in classes:
        name, obj_dict, obj_slots = data.__class__.__name__, [], []
        if hasattr(data, "__dict__"):
            obj_dict = [[_dumps(obj, classes), _dumps(data.__dict__[obj], classes)] for obj in data.__dict__]
        if hasattr(data, "__slots__"):
            obj_slots = [[_dumps(obj, classes), _dumps(getattr(data, obj), classes)] for obj in data.__slots__]
        return data.__class__.__name__, obj_dict, obj_slots
    elif type(data) in (tuple, list, set):
        return data.__class__.__name__, [_dumps(obj, classes) for obj in data]
    elif type(data) == dict:
        return "dict", [[_dumps(obj, classes), _dumps(data[obj], classes)] for obj in data]

    raise ObjectJsonError("Can not dump {}".format(data.__class__.__name__))
