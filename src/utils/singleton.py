class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls is Singleton:
            raise NotImplementedError(
                "Singleton is an abstract class that cannot be instantiated directly!"
            )
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]



class Singleton(metaclass=SingletonMeta):
    """
        /!\\ Never call super() in unherited object /!\\

    This object is an abstract parent to define a singleton Object by unheritance.
    Singleton: Allows developper to create object than cannot be re-instanciated
               If tried to re-instanciate it, it returns the current instanciated object instead.
    This object is not intended to be directly instanciated and will raise an Error if it is tried.
    """
    @classmethod
    def reset(cls):
        return cls._instances.pop(cls, None) is not None
