import math
import logging
from pprint import pprint
from Eurocode.ec6.masonry import Masonry
#TODO decorator for length etc
# str -> float/int


"""
excel houdt geen rekening met condities voor hoogte -> slechtere(hoger) waarden hef in excel
"""


class Wall:
    def __init__(self, hoogte, lengte, dikte, vaste_zijrand, inklemming):
        """
        :param hoogte: hoogte van de wand
        :param lengte: lengte van de wand
        :param dikte: dikte van de wand
        :param vaste_zijrand:
        :param inklemming:
        """
        self.hoogte = float(hoogte)
        self.lengte = float(lengte)
        self.dikte = dikte
        self.dikte_effectief = dikte
        self.vaste_zijrand = vaste_zijrand
        self.inklemming = inklemming

    @property
    def vaste_zijrand(self):
        return self._vaste_zijrand

    @vaste_zijrand.setter
    def vaste_zijrand(self, vaste_zijrand):
        if isinstance(vaste_zijrand, str) and vaste_zijrand.isdigit():
            vaste_zijrand = int(vaste_zijrand)
        if vaste_zijrand in (2, 1, 0):
            self._vaste_zijrand = vaste_zijrand
        else:
            raise ValueError(f'vrije randen {vaste_zijrand} ongeldig')

    @property
    def slankheid(self):
        """
        NBN EN 1996-1-1:2006 (NL)
        5.5.1.4 Slankheid van metselwerkwanden

        Berekening van de slankheid van een metselwerkwand. Behoort niet groter te zijn dan 27

        formule: h[ef] / t[ef]

        :param effectieve_hoogte:
        :return:
        """
        # TODO check limit here + add to output?
        print(self.effectieveHoogte, self.dikte)
        return round(self.effectieveHoogte / self.dikte, 0)

    @property
    def reductiefactor_hoogte(self):
        """
        NBN EN 1996-1-1:2006 (NL)
        5.5.1.2 Effectieve hoogte van metselwerkwanden (10)

        Bepalen reductiefactor hoogte in functie van berekening effectieve hoogte
        """
        """
        excel 
        Public Function hef(positie As Boolean, inklemming As Boolean, opleg As Integer, zijrand As Integer, h As Double, a As Double) As Double
            Dim rhoinklem As Double
            Dim rho As Double


            If inklemming = True And positie = Not True And opleg = 2 Then
            rhoinklem = 0.75
            Else: rhoinklem = 1
            End If

            If zijrand = 1 Then
            rho = rhoinklem
            ElseIf zijrand = 2 Then
            rho = Application.Min(1.5 * a / h, rhoinklem)
            Else
            rho = Application.Min(a / (2 * h), rhoinklem)
            End If

            hef = h * rho
        """
        # TODO verify calculations
        if self.inklemming is True:
            # TODO
            #  add oplegging/excentriciteit? > or self.eindsteun< naar IF
            #  Voor wanden gesteund aan de boven- en onderzijde door gewapende betonvloeren of -(beton?)daken die
            #  aan beide zijden op hetzlfde niveau overspannen, of
            #  --> door een gewapende betonvloer die overspant aan slechts 1 zijde en die een oplegging heeft
            #  van min 2/3 van de dikte van de wand <--

            rho_inklemming = 0.75
        else:
            rho_inklemming = 1.0

        if self.vaste_zijrand == 1:
            if self.hoogte <= (3.5 * self.lengte):
                rho_3 = ((1 / (1 + (((rho_inklemming * self.hoogte) / (3 * self.lengte)) ** 2))) * rho_inklemming)
            else:
                rho_3 = max(1.5 * self.lengte / self.hoogte, 0.3)
            reductiefactor_hoogte = rho_3
        elif self.vaste_zijrand == 2:
            if self.hoogte <= (1.15 * self.lengte):
                rho_4 = ((1 / (1 + (((rho_inklemming * self.hoogte) / self.lengte) ** 2))) * rho_inklemming)
            else:
                rho_4 = 0.5 * self.lengte / self.hoogte
            reductiefactor_hoogte = rho_4
        else:
            reductiefactor_hoogte = rho_inklemming

        return round(reductiefactor_hoogte, 2)

    @property
    def effectieveHoogte(self):
        """
        NBN EN 1996-1-1:2006 (NL)
        5.5.1.2 Effectieve hoogte van metselwerkwanden (10)

        Berekening effectieve hoogte van een dragende wand, rekening houdend met de relatieve stijfheid van
        de constructie-onderdelen die met de wand zijn verbonden en met de effectiviteit van de verbindingen

        Formule (5.2): h[ef] = ro[n] * h
        :return: effectieve hoogte metselwerkwand
        """
        effectieve_hoogte = self.hoogte * self.reductiefactor_hoogte
        return round(effectieve_hoogte, 2)


