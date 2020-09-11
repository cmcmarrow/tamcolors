from weakref import ref


class Cache:
    objects = {}
    objects_keys = iter({})

    def __new__(cls, *args, **kwargs):
        constructor_args = (cls, *args, *[(key, kwargs[key])for key in kwargs])

        if constructor_args in cls.objects:
            made_object = cls.objects[constructor_args]()
            if made_object is not None:
                return made_object

        new_object = super().__new__(cls)
        weakref = ref(new_object)
        cls.objects[constructor_args] = weakref

        try:
            for _ in range(2):
                key = next(cls.objects_keys)
                if key in cls.objects_keys and cls.objects[key]() is None:
                    del cls.objects[key]
        except StopIteration:
            cls.objects_keys = iter(tuple(cls.objects))

        return new_object

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self
