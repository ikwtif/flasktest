from Eurocode.ec2.materials import Concrete
from Eurocode.base.materials import BaseMaterial
from pprint import pprint
import math
from Eurocode.base.units import (transform_units, transform_value, inverse_transform_value)
from collections import OrderedDict

# 1 pa == 1 N/m²
# 1 Mpa == 1 N/mm²
# --------------------------
# 1 Mpa == 1 * 10**-3 kN/mm³
# 1 pa == 1 * 10**-6 N/mm³
# 1 pa == 1 * 10**-9 kN/mm²
# --------------------------
# UNIT_PREFIXES = {
#         'G': 1e+09,
#         'M': 1e+06,
#         'k': 1e+03,
#         'none': 1,
#         'c': 1e-02,
#         'm': 1e-03,
#         }
# --------------------------


def zwaartepunt_rlhoek(breedte1, hoogte1, breedte2=0, hoogte2=0):
    """
    berekenen zwaartepunt voor rechthoek/vierkant/L-vorm
    :param breedte1:
    :param hoogte1:
    :param breedte2:
    :param hoogte2:
    :return:
    """
    if breedte1 < (hoogte1 + hoogte2) or breedte2 > (hoogte1 + hoogte2):
        if breedte1 > breedte2:
            hoogte1, hoogte2, breedte1, breedte2 = breedte2, breedte1-breedte2, hoogte2+hoogte1, hoogte1
        elif breedte1 <= breedte2:
            hoogte1, hoogte2, breedte1, breedte2 = breedte1, breedte2-breedte1, hoogte1+hoogte2, hoogte2

    A1 = breedte1 * hoogte1
    A2 = breedte2 * hoogte2
    C1 = hoogte1 / 2
    C2 = hoogte2 / 2 + hoogte1

    C = (C1 * A1 + C2 * A2) / (A1 + A2)

    D1 = abs(C - C1)
    D2 = abs(C - C2)

    I1 = (1 / 12) * breedte1 * (hoogte1 ** 3)
    I2 = (1 / 12) * breedte2 * (hoogte2 ** 3)
    I1n = I1 + A1 * (D1 ** 2)
    I2n = I2 + A2 * (D2 ** 2)
    In = I1n + I2n

    return In


class Shape:
    """
    Shape of element
    """
    def __init__(self, **kwargs):
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')
        self.radius = kwargs.get('radius')
        self.height2 = kwargs.get('heigth2')
        self.width2 = kwargs.get('width2')

    @property
    def area(self):
        """
        calculates area of a shape (circle, L-rectangle, rectangle)
        :return:
        """
        if self.radius:
            return round(self.radius * math.pi, 2)
        elif self.width2 and self.height2:
            return round(((self.width * self.height) + (self.width2 * self.height2)), 2)
        elif self.width and self.height:
            return round(self.width * self.height, 2)

    @property
    def oppervlaktetraagheidsmoment(self):
        """
        calculates moment of inertie for shape
        :return:
        """
        if self.radius:
            return math.pi * (self.radius**4) / 4
        elif self.width2 and self.height2:
            return  zwaartepunt_rlhoek(self.width, self.height, self.width2, self.height2)
        elif self.width and self.height:
            return zwaartepunt_rlhoek(self.width, self.height)

    @property
    def traagheidsstraal(self):
        """
        calculates radius of gyration
        :return:
        """
        return round(math.sqrt(self.oppervlaktetraagheidsmoment / self.area), 2)


class Column(Shape, BaseMaterial):
    """
    Column
    """
    weight_density = None

    def __init__(self, length, lownode, highnode, width=None, height=None, radius=None, width2=None, heigth2=None, k1=0.1, k2=0.1):
        super().__init__(height=height, width=width, radius=radius, width2=width2, heigth2=heigth2)
        self.length = length
        self.lownode = lownode
        self.highnode = highnode
        self.spring_constant_high = k1
        self.spring_constant_low = k2


    @property
    def length_effective(self):
        """
        calculates effective length for column
        """
        if self.lownode == 'scharnier' and self.highnode == 'scharnier':
            lef = self.length
        elif self.lownode == 'inklemming' and self.highnode == 'vrij':
            lef = 2 * self.length
        elif self.lownode == 'inklemming' and self.highnode == 'scharnier':
            lef = self.length / math.sqrt(2)
        elif self.lownode == 'inklemming' and self.highnode == 'inklemming':
            lef = self.length / 2
        elif self.lownode == 'inklemming' and self.highnode == 'rol':
            lef = self.length
        elif self.lownode == 'veer' and self.highnode == 'veer':
            lef = 0.5 * self.length * math.sqrt((1 + (self.spring_constant_high / (0.45 + self.spring_constant_high))) *
                                                (1 + (self.spring_constant_low / (0.45 + self.spring_constant_low))))
            if self.length / 2 < lef < self.length:
                pass
            else:
                raise ValueError('error lef')
        elif self.lownode == 'veer' and self.highnode == 'vrij':
            lef = self.length * max(math.sqrt(1 + (10 * ((self.spring_constant_high * self.spring_constant_low) /
                                                         (self.spring_constant_high + self.spring_constant_low)))),
                                            ((1 + (self.spring_constant_high / (1 + self.spring_constant_high))) *
                                             (1 + (self.spring_constant_low / (1 + self.spring_constant_low)))))
            if lef > 2 * self.length:
                pass
            else:
                raise ValueError('error lef')

        return round(lef, 2)


    @property
    def slenderness(self):
        """
        calculates slenderness for column
        :return:
        #TODO round up?
        """

        return math.ceil(self.length_effective / self.traagheidsstraal)


