from functools import wraps

UNIT_PREFIXES = {
        'G': 1e+09,
        'M': 1e+06,
        'k': 1e+03,
        'none': 1,
        'c': 1e-02,
        'm': 1e-03,
        }


def transform_value(value, prefix='k'):
    if prefix not in UNIT_PREFIXES:
        raise ValueError
    factor = UNIT_PREFIXES[prefix]
    return factor * value


def transform_units(prefix='k'):

    def decorator(func):
        @wraps(func)
        def transform(*args, **kwargs):
            value = func(*args, **kwargs)
            return transform_value(value, prefix)

        return transform
    return decorator



