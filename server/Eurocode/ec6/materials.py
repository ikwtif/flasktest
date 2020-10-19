from Eurocode.base.materials import BaseMaterial
from Eurocode.ec6.data import STONE_DIMENSIONS, STONE_KINDS, STONE_GROUPS, MORTAR_KINDS, MORTAR_GROUPS, \
                              STONE_WEIGHT_DENSITY, MORTAR_WEIGHT_DENSITY
from pprint import pprint


class Stone(BaseMaterial):
    """Class to representing masonry"""
    weight_density = 1900

    def __init__(self, height, width, length, kind, group, f_mean, weight_density=None):
        """
        Represents a stone for masonry

        :param height: height of the stone
        :param width: width of the stone
        :param length: length of the stone
        :param kind: kind of stone used based on component parts
        :param group: group by manufacturer based on specifications
        :param f_mean: mean compressive strength of stone cfr. manufacturer [N/mm/mm]
        :param weight_density: weight_density for stone
        :type height: int
        :type width: int
        :type length: int
        :type kind: int or str
        :type group: int or str
        :type f_mean: int
        :type weight_density: int
        """
        self._height = None
        self._width = None
        self._length = None

        self._dimensions_check(height=height, width=width, length=length)
        self.group = group
        self.kind = kind
        self.f_mean = f_mean

        if weight_density is None:
            try:
                self.weight_density = STONE_WEIGHT_DENSITY[self.kind]
            except AttributeError:
                pass

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if length is None:
            self._length = length
        else:
            raise Exception(f"dont do this")

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if self._width is None:
            self._width = width
        else:
            raise Exception(f"dont do this")

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if self._height is None:
            self._height = height
        else:
            raise Exception(f"dont do this")

    @property
    def dimension(self):
        """
        Dimensions of stone based on length/width/height
        :return: lengthxwidthxheigth
        :rtype: str
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        if dimension is None:
            pass
        elif dimension in STONE_DIMENSIONS:
            self._dimension = dimension
        else:
            raise ValueError(f'dimension - {dimension} - not possible '
                             f'\n Possible dimensions (lengthxwidthxheight): {STONE_DIMENSIONS}')

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind):
        if kind in STONE_KINDS:
            self._kind = kind
        elif isinstance(kind, int):
            self._kind = STONE_KINDS[kind]
        else:
            raise ValueError(f'kind - {kind} - not possible')

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        if group in STONE_GROUPS:
            self._group = group
        elif isinstance(group, int):
            self._group = STONE_GROUPS[group]
        else:
            raise ValueError(f'group - {group} - not possible')

    def _dimensions_check(self, width, height, length):
        """
        Verifies combination of dimensions is possible
        """
        dimension = f'{length}x{width}x{height}'
        if dimension in STONE_DIMENSIONS:
            self._dimension = dimension
            self._length = length
            self._width = width
            self._height = height
        else:
            raise ValueError('combination of dimensions not possible')

    def output(self):
        """
        :return: properties of stone
        :rtype: dict
        """
        return {'length [mm]': self.length,
                'width [mm]': self.width,
                'height [mm]': self.height,
                'dimension [mmxmmxmm]': self.dimension,
                'group': self.group,
                'kind': self.kind,
                'fmean': self.f_mean
                }


class Mortar(BaseMaterial):
    """
    Class to represent mortar for masonry
    """
    weight_density = 2300   #[N/m/m/m]

    def __init__(self, kind, group, weight_density=None, mortar_type=None):
        """
        Represents mortar for masonry

        :param kind: kind of mortar used
        :param group: group of mortar used for strength
        :param weight_density: density of mortar used
        :param mortar_type: type of mortar used based on component parts
        """
        self.kind = kind
        self.group = group
        if weight_density is None and mortar_type:
            try:
                self.weight_density = MORTAR_WEIGHT_DENSITY[mortar_type]
            except ValueError:
                pass

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind):
        if kind in MORTAR_KINDS:
            self._kind = kind
        elif isinstance(kind, int):
            self._kind = MORTAR_KINDS[kind]
        else:
            raise ValueError(f'mortel type - {kind} - not possible')

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        if isinstance(group, str):
            try:
                group = int(group)
            except ValueError:
                group = float(group)
        if group in MORTAR_GROUPS:
            self._group = group
        else:
            raise ValueError(f'mortel group - {group} - not possible')

    @property
    def strength(self):
        return self.group

    def output(self):
        """
        :return: properties of mortar
        :rtype: dict
        """
        return {'kind': self.kind,
                'group': self.group,
                'strength [kN/mm/mm]': self.strength
                }

if __name__ == '__main__':
    stone = Masonry(height=190, width=140, length=290, kind='baksteen',
                  group='groep 1', f_mean=15)
    pprint(stone.output())
    mortar = Mortar(kind='algemeen', group=12)
    pprint(mortar.output())

