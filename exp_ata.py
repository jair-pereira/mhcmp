############ parameters ############
experiment_name = "ata"
#       n  tol    w
# f01 200 0.48 1.67
# f06 400 0.73 1.96
# f10 800 0.99 1.94
# f16 800 0.27 1.45
# f23 400 0.77 1.99
set_n   = [200,   400,    800,    800,    400]
set_tol = [0.48, 0.73,   0.99,   0.27,   0.77]
set_w   = [1.67, 1.96,   1.94,   1.45,   1.99]

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
from metaheuristic.ata import ata

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

tmp = ",".join(map(str, set_w))
file.write(f"w:{tmp}\n")

tmp = ",".join(map(str, set_tol))
file.write(f"tol:{tmp}\n")

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
            result = ata(problem=problem,

                         maxnfe=maxnfe,

                         n=set_n[i], tolerance=set_tol[i], w0=1, w=set_w[i],

                         seed=seeds[rep],
                         file=file)

            ## file close ##
            file.close()

            print(result["nfe"], result["f"], time.time()-start)

#cocopp.main(observer.result_folder)
