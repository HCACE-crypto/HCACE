from .NMAP2MAP import policy2booean_expr
from .boolean2lsss import boolean2lsss
from .AKPABE import Policy
import numpy as np

def transform_policy(policy, max_legth):
    expr= policy2booean_expr(policy, max_legth)
    # print(expr)
    lsss, map = boolean2lsss(expr)
    # print(lsss)
    # print(len(lsss))
    lsss.reverse()
    lsss = np.array(lsss)
    
    name_map = []
    value_map = map
    value_map.reverse()
    for i in range(len(map)):
        name_map.append(str(max_legth -1 - i%max_legth))

    pai_map = []
    for name, value in zip(name_map, value_map):
        pai_map.append([name, value]) 

    return Policy(lsss, pai_map, [name_map, value_map])

def print_list(l):
    for e in l:
        print(e)

if __name__ == "__main__":
    policy = [7, 12, 3]
    print(transform_policy(policy, 4))
