import numpy as np


def node_probability(operator, probs):

    if operator == 'Or':
        return 1 - np.prod([1 - float(member) for member in probs])
    elif operator == 'And':
        return np.prod(np.array(probs).astype(float))
    else:
        print("Invalid Operator: ", operator)

