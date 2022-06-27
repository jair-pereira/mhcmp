############ parameters ############
experiment_name = "rio"
#     n   th   a1   a2   a3   c0   c1
# f01  25 0.84 0.10 0.88 0.48 1.46 1.38
# f06  50 0.79 0.65 0.82 0.32 0.85 0.58
# f10  25 0.90 0.43 0.84 0.04 0.77 0.45
# f16 100 0.36 0.04 0.79 0.59 1.25 0.41
# f23 200 0.67 0.74 0.86 0.24 1.22 1.10
set_n       = [25,     50,     25,    100,    200]
set_hunger  = [0.84, 0.79,   0.90,   0.36,   0.67]
set_c0      = [1.46, 0.85,   0.77,   1.25,   1.22]
set_c1      = [1.38, 0.58,   0.45,   0.41,   1.10]
set_a       = [ (0.10, 0.88, 0.48),
                (0.65, 0.82, 0.32),
                (0.43, 0.84, 0.04),
                (0.04, 0.79, 0.59),
                (0.74, 0.86, 0.24)]

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
from metaheuristic.rio import rio

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

file.write(f"seed:{seeds[rep]}\n")

tmp = ",".join(map(str, seeds))
file.write(f"seeds:{tmp}\n")

tmp = ",".join(map(str, set_n))
file.write(f"n:{tmp}\n")

tmp = ",".join(map(str, set_hunger))
file.write(f"thunger:{tmp}\n")

tmp = ",".join(map(str, set_a))
file.write(f"a:{tmp}\n")

tmp = ",".join(map(str, set_c0))
file.write(f"c0:{tmp}\n")

tmp = ",".join(map(str, set_c1))
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
            result = rio(problem=problem,

                         maxnfe=maxnfe,
                         n=set_n[i], t_hunger=set_hunger[i], a=np.sort(set_a[i]), c0=set_c0[i], c1=set_c1[i],

                         seed=seeds[rep],
                         file=file)

            ## file close ##
            file.close()

            print(result["nfe"], result["f"], time.time()-start)

#cocopp.main(observer.result_folder)
