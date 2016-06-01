from functools import wraps


def validate_payload(func):
    @wraps(func)
    def func_wrapper(instance, payload):
        native_types = [bool, int, float, str, list, tuple, dict]
        if type(payload) not in native_types:
            raise ValueError("Invalid payload specified")
        return func(instance, payload)
    return func_wrapper


def parse_results(func):
    @wraps(func)
    def func_wrapper(instance, *args, **kwargs):
        results = func(instance, *args, **kwargs)
        if results.status_code == 200:
            return results.json()
        else:
            results.raise_for_status()
    return func_wrapper