class WallSimple(Wall):
    """
    EN 1996-3:2006
    4.4 Simplified calculation method for shear walls
    """

    def __init__(self, hoogte, lengte, vaste_zijrand, dak,
                 inklemming, eindsteun, hyperstatisch, dragende_richting, masonry, last_op_wand, lengte_overspanning=7):
        """
        :param hoogte: hoogte van de wand   [m]
        :param lengte: lengte van de wand   [m]
        :param vaste_zijrand: gesteunde randen van de wand (0,1,2)
        :param dak: wand onder dak
        :param inklemming: boven & onder inklemming van de wand
        :param eindsteun: wand is eindsteun van de vloer
        :param hyperstatisch: vloer is hyperstatisch
        :param dragende_richting: vloer draagd in 2 richtingen
        :param masonry: masonry object
        :param last_op_wand: totale last op wand in UGT
        :param lengte_overspanning: lengte overspanning van de vloer
        """
        super().__init__(hoogte=hoogte, lengte=lengte, dikte=masonry.stone.width/1000,
                         vaste_zijrand=vaste_zijrand, inklemming=inklemming)
        self.dak = dak
        self.masonry = masonry
        # inklemming = betonvloer
        # geen inklemming = houten vloer
        self.eindsteun = eindsteun
        self.hyperstatisch = hyperstatisch
        self.dragende_richting = dragende_richting
        self.lengte_overspanning = lengte_overspanning
        self.last_op_wand = last_op_wand

    @property
    def lengte_overspanning_effectief(self):
        """
        EN 1996-3:2006 (E)
        p 16
        """
        # TODO check calculations
        if self.eindsteun and self.hyperstatisch:
            l_ef = 0.7 * self.lengte_overspanning
        else:
            l_ef = self.lengte_overspanning
        return round(l_ef, 2)

    def voorwaarde_overspanning(self):
        if self.masonry.stone.group == 'groep 1':
            k_G = 0.2
        elif self.masonry.stone.group in ('groep 2', 'groep 3'):
            k_G = 0.1
        else:
            raise ValueError(f'steen groep ongeldig')
        #TODO check steenkarak of ander
        if self.eindsteun:
            if self.last_op_wand <= self.dikte * k_G * 1000 * self.masonry.sterkte_rekenwaarde:
                overspanning_vloer_max = 7*1000 #in mm
            else:
                if self.masonry.sterkte_rekenwaarde > 2.5:
                    overspanning_vloer_max = min(4.5*1000 + 10 * self.dikte, 7*1000)
                else:
                    overspanning_vloer_max = min(4.5*1000 + 10 * self.dikte, 6*1000)
        else:
            overspanning_vloer_max = None

        if overspanning_vloer_max is not None:
            overspanning_vloer_max = round(overspanning_vloer_max , 2)

        return overspanning_vloer_max

    @property
    def reductiefactor_draagvermogen(self):
        """
        EN 1996-1
        4.2.2.3 Reductiefactor op draagvermogen
        EN 1996-3 ANB:2012
        Vervanging formules (4.5a);(4.5b);(4.5c)
        :return:
        """

        '''
        if self.eindsteun is False:
            reductie_factor = 0.85 - 0.0011 * (self.effectieveHoogte / self.dikte) ** 2
        elif self.eindsteun and self.dak is False:
            reductie_factor = min(1.3 - (self.lengte_overspanning_effectief / 8), 0.85,
                                  0.85 - 0.0011 * (self.effectieveHoogte / self.dikte) ** 2)
        elif self.eindsteun and self.dak:
            reductie_factor = min(0.4, 1.3 - (self.lengte_overspanning_effectief / 8),
                                  0.85 - 0.0011 * (self.effectieveHoogte / self.dikte) ** 2)
        else:
            raise ValueError(f'reduciefactor kan niet berekend worden')
        '''
        reductie_factor = min((1.3 - (self.lengte_overspanning_effectief / 8) - 0.0004 * (self.effectieveHoogte / self.dikte_effectief)**2),
                              0.85 - 0.0011 * (self.effectieveHoogte / self.dikte_effectief)**2)

        return round(reductie_factor, 2)

    @property
    def sterkte(self):
        """

        :param steen_sterkte_design: sterkte_rekenwaarde fd
        :return:
        """
        wand_sterkte_design = self.reductiefactor_draagvermogen * self.masonry.sterkte_rekenwaarde * self.dikte * 1000

        return round(wand_sterkte_design, 0)

    def calculation(self):
        self.voorwaarde_overspanning()
        wand_sterkte_design = self.sterkte
        if self.last_op_wand <= wand_sterkte_design:
            logging.info(f'Ned<=Nrd - {self.last_op_wand} kN/m <= {round(wand_sterkte_design, 2)} kN/m')
            return f'Ned<=Nrd - {self.last_op_wand} kN/m <= {round(wand_sterkte_design, 2)} kN/m'
        else:
            return f'wand niet sterk genoeg \n Ned>Nrd - {self.last_op_wand}>{wand_sterkte_design}'

    #TODO probably create wrapper here -> gebruikt wel variabele namen
    def output(self):
        dic = self.masonry.output()
        wall = {'wall': {
                        'hoogte [mm]': self.hoogte,
                        'lengte [mm]': self.lengte,
                        'breedte [mm]': self.dikte,
                        'vaste zijrand': self.vaste_zijrand,
                        'dak': self.dak,
                        'inklemming': self.inklemming,
                        'eindsteun': self.eindsteun,
                        'lengte overspanning [mm]': self.lengte_overspanning * 1000,
                        'hyperstatisch': self.hyperstatisch,
                        'draagrichting': self.dragende_richting,
                        'output': {'effectieve hoogte [mm]': self.effectieveHoogte * 1000,
                                   'effectieve overspanning [mm]': self.lengte_overspanning_effectief * 1000,
                                   'reductiefactor': self.reductiefactor_draagvermogen,
                                   'reductiefactor hoogte': self.reductiefactor_hoogte,
                                   'slankheid': self.slankheid
                                   }
                        }
                }

        return dict(dic, **wall)


