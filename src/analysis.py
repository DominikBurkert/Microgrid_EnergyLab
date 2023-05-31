import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = 7, 5


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