class ConcreteColumn(Column, Concrete):
    """
    Concrete Column
    """
    weight_density = 2400

    def __init__(self, length, lownode='inklemming', highnode='scharnier', width=None, height=None, materiaalcoeff=None,
                 fck=None, width2=None, height2=None, radius=None, k1=None, k2=None):
        """

        :param length:
        :param width:
        :param height:
        :param lownode:
        :param highnode:
        :param materiaalcoeff:
        :param fck: Characteristic strengh [Mpa] [N/mm²]
        """
        Column.__init__(self, length=length, lownode=lownode, highnode=highnode, width=width, height=height,
                        heigth2=height2, width2=width2, radius=radius, k1=k1, k2=k2)
        Concrete.__init__(self, fck=fck)
        self.materiaalcoeff = materiaalcoeff
        # default parameters
        self.ro3 = 0.003
        self.ro8 = 0.008
        self.area_steel = None
        self.area_steel_stifness = None
        self.fsd = None
        self.total_reinforcementbars = None

    def buckling_factor(self, ouderdom_belasting=100):
        """
        calculates buckling factor for concrete column
        knikfactor lambda
        :return:
        """
        ym = 0

        if 25 <= self.slenderness <= 50:
            ym = 1 / (1 + 0.2 * (self.slenderness / 35)**2)
        elif 50 < self.slenderness <= 100:
            ym = 0.70 * (50 / self.slenderness)**2
            print(f'gebruik excentrische - te zware wapening')
        else:
            print("slankheid te klein: ", self.slenderness)

        if 7.22 <= self.length_effective / self.width <= 14.43:
            ym = 1 / (1 + 0.2 * ((self.length_effective / self.width) / 10.10) ** 2)
        elif 14.43 < self.length_effective / self.width <= 28.87:
            ym = 0.70 * (14.43 / (self.length_effective / self.width)) ** 2

        #aanpassing coeff ifv kruip
        if 29 <= ouderdom_belasting < 90:
            ym = ym / 1.10
        elif ouderdom_belasting < 28:
            ym = ym / 1.20
        else:
            pass

        return round(ym, 2)

    @property
    def area_concrete(self):
        """
        Calculates are of concrete based on shape
        :return: area of concrete
        :rtype: float
        """
        if self.radius:
            radius = self.radius - 10
            return round(radius * math.pi, 2)

        elif self.width2 and self.height2:
            width = self.width - 20
            height = self.height - 20
            width2 = self.width2 - 20
            height2 = self.height2 - 10
            return round(((width * height) + (width2 * height2)), 2)

        elif self.width and self.height:
            width = self.width - 20
            height = self.height - 20
            return round(width * height, 2)

    def area_steel_design(self, ro, N_design, fsd=400):
        """

        :param N_design: design load in Newton
        :param fsd: quality steel
        :return: area_steel_stifness [N/mm/mm]
        :rtype: float
        """
        v = N_design / ((1 - ro) * self.area * 10**-6 * self.fcd() * 10**3)
        #TODO check v
        print('v', v)

        if self.slenderness <= 25 or self.slenderness <= (15 / math.sqrt(v)):
            if 50 < self.slenderness <= 100:
                print('berekening eenvoudige knikberekening voor centrisch belaste kolommen')
                return ((N_design / self.buckling_factor()) - (self.area_concrete * self.fcu * 10 ** -6)) / fsd
            else:
                print('berekening zuiver druk')
                #TODO check voorwaarden
                return (1.1 * N_design - self.area * self.fcu * 10**-6) / (fsd - self.fcu * 10**-6)
        else:
            print('berekening eenvoudige knikberekening voor centrisch belaste kolommen')
            return ((N_design / self.buckling_factor()) - (self.area_concrete * self.fcu * 10 ** -6)) / fsd

    def _area_column_minimum(self, N_design, ro, fsd):
        """
        Calculates minimum required concrete area
        :param N_design: [Newton]
        :param ro:
        :param fsd: [N/mm/MM]
        :return: [mm²]
        #yn = 1.1 (factor onnauwkeurigheden)
        """
        return (1.1 * N_design * 10**-6) / ((1 - ro) * self.fcu * 10**-6 + ro * fsd) * 10**6

    def add_total_reinforcement(self, area_steel, area_steel_stifness, fsd=400):
        if self.area_steel is not None or self.area_steel_stifness is not None or self.fsd is not None:
            raise Exception("bars already applied")
        else:
            self.area_steel = area_steel
            self.area_steel_stifness = area_steel_stifness
            self.fsd = fsd

    def add_bar_reinforcement(self, amount, diameter, stiffness=None, fsd=400):
        area_bar = amount * diameter * 4 * math.pi**2
        self.area_steel += area_bar
        self.total_reinforcementbars = amount
        if stiffness:
            self.area_steel_stifness += area_bar
        if self.fsd is None:
            self.fsd = fsd
        elif self.fsd == fsd:
            pass
        else:
            raise Exception(f"different steel strength than already used bars")

    def reinforcement_ugt(self, load_kN, full_report=None):
        """

        :param area_steel:
        :param area_steel_stifness:
        :param load_kN:
        :param fsd:
        :param full_report:
        :return:
        """
        if self.area_steel is None or self.area_steel_stifness is None or self.fsd is None:
            raise Exception(f"add_reinforcement")

        ro = self.area_steel / self.area
        #ro = 0.01
        N_design = load_kN * 10 ** 3
        Area_Column_Min = self._area_column_minimum(N_design, ro, self.fsd)

        errors = dict()
        errors['errors'] = list()
        if self.area < Area_Column_Min:                                    #TODO check vw
            errors['errors'].append('A < Amin')
        if self.area_steel < self.ro3 * self.area:
            errors['errors'].append('area_steel < 0.3% A')
        if self.area_steel < self.ro8 * Area_Column_Min:
            errors['errors'].append('area_steel < 0.8% Amin')
        if self.area_steel > 0.04 * self.area:
            errors['errors'].append('area_steel > 4% A')
        if self.area_steel_stifness < self.area_steel_design(ro, load_kN, self.fsd):
            errors['errors'].append('area_steel_stifness < As0d')
        if len(errors['errors']) > 0:
            errors['design'] = False
        else:
            errors['design'] = True

        if full_report:
            result = _output_empty()
            res = (('Ro', round(ro, 6)),
                   ('Load', load_kN),
                   ('Fcu', self.fcu * 10**-6),
                   ('Slankheid', self.slenderness),
                   ('Kniklengte', self.length_effective),
                   ('Knikfactor', round(self.buckling_factor(), 2)),
                   ('L0/b', round(self.length_effective / self.width, 2)),
                   ('AreaColumn', round(self.area, 0)),
                   ('AreaConcrete', round(self.area_concrete, 0)),
                   ('AreaSteel', self.area_steel),
                   ('area_steel_stifness', self.area_steel_stifness),
                   ('AreaSteelDesign', round(self.area_steel_design(ro, N_design, self.fsd), 0)),
                   ('AreaMinimum', round(Area_Column_Min, 2)),
                   ('AreaSteelPercent0.3', round(self.ro3 * self.area, 0)),
                   ('AreaMinSteelPercent0.8', round(self.ro8 * Area_Column_Min, 0)),
                   ('AreaSteelPercent4', round(0.04 * self.area, 0))
                   )

            for tup in res:
                print(tup)
                result[tup[0]]['value'] = tup[1]
            return {**errors, **result}
        else:
            return errors

    def output_report(self):
        some_dict = {}

        return some_dict