class WallExtensive(Wall):
    def __init__(self, hoogte, lengte, vaste_zijrand, inklemming, masonry, last_op_wand,
                 boven_e_belasting=20, boven_e_horizontaal=5, onder_e_belasting=20, onder_e_horizontaal=5,
                 midden_e_belasting=20, midden_e_horizontaal=5, coeff_kruip=0, elasticiteitsfactor_1=700,
                 elasticiteitsfactor_2=1000, boven_m=0, boven_n=0, onder_m=0, onder_n=0, midden_m=0, midden_n=0):
        super().__init__(hoogte=hoogte, lengte=lengte, dikte=masonry.stone.width / 1000,
                         vaste_zijrand=vaste_zijrand, inklemming=inklemming)
        self.masonry = masonry
        self.last_op_wand = last_op_wand
        self.boven_m = int(boven_m)
        self.boven_n = int(boven_n)
        self.boven_e_belasting = int(boven_e_belasting)
        self.boven_e_horizontaal = int(boven_e_horizontaal)

        self.onder_m = int(onder_m)
        self.onder_n = int(onder_n)
        self.onder_e_belasting = int(onder_e_belasting)
        self.onder_e_horizontaal = int(onder_e_horizontaal)

        self.midden_m = int(midden_m)
        self.midden_n = int(midden_n)
        self.midden_e_belasting = int(midden_e_belasting)
        self.midden_e_horizontaal = int(midden_e_horizontaal)

        self.coeff_kruip = int(coeff_kruip)
        self.elasticiteitsfactor_1 = int(elasticiteitsfactor_1)
        self.elasticiteitsfactor_2 = int(elasticiteitsfactor_2)

        self.e_initieel = (self.effectieveHoogte * 1000 / 450)

    def _excentriciteit(self, M, N, e_bel, e_he, e_init):
        excent_min = 0.05 * self.dikte * 1000
        if M is None or N is None or M == 0 or N == 0:
            excent = e_bel + e_he + e_init
        else:
            excent = (M / N) + e_he + e_init
        return max(excent, excent_min)

    def _excentriciteit_midden(self, M, N, e_bel, e_he, e_init, kruip_coeff):
        excent_min = 0.05 * self.dikte * 1000
        if M is None or N is None or M == 0 or N == 0:
            excent = e_bel + e_he + e_init
        else:
            excent = (M / N) + e_he + e_init

        if self.slankheid > 15:
            e_k = 0.002 * kruip_coeff * (self.effectieveHoogte/self.dikte_effectief) * math.sqrt(self.dikte * excent)
        else:
            e_k = 0
        return max(excent + e_k, excent_min)

    def _reductiefactor_onder(self):
        excentriciteit = self._excentriciteit(M=self.onder_m, N=self.onder_n,
                                               e_bel=self.onder_e_belasting,
                                               e_he=self.onder_e_horizontaal,
                                               e_init=self.e_initieel
                                               )
        return round(1 - (2 * (excentriciteit / (self.dikte * 1000))), 2)

    def _reductiefactor_boven(self):
        excentriciteit = self._excentriciteit(M=self.boven_m, N=self.boven_n,
                                               e_bel=self.boven_e_belasting,
                                               e_he=self.boven_e_horizontaal,
                                               e_init=self.e_initieel
                                               )
        return round(1 - (2 * (excentriciteit / (self.dikte * 1000))), 2)

    def _reductiefactor_midden(self, elasticiteitsmodulus):
        excentriciteit = self._excentriciteit_midden(M=self.midden_m, N=self.midden_n,
                                                      e_bel=self.midden_e_belasting,
                                                      e_he=self.midden_e_horizontaal,
                                                      e_init=self.e_initieel,
                                                      kruip_coeff=self.coeff_kruip
                                                      )

        factor_A = 1 - (2 * (excentriciteit / (self.dikte*1000)))
        factor_L = (self.effectieveHoogte * 1000 / (self.dikte_effectief * 1000)) * math.sqrt(self.masonry.sterkte_karakteristiek / elasticiteitsmodulus)
        factor_U = (factor_L - 0.063) / (0.73 - (1.17 * (excentriciteit / (self.dikte*1000))))
        return round(factor_A * math.exp(-((factor_U**2) / 2)), 2)

    def _reductieFactoren_uitgebreid(self):
        red_boven = self._reductiefactor_boven()
        red_onder = self._reductiefactor_onder()

        elasticiteitsmodulus_1 = self.elasticiteitsfactor_1 * self.masonry.sterkte_karakteristiek
        elasticiteitsmodulus_2 = self.elasticiteitsfactor_2 * self.masonry.sterkte_karakteristiek

        red_midden_1 = self._reductiefactor_midden(elasticiteitsmodulus_1)
        red_midden_2 = self._reductiefactor_midden(elasticiteitsmodulus_2)

        logging.info(f'reductiefactor boven: {red_boven} \n'
                     f'reductiefactor onder: {red_onder} \n'
                     f'reductiefactor midden 1 : {red_midden_1} \n'
                     f'reductiefactor midden 2: {red_midden_2}')
        return red_boven, red_onder, red_midden_1, red_midden_2

    def reductieFactor_uitgebreid(self):
        red_boven, red_onder, red_midden_1, red_midden_2 = self._reductieFactoren_uitgebreid()
        return min(red_boven, red_onder, red_midden_1, red_midden_2)

    def wandSterkte_uitgebreid(self):
        reductiefactor = self.reductieFactor_uitgebreid()
        wand_sterkte_design = reductiefactor * self.masonry.sterkte_karakteristiek * self.dikte * 1000
        return round(wand_sterkte_design, 0)

    def wandConditie_uitgebreid(self):
        wand_sterkte_design = self.wandSterkte_uitgebreid()

        if self.last_op_wand <= wand_sterkte_design:
            if self.slankheid < 27:
                logging.info(f'Ned<=Nrd - {self.last_op_wand} kN/m <= {round(wand_sterkte_design, 2)} kN/m')
                return f'Ned<=Nrd - {self.last_op_wand} kN/m <= {round(wand_sterkte_design, 2)} kN/m'
            else:
                return f'wand te slank: {self.slankheid} > 27'
        else:
            return f'wand niet sterk genoeg \n Ned>Nrd - {self.last_op_wand}>{wand_sterkte_design}'

    #TODO probably create wrapper here -> gebruikt wel variabele namen
    def output(self):
        dic = self.masonry.output()
        wall = {'wall': {
                        'hoogte [mm]': self.hoogte,
                        'lengte [mm]': self.lengte,
                        'breedte [mm]': self.dikte,
                        'vaste zijrand': self.vaste_zijrand,
                        'inklemming': self.inklemming,
                        'output': {'effectieve hoogte [mm]': self.effectieveHoogte * 1000,
                                   'reductiefactor': self.reductieFactor_uitgebreid(),
                                   'reductiefactor hoogte': self.reductiefactor_hoogte,
                                   'slankheid': self.slankheid
                                   }
                        }
                }

        return dict(dic, **wall)

if __name__ == '__main__':

    from Eurocode.ec6.masonry import Masonry
    brick = Masonry(stone_height=190, stone_width=140, stone_length=290, stone_kind='baksteen', stone_fmean=10,
                    stone_group='groep 2',
                    mortar_kind='algemeen', mortar_group=12,
                    application='stenen van categorie II met willekeurige mortel', supervision='normaal')
    wand = WallSimple(hoogte=2.7, lengte=8, vaste_zijrand=2, dak=False, inklemming=True, eindsteun=False,
                      lengte_overspanning=5, hyperstatisch=False, dragende_richting=False,
                      masonry=brick, last_op_wand=100)
    pprint(wand.output())
    wand2 = WallExtensive(hoogte=2.7, lengte=8, vaste_zijrand=2, inklemming=True, masonry=brick, last_op_wand=100)
