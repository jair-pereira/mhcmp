############ parameters ############
experiment_name = "gsa"
#       n g0 alpha
# f01 200  1    17
# f06 100  1    11
# f10 100  2     3
# f16 200  4     6
# f23 200  4     6
set_n      = [200, 100, 100, 200, 200]
set_g0     = [1,    1,   2,   4,   4]
set_alpha  = [17,  11,   3,   6,   6]

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
from metaheuristic.gsa import gsa

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

tmp = ",".join(map(str, set_g0))
file.write(f"g0:{tmp}\n")

tmp = ",".join(map(str, set_alpha))
file.write(f"alpha:{tmp}\n")

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
            result = gsa(problem=problem,

                         maxnfe=maxnfe,
                         n=set_n[i], g0=set_g0[i], alpha=set_alpha[i],

                         seed=seeds[rep],
                         file=file)

            ## file close ##
            file.close()

            print(result["nfe"], result["f"], time.time()-start)

#cocopp.main(observer.result_folder)
