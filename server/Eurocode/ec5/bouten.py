import math


class Bouten(VerbindingsMiddel):
    def __init__(self, materiaal, diameter, treksterkte, sluitringsterkte):
        super().__init__(materiaal=materiaal, diameter=diameter, lengte=lengte, treksterkte=treksterkte)
        self.bout_diameter = diameter
        self.treksterkte = treksterkte
        self.sterkte_sluitring = sluitringsterkte
        self.moment_vloei = 0.3 * self.treksterkte * self.bout_diameter ** 2.6
        self.voorgeboord = True


    def _checkVoorboring(self, member=None):
        return self.voorgeboord


    def K90(self, member):#verbindingstype mag weg
        if member.materiaal == 'Naaldhout':
            k_90 = 1.35 + 0.015 * self.bout_diameter
        elif member.materiaal == 'LVL':
            k_90 = 1.30 + 0.015 * self.bout_diameter
        elif member.materiaal == 'Loofhout':
            k_90 = 0.90 + 0.015 * self.bout_diameter
        else:
            k_90 = 'factor K90: verkeerde houtsoort'

        return k_90


    def __stuiksterkteHoutHout(self, member, verbindingskrachten):
        if self.bout_diameter < 30:
                K_90 = self.K90(member)
                stuiksterkte_even = 0.082 * (1 - (0.01 * self.bout_diameter)) * member.ro
                stuiksterkte = stuiksterkte_even / ((K_90 * (math.sin(verbindingskrachten['Rad']))**2) +
                                                    (math.cos(verbindingskrachten['Rad']))**2)
        else:
            print('boutdiameter te groot')

        return stuiksterkte


    def __stuiksterkteStaalHout(self, member, verbindingskrachten):
        if member.materiaal == 'staal':
            print('member moet hout zijn')
        if self.bout_diameter < 30:
                K_90 = self.K90(member)
                stuiksterkte_even = 0.082 * (1 - (0.01 * self.bout_diameter)) * member.ro
                stuiksterkte = stuiksterkte_even / ((K_90 * (math.sin(verbindingskrachten['Rad']))**2) +
                                                    (math.cos(verbindingskrachten['Rad']))**2)
        else:
            print('boutdiameter te groot')

        return stuiksterkte


    def __stuiksterktePlaatHout(self, member):
        if self.bout_diameter < 30:
            if member.hout_type == 'multiplex':
                stuiksterkte = 0.11 * (1 - 0.01 * self.bout_diameter) * member.ro
            elif member.hout_type == 'spaanplaat' or member.hout_type == 'osb':
                # welke dikte gebruiken????
                stuiksterkte = 50 * self.bout_diameter**(-0.6) * member.dikte
            else:
                stuiksterkte = 'element 1 moet plaat zijn van de soort Multiplex/Spaanplaat/OSB'

        return stuiksterkte


    def stuiksterkteHout(self, verbindingstype, element1, element2, verbindingskrachten):
        if self.bout_diameter < 30:
            if verbindingstype == 'Hout-op-hout' or verbindingstype == 'Staal-op-hout': # 2de deel stuik???
                # element 1 in berekening moet hout zijn
                if element1['Soort'] == 'Staal':
                    element2 = element1
                    element1 = element2
                K_90 = self.K90(element1)
                stuiksterkte_even = 0.082 * (1 - (0.01 * self.bout_diameter)) * element1['Ro']
                stuiksterkte = stuiksterkte_even / ((K_90 * (math.sin(verbindingskrachten['Rad']))**2) +
                                                    (math.cos(verbindingskrachten['Rad']))**2)
            elif verbindingstype == 'Plaat-op-hout':
                plaat = element1['Soort']
                if plaat == 'Multiplex':
                    stuiksterkte = 0.11 * (1 - 0.01 * self.bout_diameter) * element1['Ro']
                elif plaat == 'Spaanplaat' or plaat == 'OSB':
                    # welke dikte gebruiken????
                    stuiksterkte = 50 * self.bout_diameter**(-0.6) * element1['Dikte']
                else:
                    stuiksterkte = 'element 1 moet plaat zijn van de soort Multiplex/Spaanplaat/OSB'

        return stuiksterkte


    def uittreksterkte(self, element, verbindingstype):
        if verbindingstype == 'Staal-op-hout':
            if element['Soort'] == 'Staal':
                kracht = min(self.treksterkte, element['Treksterkte'])
            else:
                kracht = 'Element soort moet staal zijn'
        else:
            kracht = min (self.treksterkte, self.sterkte_sluitring)

        return kracht

if __name__ == '__main__':
    Bouten()