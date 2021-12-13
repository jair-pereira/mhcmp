import numpy as np
import cocoex
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metaheuristic.de import de

### interface between the target-runner and the solvers for irace ###

def main(args):
    ## arguments ##
    parser = argparse.ArgumentParser()
    #parser.add_argument('--nfe'  , dest='nfe'  , type=float, help="Integer   : Number of Function Evaluations")
    parser.add_argument('--n'    , dest='n'    , type=int, help="Integer   : Population size")
    parser.add_argument('--cxpr' , dest='cxpr'    , type=float, help="Real value:")
    parser.add_argument('--beta' , dest='beta'   , type=float, help="Real value:")
    parser.add_argument('--seed' , dest='seed' , type=int,   help="Integer   : Exp Seed")
    #parser.add_argument('--bbob', dest='bbob'  , type=str  , help="String    : BBOB suite e.g.:function_indices:1 dimensions:2 instance_indices:1")
    args = parser.parse_args()

    ## bbob training suite ##
    suite = cocoex.Suite("bbob", "", "function_indices:16 dimensions:5 instance_indices:1")

    ## nfe ##
    nfe = int(1e+5)

    ## loop over problems ##
    problem = suite[0]
    result = de(problem, maxnfe=nfe, n=int(args.n), cxpr=args.cxpr, beta=args.beta, seed=int(args.seed))

    fitness = result["f"]
    ## irace get information from standard output ##
    print(fitness)
    return

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])
