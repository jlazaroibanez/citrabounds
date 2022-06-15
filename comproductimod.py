#! /usr/bin/env python
#Test kinetic model of E. coli plus citramalate reaction with different glucose feeds
from __future__ import division, print_function
from ecolicitra import ecolicit, mmCITRA, mmGLC
import matplotlib.pyplot as plt
import numpy as np
import roadrunner
import libsbml

import numpy as np
from scipy.optimize import differential_evolution, rosen
import pyade.sade
import math
import functools as ft
import sys
import timeit


# Class to modify the model to the given values of the compounds
class Multisimulator:
	# init the class with the target compounds and the model
	def __init__(self, model, compounds_vmax_dict, negate,
				 objective_f = "citraprod", f_args = {}):
		# Model and start values
		self.model = model
		self.comp_dict = compounds_vmax_dict
		# Negate if needed
		self.set_negative(negate)
		# Select the objective function
		self.select_objective_function(objective_f, f_args)


	# Set the negative value for the objective function
	def set_negative(self, negate):
		self.__n = negate*(-1) + (not negate)

	# Select a objective function
	def select_objective_function(self, objective_f, f_args):
		if objective_f == "citraprod":
			self.objective_f = self.model.comproducti
		elif objective_f == "flux":
			self.objective_f = ft.partial(self.model.reacflux,
										  f_args["target_reacs"])  ## esto no lo entiendo
		else:
			raise Exception('Unknown function\"' + str(objective_f) + '\".')


	# Return the citramalate prod given the Vmax value for the compounds
	def target_value(self, vs):
		# Iterate over compounds and values, setting the new value
		for (c, w), v in zip(self.comp_dict.items(), vs):  # comp_dict es un diccionario con id_reaction: Vmax, vs es una lista con valores random que se generan
			self.model.setVmax(c, w*v)   # que son los dos argumentos de la función setVmax de ecolicitra.py
		# Value of the objective function
		try:
			# Return the objective function negated if needed
			return self.__n * self.objective_f()
		except Exception as e:
			# If fails in convergence, returns the highest value
			return math.inf


# Find the optimal values for the compounds and their Vmax in wild indicated
# in <<compvmaxdict>> for the model <<model>>
def optimalcomp(model, compvmaxdict, maximize = True, function = "citraprod",
				lbound = 0.3, ubound = 10.0, step=0.1, f_args = {}):
	if not isinstance(compvmaxdict, dict):
		raise(TypeError("compvmaxdict is " + str(type(compvmaxdict)) \
			  + ", not a dict"))
	if not isinstance(model, ecolicit):
		raise(TypeError("compvmaxdict is " + str(type(model)) \
			  + ", not a ecolicit"))
	
	# Parameters
	D = len(compvmaxdict)			# Dimensions of the problem
	NP = 28							# Population size
	F = 0.6607						# Mutation constant or differential weight
	CR = 0.9426						# Recombination or crossover probability
	max_iter = 100					# Max number of iterations
	# Bounds of the problem (given in times the initial value)
	varbounds = np.array(D * [[lbound, ubound]])
	
	# Model multiple times simulator
	tester = Multisimulator(model, compvmaxdict, negate = maximize,
							objective_f = function, f_args = f_args)

	SaDE_algorithm = pyade.sade
	params = SaDE_algorithm.get_default_params(dim=D)
	params["bounds"] = varbounds
	params["func"] = tester.target_value
	solution, fitness = SaDE_algorithm.apply(**params)


	# Finds the optimal for the compound with the genetic algorithm
	return differential_evolution(func = tester.target_value,
								bounds = varbounds,
								mutation = F,
								recombination = CR,
								popsize = NP,
								maxiter = max_iter,
								disp = True,
								updating = 'deferred',
								workers = -1
								)

