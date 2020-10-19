


class Member():
    def __init__(self, materiaal, dikte, zijde, **properties):
        """
        :param materiaal: hout of staal
        :param dikte: dikte element
        :param zijde: ten opzichte van verbindingsmiddel [kop, punt, midden]
        :param properties: eigenschappen specifiek element
        """
        self.materiaal = materiaal
        self.dikte = dikte
        self.zijde = zijde
        if materiaal == 'hout':
            # ** unpacks kwargs
            self.initialize_hout(**properties)
        elif materiaal == 'staal':
            self.initialize_staal(**properties)
        else:
            print(f'verkeerd materiaal: {materiaal}')


    def initialize_hout(self, hout_type, ro, kmod, fc, hechtlengte):
        self.hout_type = hout_type
        self.ro = ro
        self.kmod = kmod
        self.fc = fc
        self.hechtlengte = hechtlengte
        self.plaat = False
        if hout_type in ['multiplex', 'spaanplaat', 'osb', 'hardboard']:
            self.plaat = True

    def initialize_staal(self, treksterkte, hechtlengte):
        self.treksterkte = treksterkte
        self.hechtlengte = hechtlengte



if __name__ == '__main__':
    '''
    materiaal = 'staal'
    dikte = 5
    treksterkte = 235
    hechtlengte = 4
    
    stalen = Member(materiaal, dikte, treksterkte, hechtlengte)
    print(stalen.__dict__)
    '''
    stalen2 = Member(materiaal='staal', dikte=5, treksterkte=235, hechtlengte=4)
    print(stalen2.__dict__)