import logging
import time

import matplotlib.pyplot as plt
import pandas as pd
from gboml import GbomlGraph

plt.rcParams["figure.figsize"] = 7, 5


def run_model(model_txt: str, timehorizon: int = 8760):
    gboml_model = GbomlGraph(timehorizon)
    nodes, edges, _ = gboml_model.import_all_nodes_and_edges(
        f"../models/scenarios/{model_txt}"
    )
    gboml_model.add_nodes_in_model(*nodes)
    gboml_model.add_hyperedges_in_model(*edges)
    gboml_model.build_model()
    solution = gboml_model.solve_gurobi(details=True)
    (solution_flat, objective, status, solver_info, constr_info, var_info) = solution
    solution_dict = gboml_model.turn_solution_to_dictionary(
        solution=solution_flat,
        solver_data=solver_info,
        status=status,
        objective=objective,
        constraint_info=constr_info,
        variables_info=var_info,
    )
    return solution, solution_dict


def show_results(solution_dict: dict, days: int = 7):
    """
    This function reads the solution that gboml creates as an
    output and prints the results in the stdout for better readability
    and faster interpretation of the results. For scalar results like
    investment costs, it just prints the result. For continuous variables
    it creates and prints a plot over the first seven days but the number
    of days for the visualization can be given as a parameter and thus a
    visualization for a longer period of time can be created.

    Parameters
    ----------
    solution_dict : dict
        The solution dictionary that gboml creates as an output.
    days : int
        The number of days the visualizations should be created for.
    """
    print(f"Objective result: {str(solution_dict['solution']['objective'])}")
    print(f"Objective status: {str(solution_dict['solution']['status'])}")
    elements = solution_dict["solution"]["elements"]
    for element in elements.keys():
        for variable in elements[element]["variables"].keys():
            var_values = elements[element]["variables"][variable]["values"]
            if len(var_values) == 1:
                result = f"Node {element}: {variable}: {var_values[0]}"
                print(result)
            else:
                print(f"Node {element}: {variable}: (first week)")
                plt.plot(var_values[: 24 * days])
                plt.show()


def get_results_new(scenarios: dict):
    """
    This function reads the solution that gboml creates as an
    output and prints the results in the stdout for better readability
    and faster interpretation of the results. For scalar results like
    investment costs, it just prints the result. For continuous variables
    it creates and prints a plot over the first seven days but the number
    of days for the visualization can be given as a parameter and thus a
    visualization for a longer period of time can be created.

    Parameters
    ----------
    model_txt : list
        A list containing the models you want to run, e.g. ['model.txt','benchmark.txt']
    """
    result = pd.DataFrame(
        columns=["execution_time", "num_households"], index=scenarios.keys()
    )
    objective_result = pd.DataFrame(
        columns=[
            "execution_time",
            "objective",
            "obj_per_houshold",
            "status",
            "num_households",
        ],
        index=scenarios.keys(),
    )
    for model in scenarios.keys():
        logging.info(f"Runnig {model}.")
        start_time = time.time()
        _, solution_dict = run_model(model)
        end_time = time.time() - start_time
        (
            objective_result.loc[model, "execution_time"],
            result.loc[model, "execution_time"],
        ) = (end_time, end_time)
        num_households = scenarios[model]
        objective_result.loc[model, "objective"] = solution_dict["solution"][
            "objective"
        ]
        objective_result.loc[model, "obj_per_houshold"] = (
            solution_dict["solution"]["objective"] / num_households
        )
        objective_result.loc[model, "status"] = solution_dict["solution"]["status"]
        result.loc[model, "num_households"] = num_households
        objective_result.loc[model, "num_households"] = num_households
        elements = solution_dict["solution"]["elements"]
        for element in elements.keys():
            if "objectives" in elements[element].keys():
                objective_result.loc[model, f"{element}: objective"] = elements[
                    element
                ]["objectives"]["unnamed"][0]
                objective_result.loc[model, f"{element}: obj_per_household"] = (
                    elements[element]["objectives"]["unnamed"][0] / num_households
                )
            for variable in elements[element]["variables"].keys():
                var_values = elements[element]["variables"][variable]["values"]
                if len(var_values) == 1:
                    column = f"{element}: {variable}"
                    result.loc[model, column] = var_values[0]
    return objective_result, result
