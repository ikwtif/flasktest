import functies
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

from pprint import pprint
from nagels import Nagels

#################
# verbinding checken beide zijden? - input voor verbindingsmiddel?

class VerbindingenHout():
    """
    NBN EN 1995-1-1:2005+AC:2006 (NL)
    """
    def __init__(self, member_kop, member_punt, verbinding_middel, member_midden=None, verbinding_krachten=None):
        """
        :param member_kop: element zijde kop verbindingsmiddel
        :param member_punt: element zijde punt verbindingsmiddel
        :param verbinding_middel: verbindingsmiddel
        :param member_midden: element zijde midden verbindingsmiddel
        :param verbinding_krachten: krachten op verbinding
        """
        self.member_kop = member_kop
        self.member_punt = member_punt
        self.verbinding_middel = verbinding_middel
        self.member_midden = member_midden
        self.memberCheck()
        self.snede_enkel = True
        if self.member_midden is not None:
            self.snede_enkel = False
        self.verbinding_krachten = verbinding_krachten
        self.verbinding_type = None
        self.typeCheck()


    def memberCheck(self):
        """
        Raises error voor verkeerde member input
        """
        if self.member_kop.zijde != 'kop':
            raise ValueError(f'member {self.member_kop} heeft zijde self.member_kop.zijde maar moet kop zijn')
        if self.member_punt.zijde != 'punt':
            raise ValueError(f'member {self.member_punt} heeft zijde self.member_punt.zijde maar moet punt zijn')
        if self.member_midden is not None and self.member_midden.zijde != 'midden':
            raise ValueError(f'member {self.member_midden} heeft zijde self.member_midden.zijde maar moet midden zijn')


    def typeCheck(self):
        """
        Stelt type verbinding vast
        """
        #andere elementen checken?
        #plaat op hout?
        if self.member_kop.materiaal == 'staal':
            self.verbinding_type = 'staal-op-hout'
        elif self.member_kop.materiaal == 'hout'and self.member_kop.hout_type not in ['multiplex', 'spaanplaat', 'hardboard', 'osb']:
            self.verbinding_type = 'hout-op-hout'
        elif self.member_kop.materiaal == 'hout'and self.member_kop.hout_type in ['multiplex', 'spaanplaat', 'hardboard', 'osb']:
            self.verbinding_type = 'plaat-op-hout'


    def berekeningSterkte(self, verbinding_middel, verbinding_krachten):
        """
        8.1.2 Verbindingen met meer dan een verbinding_middel
        """
        logging.info('berekening sterkte volgens 8.1.2')
        Fv_ef = Nef * Fv_Rk

        afschuif_el1 = self.afschuivingElement(data)
        afschuif_el2 = self.afschuivingElement(data)

        return Fv_ef


    def uittrekSterkte(self):
        """
        Berekening uittreksterkte
        :return: uittreksterkte
        """
        logging.info('berekening uittreksterkte')

        uittreksterkte = self.verbinding_middel.uittrekSterkte(self.member_punt, self.member_kop)

        return uittreksterkte


    def stuikSterkte(self):
        """
        Berekening stuiksterkte voor ALLE elementen voor het verbindingsmiddel
        """
        logging.info('berekening stuiksterkte voor alle elementen voor het verbindingsmiddel')

        if self.member_kop.materiaal != 'staal':
            self.stuiksterkte_kop = self.verbinding_middel.stuiksterkteHout(member=self.member_kop,
                                                                            verbinding_krachten=self.verbinding_krachten)
        if self.member_kop.materiaal != 'staal':
            self.stuiksterkte_punt = self.verbinding_middel.stuiksterkteHout(member=self.member_punt,
                                                                             verbinding_krachten=self.verbinding_krachten)
        if self.member_midden is not None and self.member_midden != 'staal':
            self.stuiksterkte_midden = self.verbinding_middel.stuiksterkteHout(member=self.member_kop,
                                                                               verbinding_krachten=self.verbinding_krachten)
            stuiksterkte = [self.stuiksterkte_kop, self.stuiksterkte_midden, self.stuiksterkte_punt]
        else:
            stuiksterkte = [self.stuiksterkte_kop, self.stuiksterkte_punt]

        return stuiksterkte


    def afschuivingElement(self):
        """
        8.2 Sterkte van op afschuiving belaste stiftvormige metalen verbinding_middelen
        Karakteristieke sterkte
        ------------------------------------------------------
        KLEINSTE WAARDE (PER SNEDE EN PER VERBINDINGSMIDDEL)
        ------------------------------------------------------
        """
        logging.info('berekening afschuiving')
        #karakteristieke sterkte berekenen
        uittreksterkte = self.uittrekSterkte()
        self.stuikSterkte()

        if self.verbinding_type == 'hout-op-hout' or self.verbinding_type == 'plaat-op-hout':
            sterkte_kar = functies.afschuivingHoH(snede=self.snede_enkel,
                                    member_kop=self.member_kop,
                                    member_punt=self.member_punt,
                                    member_midden=self.member_midden,
                                    verbinding_middel=self.verbinding_middel,
                                    stuiksterkte_1k=self.stuiksterkte_kop,
                                    stuiksterkte_2k=self.stuiksterkte_punt,
                                    uittreksterkte=uittreksterkte)

        elif self.verbinding_type == 'staal-op-hout':
            # stuiksterkte bepalen enkel van houten deel
            sterkte_kar = functies.afschuivingSoH(snede=self.snede_enkel,
                                member_kop=self.member_kop,
                                member_punt=self.member_punt,
                                verbinding_middel=self.verbinding_middel,
                                stuiksterkte=self.stuiksterkte_punt,
                                uittreksterkte=uittreksterkte)
        else:
            sterkte_kar = None
        return sterkte_kar



if __name__ == '__main__':
    from nagels import Nagels
    from members import Member

    verbindingskrachten= {'Alfa': 1.57,
                            'AlfaTrek': 0,
                            'Rad': 1.57,
                            'RadTrek': 0
                            }

    member_staal = Member(materiaal='staal', dikte=5, zijde='kop', treksterkte=235, hechtlengte=4)
    member_hout = Member(materiaal='hout', dikte=71, zijde='kop', hout_type='osb', ro=320, kmod=0.9, fc=2.2, hechtlengte=56)
    member_hout_2 = Member(materiaal='hout', dikte=71, zijde='punt', hout_type='loofhout', ro=320, kmod=0.9, fc=2.2, hechtlengte=56)
    nagel = Nagels(materiaal='nagel', nagel_type='glad', diameter=7, lengte=100, treksterkte=235, uitvoering='glad', kop_type='rond',
                   kop_diameter=14, fax=2.05, fhead=7.17)

    print(member_hout)
    print(member_hout_2)
    print(nagel)
    #verb = VerbindingenHout(member_kop=member_staal, member_punt=member_hout, verbinding_middel=nagel, verbinding_krachten=verbindingskrachten)
    verb = VerbindingenHout(member_kop=member_hout, member_punt=member_hout_2, verbinding_middel=nagel,
                            verbinding_krachten=verbindingskrachten)

    print('test', verb.afschuivingElement())
    print(verb.__dict__)