def argument_parser(argv):
	# Argument extractor
	parsed_args = {"compound2test": '-a',
					"all_reac": False,
					"maximize": True,
					"model_file": 'model_file.xml',
					"target_f": "citraprod",
					"f_arguments": {},
					"wild": False
					}
	i = 0
	while i < len(argv):   # argv son los parámetros que le paso yo en la terminal
		if argv[i] == '-m':		# Model given
			if len(argv) > i+1:
				parsed_args['model_file'] = argv[i+1]
				i += 1
			else:
				print('Model file not specified')
				sys.exit(1)
		elif argv[i] == '-a':	# All reactions
			parsed_args['all_reac'] = True
		elif argv[i] == '-n':	# Minimize
			parsed_args['maximize'] = False
		elif argv[i] == '-f':	# Target function selection
			if len(argv) > i+1:
				parsed_args['target_f'] = argv[i+1]
				i += 1
			else:
				print('Function not specified')
				sys.exit(1)
		elif argv[i] == '-p':	# Parameter indication
			if len(argv) > i+2:
				parsed_args['f_arguments'][argv[i+1]] = argv[i+2]
				i += 2
			else:
				print('Wrong parameter specification: -p parameter_name value')
				exit(1)
		elif argv[i] == '-w':	# Wild type
			parsed_args['wild'] = True
		else:
			parsed_args['compound2test'] = argv[i].replace(' ', '')\
												  .split(',')
		i += 1			# Next argumet

	return parsed_args

# parsed_args = argument_parser(sys.argv[1:])

if __name__ == '__main__':
	# Parse the arguments
	parsed_args = argument_parser(sys.argv[1:])

	# Parameters of kinetic model
	ecit = ecolicit(include_CITRA = True, sbmlfile = parsed_args['model_file'])    ### ecit sería el copy_object de la clase??
	ecit.setVmax('CITRA_SYN', 4.0)
	ecit.time0 = 0
	ecit.timef = 2*3600 # final simulation time in seconds
	ecit.npoints = 1000  # Number of points to be computed in the simulation

	if parsed_args['all_reac']:		# All reactions used
		compound2test = ecit.reacVmaxes
	else:
		compound2test = parsed_args['compound2test']

	if not parsed_args['wild']:		# No wild type (optimization)
		# Extract Vmaxes in wild ant set it as dictionary
		wildVmaxes = dict(zip(ecit.reacVmaxes, ecit.iniVmaxes))

		# Extract wild values of Vmax
		vmax2test = np.array([wildVmaxes[key] for key in compound2test])
		compVmax2test = dict(zip(compound2test, vmax2test))

		# Estimate the optimus value
		optresult = optimalcomp(compvmaxdict = compVmax2test,
								model = ecit,
								maximize = parsed_args['maximize'],
								function = parsed_args['target_f'],
								f_args = parsed_args['f_arguments'])

		# Prints the result
		optcompVmax = dict(zip(compound2test, vmax2test*optresult.x))
		optcompVmaxrelation = dict(zip(compound2test, optresult.x))
		print("Optimus Vmax: ", optcompVmax,
			  "\n\tWild multiply: ", optcompVmaxrelation, 
			  "\n", parsed_args['target_f']," with ",
			  parsed_args["f_arguments"], ":", 
			  ((-1)*parsed_args['maximize']+(not parsed_args['maximize']))\
				  *optresult.fun)

	else:	# No optimization
		# Extract Vmaxes in wild ant set it as dictionary
		wildVmaxes = dict(zip(ecit.reacVmaxes, ecit.iniVmaxes))

		# Extract wild values of Vmax
		vmax2test = np.array([wildVmaxes[key] for key in compound2test])
		compVmax2test = dict(zip(compound2test, vmax2test))
		res = Multisimulator(ecit,
								compounds_vmax_dict= compVmax2test,
								negate = parsed_args['maximize'],
								objective_f = parsed_args['target_f'],
								f_args = parsed_args['f_arguments'])\
									.target_value([1]*len(compound2test))
		print("The ",parsed_args['target_f'], " value is :",
				((-1)*parsed_args['maximize']+(not parsed_args['maximize']))\
					*wild_res)


