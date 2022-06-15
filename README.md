# citrabounds

The citrabounds github repository contains the files used in my Master's Thesis: "ENRICHMENT OF METABOLIC CONSTRAINT-BASED MODELS USING KINETIC INFORMATION". 

1. ecolicitra.py: This .py file defines the functions that are subsequently executed by the
comproductimod.py script. It contains functions related to the kinetic model analysis and the
implementation of the citramalate production reaction, as well as the Vmax extraction from
each reaction.

2. comproductimod.py: This .py file executes the methods defined in ecolicitra.py. It also
includes a differential evolution algorithm that finds the optimal citramalate productivity varying
the V max of each selected reaction.

3. gen_citra_model.py: This .py file allows editing the original constraint-based model and
adds for citramalate production-related reactions: "R_CIMA", two transport reactions
"R_CitraTransp1" and "R_CitraTransp2", and "R_EX_Citramalate".

4. fba_citra_max.py: .py file that initially sets the minimum and maximum bounds of the
MODEL1108160000 to the differential evolution-computed kinetic bounds. After setting the
new bounds, FBA and FVA are performed for each metabolic subsystem.

## Excel files

5. Mapping_Reactionsx.xlsx: This spreadsheet reports the results for the mapping of the
reactions between the two models. One or multiple reactions in the kinetic model correspond
with one reaction in the constraint-based model.

6. Flux_bounds_mapping.xlsx: Spreadsheet reporting the resulting maximum and minimum
bounds for each reaction after executing the differential evolution algorithm.
33

## Graphs

The graphs were designed in R. They can be found in the Grphs folder in the R script Graphs.R
