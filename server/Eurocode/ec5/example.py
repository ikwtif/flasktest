import functions


class Joint():
    def __init__(self, joint):
        # loads all parameters based on joint specifications (elements of joint, powers on joint, connection medium)
        self.element1 = joint['Element 1']
        self.element2 = joint['Element 2']
        self.type()

    def type(self):

    # sets type of the joint based on elements

    def shearForce(self, jointMedium, jointForces):
        # filters what functions to use based on conection medium and joint type and, for example, loads Nails(jointMedium) in this case
        # calculates several properties for connection medium
        # calculates strength joint based on shear and properties of joint + connection medium
        # final calculations imported from separate function.py file
        ''' EXAMPLE
        if jointMedium == 'nails':
            medium_func = Nails(jointMedium)
            if self.element1['kind'] == 'steel':
                someForce = medium_func.shearForce(self.element1, self.element2, jointForce)
        if self.type =='something':
            someOtherForce : medium_func.someOtherForce(self.type, self.element1, self.element2)

        forceTotal = functions.somefunction(self.type, self.element1, self.element2, someForce, someOtherForce)
        '''


class Nails():
    def __init__(self, jointMedium):

    # loads connection medium properties

    def K90(self, element):

    # calculation of element based on medium

    def checkPreDrill(self, jointType, element1, element2):

    # same as K90

    def someForce(self, jointType, element1, element2, jointForces):

    # calculationsbased on elements and nail properties

    def someOtherFroce(self, element1, element2):
# calculations based on elements and nail properties