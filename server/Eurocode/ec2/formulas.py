


def v_factor(fck):
    """
    NBN EN 1992-1-1:2005 - (6.6N)

    sterktereductiefactor voor beton, gescheurd door dwarskracht.

    :param fck:
    :return:
    """

    return 0.6 * (1 - fck / 250)