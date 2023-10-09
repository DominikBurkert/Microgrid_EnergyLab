# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:02:52 2023

@author: domin
"""

import os
from gboml import GbomlGraph


print("Der aktuelle Pfad ist:", os.getcwd())
os.chdir('C:/Users/domin/Desktop/Master/Praktikum_EI2/Microgrid_EnergyLab/Microgrid_EnergyLab/models/scenarios')
print("Der aktuelle Pfad ist:", os.getcwd())


model_txt = "benchmark.txt"
gboml_model = GbomlGraph(8760)
nodes, edges, _ = gboml_model.import_all_nodes_and_edges("model.txt")
gboml_model.add_nodes_in_model(*nodes)
gboml_model.add_hyperedges_in_model(*edges)
gboml_model.build_model()



solution, obj, status, solver_info, constr_info, _ = gboml_model.solve_gurobi()
print("Solved")
gathered_data = gboml_model.turn_solution_to_dictionary(solver_info, status, solution, obj, constr_info)
