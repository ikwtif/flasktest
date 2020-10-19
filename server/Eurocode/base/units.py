from functools import wraps

UNIT_PREFIXES = {
        'G': 1e+09,
        'M': 1e+06,
        'k': 1e+03,
        'h': 1e+02,
        'da': 1e+01,
        'none': 1,
        'd': 1e-01,
        'c': 1e-02,
        'm': 1e-03,
        }

def transform_value(quantity, prefix='M', inverse=False):
    """Transform the value of a physical quantity expressed
    in enginnering units (e.g. ``MPa``) in the fundamental
    units of the metric system (e.g. ``kg``, ``m``, ``s``).

    :param quantity: A numerical value to transform.
    :type quantity: float or int
    :param str prefix: The unit prefix that the value is
        expressed in.
    :param bool inverse: If `True` transform a value
        expressed in fundamental units in the engineering
        form implied by the ``prefix``.
    :rtype: float or callable
    """
    if prefix not in UNIT_PREFIXES:
        raise UnrecognizedUnitPrefix(1014, f'{prefix}')

    factor = UNIT_PREFIXES[prefix]
    if inverse:
        factor = 1 / factor
    #check_numerical_value(quantity)
    return factor * quantity


def inverse_transform_value(quantity, prefix='M'):
    """Wrap the ``transform_value`` function so that
    it returns the inverse transform of the quantity,
    from its representation in fundamental units, to
    a representation in engineering units.

    :param quantity: A numerical value to transform.
    :type quantity: float or int
    :param str prefix: The unit prefix that the value is
        expressed in.
    :rtype: float
    """
    return transform_value(quantity, prefix, inverse=True)


def transform_units(prefix='M', inverse=False):

    def decorator(method):

        @wraps(method)
        def transformer(*args, **kwargs):
            value = method(*args, **kwargs)
            return transform_value(value, prefix, inverse)

        return transformer

    return decorator
