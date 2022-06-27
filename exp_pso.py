############ parameters ############
experiment_name = "pso"
# f01   50 0.88 0.54 0.83
# f06  800 0.57 0.64 1.54
# f10   25 0.81 1.28 0.57
# f16  800 0.79 1.27 0.63
# f23  800 0.63 0.15 0.95
set_n  = [50,    800,   25,   800,   800]
set_w  = [0.88, 0.57, 0.81,  0.79,  0.63]
set_c1 = [0.54, 0.64, 1.28,  1.27,  0.15]
set_c2 = [0.83, 1.54, 0.57,  0.63,  0.95]

## bbob ##
#all    : "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24"
#special: "21,22, 17,18, 8,9, 3,15"
#testing: "2,3,4,5,7,8,9,11,12,13,14,15,17,18,19,20,21,22,24"
#trainng: "1,6,10,16,23"
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
from metaheuristic.pso import pso

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

tmp = ",".join(map(str, set_c1))
file.write(f"c1:{tmp}\n")

tmp = ",".join(map(str, set_c2))
file.write(f"c2:{tmp}\n")

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
            result = pso(problem=problem,

                         maxnfe=maxnfe,
                         n=set_n[i], w=set_w[i], c1=set_c1[i], c2=set_c2[i],

                         seed=seeds[rep],
                         file=file)

            ## file close ##
            file.close()

            print(result["nfe"], result["f"], time.time()-start)

#cocopp.main(observer.result_folder)
