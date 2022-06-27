############ parameters ############
experiment_name = "de"
#     n cxpr  beta
# f01   200 0.89 -0.11
# f06   25 0.74 -0.63
# f10   25 0.83 -0.66
# f16   25 0.82 -0.99
# f23  100 0.94  0.25
set_n    = [200,      25,     25,     25,    100]
set_cxpr = [0.89,   0.74,   0.83,   0.82,   0.94]
set_beta = [-0.11, -0.63,  -0.66,  -0.99,   0.25]

## bbob ##
functions  = "2,3,4,5,7,8,9,11,12,13,14,15,17,18,19,20,21,22,24"
dimensions = "5"
indices    = "1"

## budget ##
maxnfe  = int(1e+6)
restart = len(set_n)
seeds   = [2637, 9609, 1192, 3459, 3487] #seed used on each repetition
max_rep = 5

############ main ############
## imports ##
import os
import time
import numpy as np
import cocoex#, cocopp
from metaheuristic.de import de

## bbob setup ##
suite_string  = f"function_indices:{functions} dimensions:{dimensions} instance_indices:{indices}"
suite       = cocoex.Suite("bbob", "", suite_string)
#observer = cocoex.Observer("bbob", "result_folder: " + f"{experiment_name}")

## create folders ##
if not os.path.exists("results"):
    os.mkdir("results")


i=0
while os.path.exists(f"results/{experiment_name}_{i:03d}"):
    i+=1

folder_results = f"results/{experiment_name}_{i:03d}"
os.mkdir(folder_results)

## write parameters into a file ##
file = open(f"{folder_results}/parameters.csv", "a")

file.write(f"experiment_name:{experiment_name}\n")
file.write(f"suite:{suite_string}\n")
file.write(f"maxnfe:{maxnfe}\n")

tmp = ",".join(map(str, seeds))
file.write(f"seeds:{tmp}\n")

tmp = ",".join(map(str, set_n))
file.write(f"n:{tmp}\n")

tmp = ",".join(map(str, set_cxpr))
file.write(f"w:{tmp}\n")

tmp = ",".join(map(str, set_beta))
file.write(f"c1:{tmp}\n")

file.close()

## main loop ##
for problem in suite:
    print(problem.id)
    #problem.observe_with(observer)

    for rep in range(max_rep):
        for i in range(restart):
            ## timing ##
            start = time.time()

            ## file open ##
            file = open(f"{folder_results}/{problem.id}_res{i}_rep{rep}.csv", "a")

            ## run method ##
            result = de(problem=problem,

                         maxnfe=maxnfe,
                         n=set_n[i], cxpr=set_cxpr[i], beta=set_beta[i],

                         seed=seeds[rep],
                         file=file)

            ## file close ##
            file.close()

            print(result["nfe"], result["f"], time.time()-start)

#cocopp.main(observer.result_folder)
