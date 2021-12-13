import numpy as np
import cocoex
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metaheuristic.pso import pso

### interface between the target-runner and the solvers for irace ###

def main(args):
    ## arguments ##
    parser = argparse.ArgumentParser()
    #parser.add_argument('--nfe'  , dest='nfe'  , type=float, help="Integer   : Number of Function Evaluations")
    parser.add_argument('--n'    , dest='n'    , type=int, help="Integer   : Population size")
    parser.add_argument('--c1'   , dest='c1'   , type=float, help="Real value: pbest modifier")
    parser.add_argument('--c2'   , dest='c2'   , type=float, help="Real value: gbest modifier")
    parser.add_argument('--seed' , dest='seed' , type=int,   help="Integer   : Exp Seed")
    #parser.add_argument('--bbob', dest='bbob'  , type=str  , help="String    : BBOB suite e.g.:function_indices:1 dimensions:2 instance_indices:1")
    args = parser.parse_args()

    ## bbob training suite ##
    suite = cocoex.Suite("bbob", "", "function_indices:16 dimensions:5 instance_indices:1")

    ## nfe ##
    nfe = int(1e+5)

    ## loop over problems ##
    problem = suite[0]
    result = pso(problem, maxnfe=nfe, n=int(args.n), w=0, c1=args.c1, c2=args.c2, seed=int(args.seed))

    fitness = result["f"]
    ## irace get information from standard output ##
    print(fitness)
    return

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])
