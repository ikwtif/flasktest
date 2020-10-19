import math
from Eurocode.ec5.materials import VerbindingsMiddel
import logging


class Nagels(VerbindingsMiddel):
    weight_density = 1900
    def __init__(self, materiaal, diameter, lengte, treksterkte, uitvoering, kop_type, kop_diameter, fax, fhead, schroefdraad_hechtlengte=None):
        super().__init__(materiaal=materiaal, diameter=diameter, lengte=lengte, treksterkte=treksterkte)
        self.kop_type = kop_type
        self.kop_diameter = int(kop_diameter)
        self.uitvoering = uitvoering
        self.fax = int(fax)
        self.fhead = int(fhead)
        self.nagel_type = uitvoering
        self.schroefdraad_hechtlengte = schroefdraad_hechtlengte

    def _checkVoorboring(self, member):
        #8.3.1.1(2)
        if member.ro > 500 or self.diameter > 8:
            voorgeboord = True
        else:
            #8.3.1.2(6)
            d1 = 7 * self.diameter
            d2 = (13 * self.diameter) * (member.ro / 400)
            if member.dikte < max(d1, d2):
                voorgeboord = True
            else:
                voorgeboord = False
        #8.3.2(7)
        #gevoelig voor splijten
        if member.hout_type in ['den', 'douglasspar', 'spar']:
            d1 = 14 * self.diameter
            d2 = (13 * self.diameter - 30) * (member.ro / 200)
            if member.dikte < max(d1, d2):
                voorgeboord = True
            else:
                voorgeboord = False

        return voorgeboord

    @property
    def vloeimoment(self):
        if self.kop_type == 'rond':
            vloeimoment = 0.3 * self.treksterkte * self.diameter**2.6
        elif self.kop_type == 'vierkant' or self.kop_type == 'geprofileerd':
            vloeimoment = 0.45 * self.treksterkte * self.diameter**2.6
        else:
            raise ValueError(f'type nagelkop {self.kop_type} moet rond, vierkand of geprofileerd zijn')
        return vloeimoment

    @property
    def hechtlengte(self):
        if self.nagel_type == 'glad':
            hecht_lengte = 8 * self.diameter
        elif self.nagel_type == 'schroefdraad':
            hecht_lengte = 6 * self.diameter
        else:
            raise ValueError(f'type nagel is {self.nagel_type} maar moet glad of schroefdraad zijn')
        return hecht_lengte

    def stuiksterkteHout(self, member, verbinding_krachten=None):
        logging.info(f'berekening stuiksterkte {self.materiaal} voor {member.__dict__}')

        if member.plaat:
            stuiksterkte = self.__stuiksterkteHoutPlaat(member)
        elif member.plaat is False:
            stuiksterkte = self.__stuiksterkteHoutBalk(member, verbinding_krachten)
        else:
            stuiksterkte = None

        return stuiksterkte


    def __stuiksterkteHoutPlaat(self, member):
        """
        8.3.1.3 (3)
        """
        if member.plaat:    #overbodige check? mogelijks fout bij afzonderlijk ingeven
            pass
        else:
            raise ValueError(f'{member.__dict__} moet plaat zijn van de soort '
                             f'multiplex, spaanplaat, osb, of hardboard')
        if self.kop_diameter >= 2 * self.diameter:
            if member.hout_type == 'multiplex':
                stuiksterkte = 0.11 * member.ro * self.diameter ** (-0.3)
            elif member.hout_type == 'spaanplaat' or member.hout_type == 'osb':
                stuiksterkte = 65 * self.diameter ** (-0.7) * member.dikte ** 0.1
            elif member.hout_type == 'hardboard':
                stuiksterkte = 30 * self.diameter ** (-0.3) * member.dikte ** 0.6
        else:
            stuiksterkte = None
            raise ValueError(f'kopdiameter({self.kop_diameter}) moet ten minste {2*self.diameter} zijn')

        return stuiksterkte


    def __stuiksterkteHoutBalk(self, member, verbinding_krachten=None):
        """
        8.3.1.1(5)
        """
        voorgeboord = self._checkVoorboring(member)

        if self.diameter < 8:
            """
            8.3.1.1 (5) hout of LVL
            """
            if not voorgeboord:
                stuiksterkte = (0.082 * member.dikte * self.diameter**(-0.3))
            else:
                stuiksterkte = (0.082 * (1 - 0.01 * self.diameter) * member.ro)
        elif self.diameter >= 8:
            """
            stuiksterkte volgens bouten 8.5.1
            """
            K_90 = member._K90
            stuiksterkte = 0.082 * (1 - (0.01 * self.diameter)) * member.ro
            if verbinding_krachten:
                stuiksterkte = stuiksterkte / ((K_90 * (math.sin(verbinding_krachten['Rad']))**2) + (math.cos(verbinding_krachten['Rad']))**2)
        else:
            stuiksterkte = None
        return stuiksterkte


    def uittrekSterkte(self, member_punt, member_kop=None):
        """
        8.3.2 (4)  uittreksterkte nagel
        kleinste waarde in functie van 2 members
            - waarde ifv member puntzijde
            - waarde ifv member kopzijde
        """
        logging.info('berekening uittreksterkte nagel')
        #karakteristieke uittreksterkte aan de puntzijde
        #enkel schroefdraad en glad????
        #8.3.2(4) - (8.24)
        if self.nagel_type == 'glad':
            if self.schroefdraad_hechtlengte:
                hechtlengte = self.schroefdraad_hechtlengte
            else:
                hechtlengte = member_punt.hechtlengte

            if hechtlengte < self.hechtlengte:
                raise ValueError(f'Voorwaarde: Hechtlengte puntzijde ten minste {self.hechtlengte} zijn maar is {hechtlengte}')
            elif hechtlengte >= 12 * self.diameter:
                self.fax = 20 * 10**(-6) * member_kop.ro**2
                self.fhead = 70 * 10**(-6) * member_kop.ro**2
                factor = 1
            else:
                factor = (hechtlengte / ((4 * self.diameter) - 2))
                self.fax = self.fax
                self.fhead = self.fhead
            F1 = self.fax * self.diameter * hechtlengte
            F2 = self.fax * self.diameter * member_kop.dikte + self.fhead * self.kop_diameter**2
            uittreksterkte = (min(F1, F2) * factor)

        #8.3.2(4) - (8.23)
        else:#enkel voor schroefdraad???
            hechtlengte = member_punt.hechtlengte
            if self.schroefdraad_hechtlengte is not None:
                lengte_pen = min(hechtlengte, member_punt.schroefdraad_hechtlengte)
            else:
                lengte_pen = hechtlengte
            if hechtlengte < self.hechtlengte:
                print(f'hechtlengte die de puntzijde bevat moet ten minste {self.hechtlengte} zijn maar is {hechtlengte}')
            elif hechtlengte < (8 * self.diameter):
                factor = (hechtlengte / ((2 * self.diameter) - 3))
            else:
                factor = 1
            F1 = self.fax * self.diameter * lengte_pen
            F2 = self.fhead * self.kop_diameter ** 2
            uittreksterkte = (min(F1, F2) * factor)

        return uittreksterkte


if __name__ == '__main__':
    nagel = Nagels(materiaal='nagel', diameter=7, lengte=100, treksterkte=235, uitvoering='glad', kop_type='rond',
                   kop_diameter=10, fax=2.05, fhead=7.17)
    print('nageldict', nagel.__dict__)
    print(nagel.vloeimoment)
    print(nagel.hechtlengte)