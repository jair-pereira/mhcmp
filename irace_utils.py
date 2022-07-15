# script to generate iRace files
# (1) scenario_<alg>.txt
# (2) parameter/parameters_<alg>.txt
# (3) Instances/<instances>.txt

# todos:
# read parameters from a file
# add irace paths to the parameter files

import itertools

def makefile_instance(filepath, func, dim, inst, nfe, restarts):
    output = f"\"--func {func} --dim {dim} --inst {inst} --nfe {nfe} --restarts {restarts}\"\n"

    with open(filepath, "w") as file:
        file.write(output)

def makefile_scenario(filepath, alg, tr_inst, maxexperiments, iterations, parallel, digits):
    output = [
        "parameterFile = \"./parameter/parameters_{alg}.txt\"",
        "execDir = \"./\"",
        "logFile = \"./result/irace_{alg}_{tr_inst}.Rdata\"",

        "trainInstancesDir = \"\"",
        "trainInstancesFile = \"./Instances/{tr_inst}.txt\"",

        "targetRunner = \"./target-runner_{alg}.sh\"",
        "maxExperiments = {maxexperiments}",
        "nbIterations = {iterations}",
        "parallel = {parallel}",
        "digits = {digits}",
        ""
    ]
    output = "\n".join(output)

    output = output.format(
        alg=alg, tr_inst=tr_inst,
        maxexperiments=maxexperiments,
        iterations=iterations,
        parallel=parallel,
        digits=digits
    )

    with open(filepath, "w") as file:
        file.write(output)

def makefile_parameters(filepath, param_list):
    output = "# name\tswitch\ttype\tvalues\n"

    for param in param_list:
        output += f"{param['name']}\t{param['switch']}\t{param['type']}\t{param['values']}\n"

    with open(filepath, "w") as file:
        file.write(output)

def main():
    # todo: parameter files
    algnames = ["pso", "ata", "gsa", "ffa", "rio", "de", "saa"]

    func = ["01", "06", "14", "16", "23"]
    dim  = [5]
    inst = [1]
    nfe  = [int(4e+5)]
    restarts = [4] #1e+5 per restart

    irace_maxexperiments = int(1e+4)
    irace_iterations     = 0
    irace_parallel       = 15
    irace_digits         = 2

    #todo: json file
    master_parameter_list = {
        "pso":[
            {"name":"n",  "switch":f"\" \"", "type":"c", "values":"(25, 50, 100, 200, 400, 800)"},
            {"name":"w",  "switch":f"\" \"", "type":"r", "values":"(0.00, 1.00)"},
            {"name":"c1", "switch":f"\" \"", "type":"r", "values":"(0.00, 2.00)"},
            {"name":"c2", "switch":f"\" \"", "type":"r", "values":"(0.00, 2.00)"}
        ],
        "ata":[
            {"name":"n",  "switch":f"\" \"", "type":"c", "values":"(25, 50, 100, 200, 400, 800)"},
            {"name":"tol","switch":f"\" \"", "type":"r", "values":"(0.00, 1.00)"},
            {"name":"w",  "switch":f"\" \"", "type":"r", "values":"(0.00, 2.00)"}
        ],
        "gsa":[
            {"name":"n",     "switch":f"\" \"", "type":"c", "values":"(25, 50, 100, 200)"},
            {"name":"g0",    "switch":f"\" \"", "type":"i", "values":"(0, 300)"},
            {"name":"alpha", "switch":f"\" \"", "type":"i", "values":"(0, 30)"}
        ],
        "ffa":[
            {"name":"n",     "switch":f"\" \"", "type":"c", "values":"(25, 50, 100, 200)"},
            {"name":"alpha", "switch":f"\" \"", "type":"r", "values":"(0.01, 1.00)"},
            {"name":"beta0", "switch":f"\" \"", "type":"r", "values":"(0.01, 1.00)"},
            {"name":"gamma", "switch":f"\" \"", "type":"r", "values":"(0.01, 10.00)"}
        ],
        "rio":[
            {"name":"n",  "switch":f"\" \"", "type":"c",  "values":"(25, 50, 100, 200)"},
            {"name":"th", "switch":f"\" \"", "type":"r",  "values":"(0.01, 1.00)"},
            {"name":"a1", "switch":f"\" \"", "type":"r",  "values":"(0.00, 1.00)"},
            {"name":"a2", "switch":f"\" \"", "type":"r",  "values":"(0.00, 1.00)"},
            {"name":"a3", "switch":f"\" \"", "type":"r",  "values":"(0.00, 1.00)"},
            {"name":"c0", "switch":f"\" \"", "type":"r",  "values":"(0.00, 1.00)"},
            {"name":"c1", "switch":f"\" \"", "type":"r",  "values":"(0.00, 2.00)"}
        ],
        "de":[
            {"name":"n",    "switch":f"\" \"", "type":"c", "values":"(25, 50, 100, 200, 400, 800)"},
            {"name":"cxpr", "switch":f"\" \"", "type":"r", "values":"(0.00, 1.00)"},
            {"name":"beta", "switch":f"\" \"", "type":"r", "values":"(-2.00, 2.00)"}
        ],
        "saa":[
            {"name":"n",     "switch":f"\" \"", "type":"c", "values":"(25, 50, 100, 200, 400, 800)"},
            {"name":"alpha", "switch":f"\" \"", "type":"r", "values":"(0.00, 1.00)"}
        ]
    }

    # make training instance files (combination of func, dim, inst, nfe, and restart)
    training_instances = [
        {"fname":f"{f}_{d}_{i}", "func":f, "dim":d, "inst":i, "nfe":nfe, "restarts":r}
            for f, d, i, nfe, r in itertools.product(func, dim, inst, nfe, restarts)
    ]

    for a in training_instances:
        makefile_instance(f"./irace/Instances/{a['fname']}.txt", a["func"], a["dim"], a["inst"], a["nfe"], a["restarts"])

    # make scenario files (one file for each algorithm x training instance)
    for alg, tr_inst in itertools.product(algnames, [a["fname"] for a in training_instances]):
        makefile_scenario(f"./irace/scenario_{alg}_{tr_inst}.txt",
                            alg, tr_inst,
                            irace_maxexperiments, irace_iterations, irace_parallel, irace_digits)

    # make parameter files (one file per algorithm specified in the json)
    for alg, param in master_parameter_list.items():
        makefile_parameters(f"./irace/parameter/parameters_{alg}.txt", param)


if __name__ == '__main__':
    main()
