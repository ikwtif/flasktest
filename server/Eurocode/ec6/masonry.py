from Eurocode.ec6.data import MASONRY_APPLICATION, MASONRY_SUPERVISION, FORMFACTOR, STONE_CONDITIONINGFACTOR
from Eurocode.ec6.materials import Stone, Mortar
import pandas as pd
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger(__name__)

log.setLevel(logging.WARNING)


class Masonry:
    """Masonry"""

    def __init__(self, stone_height, stone_width, stone_length, stone_kind, stone_group, mortar_kind, mortar_group,
                 stone_fmean, application, supervision):
        """

        :param stone_height: hoogte van de steen [mm]
        :param stone_width: breedte van de steen [mm]
        :param stone_length: lengte van de steen [mm]
        :param stone_kind: steensoort
        :param stone_group: steengroep
        :param mortar_kind: mortelsoort
        :param mortar_group: mortelgroep
        :param stone_fmean: druksterkte steen [MPa]
        :param application: toepassing
        :param supervision: supervisie op werf
        """
        self.stone = Stone(height=stone_height, width=stone_width, length=stone_length, kind=stone_kind,
                           group=stone_group, f_mean=stone_fmean)
        self.mortar = Mortar(kind=mortar_kind, group=mortar_group)
        self.application = application
        self.supervision = supervision

    def __str__(self):
        return f"stone_dimensions: {self.stone.dimension} mm \n" \
               f"stone_kind: {self.stone.kind} \n" \
               f"stone_group: {self.stone.group} \n" \
               f"mortar_kind: {self.mortar.kind} \n" \
               f"mortar_group: {self.mortar.group} kN/mm² \n" \
               f"stone_fmean: {self.stone.f_mean} kN/mm² \n" \
               f"application: {self.application} \n" \
               f"supervision: {self.supervision}"

    # {{{ properties
    @property
    def supervision(self):
        return self._supervision
    @supervision.setter
    def supervision(self, supervision):
        if supervision in MASONRY_SUPERVISION:
            self._supervision = supervision
        elif isinstance(supervision, int):
            self._supervision = MASONRY_SUPERVISION[supervision]
        else:
            raise ValueError(f'MASONRY_SUPERVISION {supervision} ongeldig')

    @property
    def application(self):
        return self._application
    @application.setter
    def application(self, application):
        if application in MASONRY_APPLICATION:
            self._application = application
        elif isinstance(application, int):
            self._application = MASONRY_APPLICATION[application]
        else:
            raise ValueError(f'application: {application} ongeldig')

    @property
    def druksterkte_genormaliseerde_gemiddelde(self):
        """
        NBN_EN1996-1-1 ANB 2016
        (3.1) fb = fmean * vormfactor * factor_conditionering
        normalized mean compressive strength [NBN EN 772-1]
        :return: fb
        """
        return round(self.stone.f_mean * self.vormfactor * self.conditioneringsfactor, 2)

    @property
    def vormfactor(self):
        """
        vormfactor voor gebruik in druksterkteGenormaliseerdeGemiddelde()
        :return: vormfactor
        """
        df = pd.DataFrame(FORMFACTOR, columns=['hoogte', 50, 100, 150, 200, 250])
        df.set_index('hoogte', inplace=True)
        hoogte = [40, 50, 65, 100, 150, 200, 250]
        breedte = [50, 100, 150, 200, 250]
        nextlowest = lambda seq, x: min([(x - i, i) for i in seq if x >= i] or [(0, None)])[1]
        nexthighest = lambda seq, x: max([(x - i, i) for i in seq if x <= i] or [(0, None)])[1]

        if self.stone.height in hoogte and self.stone.width in breedte:
            vormfactor = df.loc[self.stone.height, self.stone.width]

        elif self.stone.height >= max(hoogte) and self.stone.width >= max(breedte):
            vormfactor = df.loc[max(hoogte), max(breedte)]

        elif self.stone.height in hoogte and self.stone.width not in breedte:
            if self.stone.width >= max(breedte):
                vormfactor = df.loc[self.stone.height, max(breedte)]
            else:
                breedte_low = nextlowest(breedte, self.stone.width)
                breedte_high = nexthighest(breedte, self.stone.width)
                ylow = df.loc[self.stone.height, breedte_low]
                yhigh = df.loc[self.stone.height, breedte_high]
                vormfactor = self.interpoleren(y1=ylow, y2=yhigh, x=self.stone.width, x1=breedte_low, x2=breedte_high)

        elif self.stone.height not in hoogte and self.stone.width in breedte:
            if self.stone.height >= max(hoogte):
                vormfactor = df.loc[max(hoogte), self.stone.width]
            else:
                hoogte_low = nextlowest(hoogte, self.stone.height)
                hoogte_high = nexthighest(hoogte, self.stone.height)
                ylow = df.loc[hoogte_low, self.stone.width]
                yhigh = df.loc[hoogte_high, self.stone.width]
                vormfactor = self.interpoleren(y1=ylow, y2=yhigh, x=self.stone.width, x1=hoogte_low, x2=hoogte_high)

        elif self.stone.height not in hoogte and self.stone.width not in breedte:
            if self.stone.height >= max(hoogte) and self.stone.width < max(breedte):
                hoog = max(hoogte)
                breedte_low = nextlowest(breedte, self.stone.width)
                breedte_high = nexthighest(breedte, self.stone.width)
                ylow = df.loc[hoog, breedte_low]
                yhigh = df.loc[hoog, breedte_high]
                vormfactor = self.interpoleren(y1=ylow, y2=yhigh, x=self.stone.width, x1=breedte_low, x2=breedte_high)

            elif self.stone.height < max(breedte) and self.stone.width >= max(breedte):
                breed = max(breedte)
                hoogte_low = nextlowest(hoogte, self.stone.height)
                hoogte_high = nexthighest(hoogte, self.steen.stone.height)
                ylow = df.loc[hoogte_low, breed]
                yhigh = df.loc[hoogte_high, breed]
                vormfactor = self.interpoleren(y1=ylow, y2=yhigh, x=self.stone.width, x1=hoogte_low, x2=hoogte_high)

            else:
                breedte_low = nextlowest(breedte, self.stone.width)
                breedte_high = nexthighest(breedte, self.stone.width)
                hoogte_low = nextlowest(hoogte, self.stone.height)
                hoogte_high = nexthighest(hoogte, self.stone.height)
                low_low = df.loc[hoogte_low, breedte_low]
                low_high = df.loc[hoogte_high, breedte_low]
                high_low = df.loc[hoogte_low, breedte_high]
                high_high = df.loc[hoogte_high, breedte_high]
                t1 = self.interpoleren(y1=low_low, y2=high_low, x=self.stone.width, x1=breedte_low, x2=breedte_high)
                t2 = self.interpoleren(y1=low_high, y2=high_high, x=self.stone.width, x1=breedte_low, x2=breedte_high)
                vormfactor = self.interpoleren(y1=t1, y2=t2, x=self.stone.height, x1=hoogte_low, x2=hoogte_high)

        return round(vormfactor, 2)

    @property
    def sterkte_karakteristiek(self):
        """

        :return:
        """
        fmean = self.stone.f_mean
        fbo = self.druksterkte_genormaliseerde_gemiddelde
        fm = self.mortar.group
        mortel = self.mortar.kind
        groep = self.stone.group
        materiaal = self.stone.kind

        if mortel == 'algemeen':
            coefalfa = 0.65
            coefbeta = 0.25
            if (groep == 'groep 2' and materiaal != 'cellenbeton') or (groep == 'groep 1' and materiaal == 'baksteen'):
                coefK = 0.5
            elif materiaal == 'baksteen' and groep == 'groep 3':
                coefK = 0.4
            elif materiaal != 'baksteen' and groep == 'groep 1':
                coefK = 0.6
            elif materiaal == 'kalkzandsteen' and groep == 'groep 3':
                coefK = 0.45
            if materiaal == 'baksteen' and groep != 'groep 1':
                fnorm = fmean
            else:
                fnorm = fbo

        if mortel == 'lijm':
            coefbeta = 0
            if materiaal == 'baksteen' and groep != 'groep 1':
                fnorm = fmean
                coefalfa = 0.8
            if materiaal != 'baksteen' and groep == 'groep 1':
                coefK = 0.8
            elif materiaal == 'baksteen' and groep == 'groep 2':
                coefK = 0.5
            elif materiaal == 'kalkzandsteen' and groep == 'groep 2':
                coefK = 0.65
            elif materiaal == 'betonsteen' and groep == 'groep 2':
                coefK = 0.55
            elif materiaal == 'baksteen' and groep == 'groep 3':
                coefK = 0.4
            elif materiaal == 'kalkzandsteen' and groep == 'groep 3':
                coefK = 0.5

        karakteristieke_sterkte = (coefK * (fnorm ** coefalfa) * (fm ** coefbeta))
        return round(karakteristieke_sterkte, 2)

    @property
    def conditioneringsfactor(self):
        return STONE_CONDITIONINGFACTOR[self.stone.kind]

    @property
    def veiligheidsfactor(self):
        N = [2.5, 2.8, 3.5]
        S = [2, 2.3, 3]
        mats = {'stenen van categorie I en mortel, beiden met bijkomende productcertificatie': 0,
                'stenen van categorie I zonder bijkomende productcertificatie en willekeurige mortel': 1,
                'stenen van categorie II met willekeurige mortel': 2}
        if self.supervision == 'normaal':
            Ym = N[mats[self.application]]
        elif self.supervision == 'uitgebreid':
            Ym = S[mats[self.application]]
        return Ym

    @property
    def sterkte_rekenwaarde(self):
        return round(self.sterkte_karakteristiek / self.veiligheidsfactor, 2)

    # }}}

    def next_low(self, seq, x):
        print(min([(x - i, i) for i in seq if x >= i] or [(0, None)]))

    def interpoleren(self, y1, y2, x, x1, x2):
        return y1 + (((x - x1) / (x2 - x1)) * (y2 - y1))


    def output(self):
        """
        :return: properties of masonry, stone and mortar
        :rtype: dict
        """
        return {'masonry': {'application': self.application,
                            'supervision': self.supervision,
                            'stone': {**self.stone.output()},
                            'mortar': {**self.mortar.output()},
                            'output': {
                                'fb [N/mm/mm]': self.druksterkte_genormaliseerde_gemiddelde,
                                'fk [N/mm/mm]': self.sterkte_karakteristiek,
                                'fd [N/mm/mm]': self.sterkte_rekenwaarde,
                                'veiligheidsfactor': self.veiligheidsfactor,
                                'conditioneringsfactor': self.conditioneringsfactor,
                                'vormfactor': self.vormfactor,
                                }
                            }
                }


if __name__ == '__main__':
    brick = Masonry(stone_height=190, stone_width=140, stone_length=290, stone_kind='baksteen', stone_fmean=15, stone_group='groep 1',
                    mortar_kind='algemeen', mortar_group=12,
                    application='stenen van categorie II met willekeurige mortel', supervision='normaal')

    pprint(brick.output())

    new_stone = Stone(height=190, width=140, length=290, kind='baksteen', f_mean=25, group='groep 3')

    brick.stone = new_stone

    pprint(brick.output())






