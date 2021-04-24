import numpy as np
from lib.plot_tools import to_precision


def node_probability(operator, probs):

    if operator == 'Or':
        return to_precision(1 - np.prod([1 - float(member) for member in probs]), 3)
    elif operator == 'And':
        return to_precision(np.prod(np.array(probs).astype(float)), 3)
    else:
        print("Invalid Operator: ", operator)

