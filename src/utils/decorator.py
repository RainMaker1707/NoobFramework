from functools import wraps


def allow_batch(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Case multiple: through dictionnary -> func({'p1': panel1, 'p2': panel2})
        if args and isinstance(args[0], dict):
            for name, value in args[0].items():
                func(self, value, string=name)
            return True
        if args and isinstance(args[0], list):
            for e in args[0]:
                if e.string:
                    func(self, e, string=e.string)
                else: 
                    func(self, e)
            return True
        # Case 3: Classic uniq call -> func(arg1, arg2)
        return func(self, *args, **kwargs)
    return wrapper
