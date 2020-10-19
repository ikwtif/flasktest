from Eurocode.base.materials import BaseMaterial




class VerbindingsMiddel(BaseMaterial):

    def __init__(self, materiaal, diameter, lengte, treksterkte):
        self.materiaal = materiaal
        self.diameter = int(diameter)
        self.lengte = int(lengte)
        self.treksterkte = int(treksterkte)

    def checkVoorboring(self):
        raise NotImplementedError

    def _K90(self, member):
        if member.soort == 'naaldhout':
            K_90 =  1.35 + 0.015 * self.diameter
        elif member.soort == 'lvl':
            K_90 = 1.30 + 0.015 * self.diameter
        elif member.soort == 'loofhout':
            K_90 = 0.90 + 0.015 * self.diameter
        else:
            K_90 = 'factor K90: verkeerde houtsoort'

        return K_90

