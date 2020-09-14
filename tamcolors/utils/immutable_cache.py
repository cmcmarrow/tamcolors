from weakref import ref


"""
Cache for immutable Objects
"""


class ImmutableCache:
    _cache_objects = {}

    def __new__(cls, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return super().__new__(cls)

        constructor_args = (*args, *[(key, kwargs[key])for key in kwargs])

        if constructor_args in cls._cache_objects:
            made_object = cls._cache_objects[constructor_args]()
            if made_object is not None:
                return made_object

        new_object = super().__new__(cls)
        setattr(new_object, "_constructor_args", constructor_args)
        weakref = ref(new_object)
        cls._cache_objects[constructor_args] = weakref

        return new_object

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __del__(self):
        if hasattr(self, "_constructor_args") and self._constructor_args in self.__class__._cache_objects:
            del self.__class__._cache_objects[self._constructor_args]
