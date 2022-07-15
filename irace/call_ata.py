import numpy as np
import cocoex
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metaheuristic.ata import ata

### interface between the target-runner and the solvers for irace ###

def main(args):
    ## arguments ##
    parser = argparse.ArgumentParser()
    parser.add_argument('--n'    , dest='n'    , type=int, help="Integer   : Population size")
    parser.add_argument('--tol'    , dest='tol'    , type=float, help="Real value:")
    parser.add_argument('--w'   , dest='w'   , type=float, help="Real value:")
    parser.add_argument('--seed' , dest='seed' , type=int,   help="Integer   : Exp Seed")
    parser.add_argument('--func' , dest='func' , type=int,   help="Int: BBOB function id")
    parser.add_argument('--dim'  , dest='dim'  , type=int,   help="Int: BBOB dimension value")
    parser.add_argument('--inst' , dest='inst' , type=int,   help="Int: BBOB instance indice")
    parser.add_argument('--nfe'  , dest='nfe'  , type=int,   help="Integer: Number of Function Evaluations")
    parser.add_argument('--restarts'  , dest='restart'  , type=int,   help="Integer: Number of restarts")
    args = parser.parse_args()

    ## bbob training suite ##
    suite = cocoex.Suite("bbob", "", f"function_indices:{args.func} dimensions:{args.dim} instance_indices:{args.inst}")

    ## nfe ##
    nfe = int(args.nfe)

    ## loop over problems ##
    problem = suite[0]

    # best fvalue
    best_f = np.inf
    for r in args.restarts: # breaks inside the solver if target hit
        result = ata(problem, maxnfe=nfe, n=int(args.n), tolerance=args.tol, w0=1, w=args.w, seed=int(args.seed))
        if best_f > result["f"]:
            best_f = result["f"]

    ## irace get information from standard output ##
    print(best_f)
    return

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])
