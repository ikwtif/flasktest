

class BaseMaterial:
    """
    Class represents materials
    """
    # N/m/m/m
    weight_density = None
    # safety factor
    gamma = None

    def __init__(self):
        #self.m = None
        pass

    @property
    def w(self):
        return self.weight_density

    @property
    def m(self):
        m = self.weight_density * 9.81
        return m

    def safety_factor(self, ontwerp_situatie, grenstoestand):
        return self.gamma[ontwerp_situatie][grenstoestand]




