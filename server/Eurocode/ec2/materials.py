
from Eurocode.base.materials import BaseMaterial
from Eurocode.ec2.safety_factors import CONCRETE_SAFETY_FACTOR
from Eurocode.ec2.formulas import v_factor
import math
from Eurocode.base.units import (transform_units, transform_value, inverse_transform_value)
from pprint import pprint

CYLINDER_TO_CUBE_STRENGTHS = dict(zip(
    (12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90),
    (15, 20, 25, 30, 37, 45, 50, 55, 60, 67, 75, 85, 95, 105),
    ))

class Concrete(BaseMaterial):
    """
    Class representing unreinforced concrete
    """
    weight_density = 0
    gamma = CONCRETE_SAFETY_FACTOR

    def __init__(self, fck):
        """
        zer
        :param fck:
        """
        self._fck_raw = fck        #[MPA]

    @property
    @transform_units()
    def fck(self):
        """
        karakteristieke cilinderdruksterkte van beton na 28 dagen - [Pa]

        :rtype: float
        """
        if self._fck_raw in CYLINDER_TO_CUBE_STRENGTHS:
            self._fck = self._fck_raw
        else:
            raise ValueError(f'fck: {self._fck_raw} not possible')
        return self._fck

    @property
    @transform_units()
    def fck_cub(self):
        """
         - [Pa]
        :return:
        """
        if self._fck_raw in CYLINDER_TO_CUBE_STRENGTHS:
            return CYLINDER_TO_CUBE_STRENGTHS[self._fck_raw]

    @property
    @transform_units()
    def fcu(self):
        """
         - [Pa]
        :return:
        """
        return round(inverse_transform_value(self.fcd()) * 0.85, 2)  # factor langdurige belasting

    @property
    @transform_units()
    def fcm(self):
        """
        gemiddelde waarde van de cilinderdruksterkte van beton - [Pa]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        return round(inverse_transform_value(self.fck) + 8, 2)

    @property
    @transform_units()
    def fctm(self):
        """
         - [Pa]
        :return:
        """
        if inverse_transform_value(self.fck) <= 50:
            return round(0.30 * inverse_transform_value(self.fck)**(2/3), 2)
        else:
            return round(2.12 * math.log(1 + (inverse_transform_value(self.fcm) / 10)), 2)

    @property
    @transform_units()
    def fctk5(self):
        """
        karakteristieke van de axiale treksterkte van beton - [Pa]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        return round(0.7 * inverse_transform_value(self.fctm), 2)

    @property
    @transform_units()
    def fctk95(self):
        """
        karakteristieke van de axiale treksterkte van beton - [Pa]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        return round(1.3 * inverse_transform_value(self.fctm), 2)

    @property
    @transform_units(prefix='G')
    def Ecm(self):
        """
        secans-elasticiteitsmodulus van beton - [GPa]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        return round(22 * (inverse_transform_value(self.fcm) / 10)**0.3, 0)

    @property
    @transform_units(prefix='m')
    def ec1(self):
        """
        betonstuik bij de piekspanning f - [‰0]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        return round(min(0.7 * inverse_transform_value(self.fcm)**0.31, 2.8), 2)

    @property
    @transform_units(prefix='m')
    def ecu1(self):
        """
        grenswaarde van de betonstuik - [‰0]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        if inverse_transform_value(self.fck) < 50:
            return 3.5
        else:
            return round(2.8 + 27 * ((98 - inverse_transform_value(self.fcm)) / 100)**4, 2)

    @property
    @transform_units(prefix='m')
    def ec2(self):
        """
        betonstuik bij de piekspanning f - [‰0]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        if inverse_transform_value(self.fck) < 50:
            return 2
        else:
            return round(2 + 0.085 * (inverse_transform_value(self.fck) - 50)**0.53, 2)

    @property
    @transform_units(prefix='m')
    def ecu2(self):
        """
        grenswaarde van de betonstuik - [‰0]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        if inverse_transform_value(self.fck) < 50:
            return 3.5
        else:
            return round(2.6 + 35 * ((90 - inverse_transform_value(self.fck)) / 100)**4, 2)

    @property
    def n(self):
        """
        Exponent at Eq. (3.17)

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        if inverse_transform_value(self.fck) < 50:
            return 2
        else:
            return round(1.4 + 23.4 * ((90 - inverse_transform_value(self.fck)) / 100)**4, 2)

    @property
    @transform_units(prefix='m')
    def ec3(self):
        """
        betonstuik bij de piekspanning f - [‰0]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        if inverse_transform_value(self.fck) < 50:
            return 1.75
        else:
            return round(1.75 + 0.55 * ((inverse_transform_value(self.fck) - 50) / 40), 2)

    @property
    @transform_units(prefix='m')
    def ecu3(self):
        """
        grenswaarde van de betonstuik - [‰0]

        NBN EN 1992-1-1:2005 - Tabel 3.1 - Sterkte-en vervormingeigenschappen voor beton

        :return:
        """
        if inverse_transform_value(self.fck) < 50:
            return 3.5
        else:
            return round(2.6 + 35 * ((90 - inverse_transform_value(self.fck)) / 100) ** 4, 2)

    @transform_units()
    def fcd(self, ontwerp_situatie='blijvend', grenstoestand='ugt'):
        """
        design strenght - [Pa]

        :param ontwerp_situatie:
        :param grenstoestand:
        :return:
        """
        return round(inverse_transform_value(self.fck) / self.safety_factor(ontwerp_situatie, grenstoestand), 2)

    @transform_units()
    def vrdmax(self, ontwerp_situatie='blijvend', grenstoestand='ugt'):
        """
         - [Pa]
        :param ontwerp_situatie:
        :param grenstoestand:
        :return:
        Ved < 0.5 * bw * d * v * fcd
        #TODO check formula
        """
        return round(0.5 * v_factor(inverse_transform_value(self.fck)) * inverse_transform_value(self.fcd(ontwerp_situatie, grenstoestand)), 2)

    def _output(self):
        return {'fck': self.fck,
                'fckcube': self.fck_cub,
                'fcm': self.fcm,
                'fctm': self.fctm,
                'fctk5': self.fctk5,
                'fctk95': self.fctk95,
                'Ecm': self.Ecm,
                'ec1': self.ec1,
                'ecu1': self.ecu1,
                'ec2': self.ec2,
                'ecu2': self.ecu2,
                'n': self.n,
                'ec3': self.ec3,
                'ecu3': self.ecu3,
                'fcd': self.fcd(),
                'vrdmax': self.vrdmax()
                }

class ReinforcementSteel:

    def __init__(self, klasse, vorm, eis):
        pass

    def fyk(self):
        """
        vloeigrens
        :return:
        """

    def f02(self):
        pass

    def fy_max(self):
        pass

    def euk(self):
        pass







if __name__ == '__main__':
    cet = Concrete(12)
    pprint(cet._output())
    pprint(cet.__dict__)