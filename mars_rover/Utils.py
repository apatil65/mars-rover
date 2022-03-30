from functools import wraps


class Try:
    """ Wraps exception handling for the incoming method

    Raises:
        Exception: Exceptions caused during the process

    Returns:
        Modified Function/Obj: Wraps try/except block to a method
    """
    @staticmethod
    def catch(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                raise
        return func_wrapper
