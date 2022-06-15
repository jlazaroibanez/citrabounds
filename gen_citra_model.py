from __future__ import division, print_function
import numpy as np
import cobra
from cobra import Reaction, Metabolite
from fnyzer import FNFactory, cobra2fn

def loadEcolimodel(filename = "MODEL1108160000", name = "EcolicitFN", solver = "cplex"):
    #### Parameters
    # filename: file with the SBML model
    # name: name of the FN
    # solver: solver to be used
    model = cobra.io.read_sbml_model(filename+'.xml')
    biomass_reaction = 'Ec_biomass_iJO1366_core_53p95M'
    Ecolicobramodel = cobra.io.read_sbml_model(filename+'.xml')
    addCimA(Ecolicobramodel) # Add synthesis, transport and exchange of citramalate
    cobra.io.write_sbml_model(Ecolicobramodel, filename+'CITRA.xml')
    # fnet = cobra2fn(Ecolicobramodel) # Build Flexible Net
    # fnet['name'] =  name
    # fnet['solver'] = solver
    # return fnet


def addCimA(model):
    """Add CimA reaction and sink for citramalate to cobra model"""
    reaccima = Reaction('CIMA')
    reaccima.name = '(R)-Citramalate production'
    reaccima.lower_bound = 0.0
    reaccima.upper_bound = 1000.0
    # reaccima.objective_coefficient = 0.0
    
    """CIMA reaction"""
    pyr_c = model.metabolites.get_by_id("pyr_c") # Pyruvate
    accoa_c = model.metabolites.get_by_id("accoa_c") # Acetyl-CoA
    h2o_c = model.metabolites.get_by_id("h2o_c") # H2O
    citramalate_c = Metabolite(
        'citramalate_c',
        formula='C5H6O5',
        name='(R)-citramalate',
        charge=-2,
        compartment='c')
    coa_c = model.metabolites.get_by_id("coa_c") # CoA
    h_c = model.metabolites.get_by_id("h_c") # H+
    
    reaccima.add_metabolites({pyr_c: -1.0,
                              accoa_c: -1.0,
                              h2o_c: -1.0,
                              citramalate_c: 1.0,
                              coa_c: 1.0,
                              h_c: 1.0})
    reaccima.gene_reaction_rule = 'CimA37'     
#    print(reaccima.reaction)                          
#    print(reaccima.genes)                          
    model.add_reaction(reaccima)
    
    
    """Transport1 for Citramalate"""
    reactransp_1 = Reaction('CitraTransp1')
    reactransp_1.name = 'Citramalate Transport from cytoplasm to periplasm'
    reactransp_1.lower_bound = 0.0
    reactransp_1.upper_bound = 1000.0    
    # reaccisink.objective_coefficient = 0.0    
    
    citramalate_c = model.metabolites.get_by_id("citramalate_c") # Citramalate
    citramalate_p = Metabolite(
        'citramalate_p',
        formula='C5H6O5',
        name='(R)-citramalate_p',
        charge=-2,
        compartment='p')
    
    reactransp_1.add_metabolites({citramalate_c: -1.0,
                                citramalate_p: 1.0})
#    print(reacTransp.reaction)                          
#    print(reacTransp.genes)                          
    model.add_reaction(reactransp_1)
    
    """Transport2 for Citramalate"""
    reactransp_2 = Reaction('CitraTransp2')
    reactransp_2.name = 'Citramalate Transport from periplasm to the extracellular space'
    reactransp_2.lower_bound = -1000.0
    reactransp_2.upper_bound = 1000.0    
    # reaccisink.objective_coefficient = 0.0    
    
    citramalate_p = model.metabolites.get_by_id("citramalate_p") # Citramalate
    citramalate_e = Metabolite(
        'citramalate_e',
        formula='C5H6O5',
        name='(R)-citramalate_e',
        charge=-2,
        compartment='e')
    
    reactransp_2.add_metabolites({citramalate_e: -1.0,
                                citramalate_p: 1.0})
#    print(reacTransp.reaction)                          
#    print(reacTransp.genes)                          
    model.add_reaction(reactransp_2)
    
    """Exchange reaction for Citramalate"""    
    reaccEX = Reaction('EX_Citramalate')
    reaccEX.name = 'Exchange reaction to allow (R)-Citramalate to leave the system'
    reaccEX.lower_bound = 0.0
    reaccEX.upper_bound = 1000.0
    # reaccisink.objective_coefficient = 0.0
    
    reaccEX.add_metabolites({citramalate_e: -1.0})
#    print(reaccisink.reaction)                          
#    print(reaccisink.genes)                          
    model.add_reaction(reaccEX) 

loadEcolimodel(filename = "MODEL1108160000", name = "EcolicitFN", solver = "cplex")
