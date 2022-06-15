from __future__ import division, print_function
import libsbml
import roadrunner
import math
from cobra.flux_analysis import flux_variability_analysis
import cobra
import pandas as pd
import os

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

# Reading .xlsx file 

ex_data = pd.read_excel('./Flux_bounds_mapping.xlsx')
# print(ex_data)

list(ex_data["Stochiometric"])
stoich_reactions = [x for x in ex_data["Stochiometric"] if str(x) != 'nan']

list(ex_data["Kinetic"])
kin_reactions = [x for x in ex_data["Kinetic"] if str(x) != 'nan']

## Glucose feed
solutions = []
growth_fluxes = []

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g  

# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Glucose feed distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Glucose metabolism

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")
const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function

C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[6:18], def_bounds[6:18]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[6:18], def_bounds[6:18]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution
solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Glucose metabolism distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# PPP

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")
const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[18:26], def_bounds[18:26]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[18:26], def_bounds[18:26]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('PPP distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# TCA cycle

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[31:41], def_bounds[31:41]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[31:41], def_bounds[31:41]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('TCA cycle distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# OXPHOS

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[46:49], def_bounds[46:49]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[46:49], def_bounds[46:49]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('OXPHOS distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Exchange reactions

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")
const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function

C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[:4], def_bounds[:4]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[:4], def_bounds[:4]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Exchange reactions distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Glucose uptake

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

lb = const_model.reactions.get_by_id(cleanedList3[4]).lower_bound = def_bounds[4]

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

ub = const_model.reactions.get_by_id(cleanedList3[4]).upper_bound = def_bounds[4]

# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Glucose uptake distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Pi uptake

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

lb = const_model.reactions.get_by_id(cleanedList3[5]).lower_bound = def_bounds[5]

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

ub = const_model.reactions.get_by_id(cleanedList3[5]).upper_bound = def_bounds[5]

# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Pi uptake distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Additional reactions for nucleotides and redox cofactor

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[49:52], def_bounds[49:52]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[49:52], def_bounds[49:52]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Additional reactions for nucleotides and redox cofactor distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# ED pathway

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")

const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function
C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[26:28], def_bounds[26:28]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[26:28], def_bounds[26:28]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('ED pathway distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Anapletoric reactions

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")
const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function

C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[28:31], def_bounds[28:31]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[28:31], def_bounds[28:31]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Anapletoric reactions distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)

# Glyoxylate shunt

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")
const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function

C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[41:43], def_bounds[41:43]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[41:43], def_bounds[41:43]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Glyoxylate shunt distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)


# Acetate metabolism

# Reading the constraint-based model with the citramalate production and transport reactions

const_model = cobra.io.read_sbml_model("MODEL1108160000CITRA.xml")
const_model.objective = "CIMA" # Set citramalate synthesis reaction as objective function

C = 6.372 # Constant for conversion from one model to the other
gamma = -1
g = 0.23

# Set glucose feed conditions
gluc_lb = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").lower_bound = gamma*C*g
gluc_ub = const_model.reactions.get_by_id("EX_glc_LPAREN_e_RPAREN_").upper_bound = gamma*C*g

# Table processing

int_reac = []
def_bounds = []

new_min_bounds = list(ex_data["Lower bound.1"])
cleanedList1 = [x for x in new_min_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Lower bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[43:46], def_bounds[43:46]):
    
    lb = const_model.reactions.get_by_id(i).lower_bound = j

# Table processing

int_reac = []
def_bounds = []

new_max_bounds = list(ex_data["Upper bound.1"])
cleanedList1 = [x for x in new_max_bounds if str(x) != 'nan']
for i in cleanedList1:
    if i != 0:
        def_bounds.append(i)

for c, element in zip(ex_data["Stochiometric"], ex_data["Upper bound.1"]):
    if element != 0:
        int_reac.append(c)

cleanedList3 = [x for x in int_reac if str(x) != 'nan']

# Set lower bounds for each reaction in the subsystem

for i, j in zip(cleanedList3[43:46], def_bounds[43:46]):

    ub = const_model.reactions.get_by_id(i).upper_bound = j
    
# Set kinetic bounds for the biomass reaction

lb_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').lower_bound = 0.00167469505003442*0.5  # 
ub_growth = const_model.reactions.get_by_id('Ec_biomass_iJO1366_WT_53p95M').upper_bound = 0.00167469505003442

# FBA solution

solution = const_model.optimize()
solutions.append(solution.objective_value)

# FVA and range between maximum and minimum flux 

difl = []

mini = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).minimum)
maxi = list(flux_variability_analysis(const_model, const_model.reactions, fraction_of_optimum = 0.99).maximum)


for i, j, x in zip(mini, maxi, const_model.reactions):
    
    if i <= 0:
        dif = abs(j - abs(i))
    
    if i <= 0 and j <= 0:
        dif = abs(abs(abs(j)) - abs(i))
        
    else:  
        dif = abs(j - i)

    difl.append(dif)
    
# Count the reactions in each group depending on the range

count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0

for dif in difl:    
    
    
    if 0 <= dif < 1:
        count_1 += 1
    
    if 1 <= dif < 10:
        count_2 += 1

    if 10 <= dif < 50:
        count_3 += 1

    if 50 <= dif < 100:
        count_4 += 1
    
    if 100 <= dif < 1000:
        count_5 += 1
    
    if dif >= 1000:
        count_6 += 1
    

print('Acetate metabolism distribution: ', count_1, count_2, count_3, count_4, count_5, count_6)


print(solutions)