def _output_empty ():
    return {'Ro': {'value': 0, 'units': ''},
            'AreaSteel': {'value': 0, 'units': 'mm²'},
            'area_steel_stifness': {'value': 0, 'units': 'mm²'},
            'Load': {'value': 0, 'units': 'kN/mm³'},
            'Fcu': {'value': 0, 'units': 'N/mm²'},
            'Slankheid': {'value': 0, 'units': ''},
            'Kniklengte': {'value': 0, 'units': 'mm'},
            'Knikfactor': {'value': 0, 'units': ''},
            'L0/b': {'value': 0, 'units': ''},
            'AreaConcrete': {'value': 0, 'units': 'mm³'},
            'AreaSteelDesign': {'value': 0, 'units': 'mm³'},
            'AreaMinimum': {'value': 0, 'units': 'mm³'},
            'AreaColumn': {'value': 0, 'units': 'mm³'},
            'AreaSteelPercent0.3': {'value': 0, 'units': 'mm³'},
            'AreaMinSteelPercent0.8': {'value': 0, 'units': 'mm³'},
            'AreaSteelPercent4': {'value': 0, 'units': 'mm³'}
            }




if __name__ == '__main__':
    col = ConcreteColumn(length=3000, width=140, height=300, fck=25)

    pprint(col.reinforcement_ugt(area_steel=616, area_steel_stifness=616, load_kN=200, fsd=400))




