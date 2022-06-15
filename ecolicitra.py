#! /usr/bin/env python
#Class for SBML kinetic model of E. coli plus reaction for the production of citramalate
from __future__ import division, print_function
import roadrunner
import libsbml

mmCITRA = 146.098 # g/mol # Molecular mass of Citramalate https://pubchem.ncbi.nlm.nih.gov/compound/5460281
mmGLC = 180.156 # g/mol  # Molecular mass of Glucose https://pubchem.ncbi.nlm.nih.gov/compound/79025


class ecolicit:
    """SBML model of E. coli plust reaction for citramalate synthesis"""

    def __init__(self, copy_object = None, sbmlfile = "E_coli_Millard2016.xml", Vmax = 4.0, Km = 0.495, include_CITRA = True, initial_CITRA = 0.0):   # estos son parámetros que se utilizan después en los métodos de la clase
        """
        sbmlfile: SBML file with the model
        Vmax: Vmax of the citramalate synthesis reaction (mM/s)
        Km: Km of the citramalate synthesis reaction (mM)
        include_CITRA: Include citramalate species in the model (notice that it grows monotonically and hence it should not be included for steady state analysis)
        ininitial_CITRA: Initial concentration of citramalate (mM)
        """
        if copy_object: 
            if isinstance(copy_object, ecolicit):   # Copy object is a ecolicit   ## y estos son los argumentos del método que no son obligatorios
                self.document = copy_object.document.clone()
                self.model = self.document.getModel()
                self.iniVmaxes = copy_object.iniVmaxes.copy()
                self.reacVmaxes = copy_object.reacVmaxes.copy()
                self.time0 = copy_object.time0
                self.timef = copy_object.timef
                self.npoints = copy_object.npoints
            elif isinstance(copy_object, list):      # Copy object is a list
                libsbml.readSBMLFromString
                self.document = libsbml.readSBMLFromString(copy_object[0])
                self.model = self.document.getModel()
                self.iniVmaxes = copy_object[1]
                self.reacVmaxes = copy_object[2]
                self.time0 = copy_object[3]
                self.timef = copy_object[4]
                self.npoints = copy_object[5]
        else:
            reader = libsbml.SBMLReader()
            self.document = reader.readSBMLFromFile(sbmlfile)
            self.model = self.document.getModel()
    #        print("Number of species: ", self.model.getNumSpecies())
    #        print("Number of reactions: ", self.model.getNumReactions())
        
            # Create species that models growth. The growth rate will be equal to
            # the derivative of the species concentration
            igrowth = self.model.createSpecies()
            igrowth.setId('iGROWTH')
            igrowth.setName('iGROWTH')
            igrowth.setCompartment('cell')
            igrowth.setConstant(False)
            igrowth.setInitialConcentration(0.0)
            igrowth.setBoundaryCondition(False)
            igrowth.setHasOnlySubstanceUnits(False)
        
            growthr = self.model.getReaction('GROWTH')  ## no entiendo esta parte
            spig = growthr.createProduct()  # spig es la speciesreference
            spig.setSpecies("iGROWTH")

            # Create citramalate species
            if include_CITRA:
                citra = self.model.createSpecies()
                citra.setId('CITRA')
                citra.setName('CITRA')
                citra.setCompartment('cell')
                citra.setConstant(False)
                citra.setInitialConcentration(initial_CITRA)
                citra.setBoundaryCondition(False)
                citra.setHasOnlySubstanceUnits(False)
        
            # Create reaction for citramalate synthesis
            citrasyn = self.model.createReaction()
            citrasyn.setId("CITRA_SYN")
            citrasyn.setName("CITRA_SYN");
        
            spr1 = citrasyn.createReactant()
            spr1.setSpecies("ACCOA")
            spr2 = citrasyn.createReactant()
            spr2.setSpecies("PYR")
            spr3 = citrasyn.createReactant()
            spr3.setSpecies("H2O")
            spp1 = citrasyn.createProduct()
            spp1.setSpecies("COA")
            spp2 = citrasyn.createProduct()
            spp2.setSpecies("Hin")
            if include_CITRA:
                spp3 = citrasyn.createProduct()
                spp3.setSpecies("CITRA")
        
            kl = citrasyn.createKineticLaw()
            para = kl.createParameter()
            para.setId("Vmax")
            para.setValue(Vmax)
            para = kl.createParameter()
            para.setId("Km")
            para.setValue(Km)
            math_ast = libsbml.parseL3Formula('(Vmax * ACCOA) / (ACCOA + Km)')
            kl.setMath(math_ast)

            # Vmaxes of the reactions
            self.getVmaxes()

    # For pickle serialization purposes
    def __reduce__(self):
        return (self.__class__, 
               ([libsbml.writeSBMLToString(self.document),
                self.iniVmaxes.copy(),
                self.reacVmaxes.copy(),
                self.time0, 
                self.timef,
                self.npoints],))

    def writeToFile(self, filename = "E_coli_Millard2016_CITRA.xml"):
        libsbml.writeSBMLToFile(self.document, filename)

    def setFEED(self, value):
        # value: mmol/s of glucose fed into the extracellular compartment.
        # Notice that the volume of the extracellular compartment is 100l, thus
        # the increase in concentration of glucose produced by the feed in the
        # extracellular glucose is value/100 mM/s
        self.model.getParameter('FEED').setValue(value)
        
    def getFEED(self):
        # see setFEED for info about units
        return self.model.getParameter('FEED').getValue()
        
    def setVmax(self, reacId, value):
        # Units: mM/s
        p = self.model.getReaction(reacId).getKineticLaw().getParameter('Vmax')
        if p:
            p.setValue(value)
                    
    def getVmax(self, reacId):
        # get Vmax of reaction reacId. See setVmax for info about units
        p = self.model.getReaction(reacId).getKineticLaw().getParameter('Vmax')
        if p:
            return p.getValue()

    def getVmaxes(self):
        # get Vmaxes of reactions. See setVmax for info about units
        Vmaxes = {}
        for reac in self.model.getListOfReactions():
            vm = self.getVmax(reac.id)
            if vm:
                Vmaxes[reac.id] = vm
        self.reacVmaxes = sorted(Vmaxes) # ids of reactions sorted alphabetically that have Vmax
        self.iniVmaxes = [Vmaxes[r] for r in self.reacVmaxes] # initial values of Vmax (as in the kinetic model)

    def reacflux(self, selection = "CITRA"):
        # Compute steady state flux
        rr = roadrunner.RoadRunner(libsbml.writeSBMLToString(self.document))
        rr.timeCourseSelections = [selection]
        result = rr.simulate(self.time0, self.timef, self.npoints)
        return result[-1][0]

    def comproducti(self):
        # Compute steady state productivity
        selection = ["CITRA", "iGROWTH"]
        rr = roadrunner.RoadRunner(libsbml.writeSBMLToString(self.document))
        rr.timeCourseSelections = selection
        result = rr.simulate(self.time0, self.timef, self.npoints)
        Y_PS = (result[-1,selection.index("CITRA")]*mmCITRA)/(self.getFEED()*self.timef*mmGLC)
        mu = result[-1,selection.index("iGROWTH'")]*3600
        return mu*Y_PS

