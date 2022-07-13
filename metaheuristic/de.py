import numpy as np

def crossover_exponential(x1, x2, pr, dim, rng):
    #pr_list = [pr**i for i in range(dim)] and roll only one
    
    pr_list = [pr]*dim + [-1]
    pr_rolls = rng.uniform(0,1, dim+1)
    
    start_i = rng.choice(range(dim))
    stop_i  = np.argmin((pr_rolls <= pr_list))
    mask = [start_i]+[(start_i+j)%dim for j in range(stop_i)]
    
    u = x1.copy()
    u[mask] = x2[mask]
    
#     v = x2.copy()
#     v[mask] = x1[mask]
    
    return u#, v

def de(problem, maxnfe, n, cxpr, beta, seed, file=None):
    myrng = np.random.default_rng(seed)
    crossover = lambda x,u: crossover_exponential(x,u, pr=cxpr, dim=problem.dimension, rng=myrng)

    ## initialization ##
    Px = np.array([myrng.uniform(problem.lower_bounds, problem.upper_bounds, problem.dimension) for _ in range(n)])

    ## evalute ##
    Pf = np.array([problem(x) for x in Px])
    nfe = len(Pf)

    ## find gbest ##
    current_best = np.argmin(Pf)
    gbest_x = Px[current_best].copy()
    gbest_f = Pf[current_best]
    
    ## history ##
    if file:
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
        
    while nfe+n <= maxnfe and not problem.final_target_hit:
        ## de-mutation ##
        Ps = np.array([np.random.choice(range(0,n), 3, replace=False) for _ in range(n)])
        Pu = np.array([Px[a] + beta*(Px[b]-Px[c]) for a,b,c in Ps])
        
        ## crossover exponential ##
        Pv = np.array([crossover(Px[i], Pu[i]) for i in range(n)])
        
        ## evaluate ##
        Pfv = np.array([problem(x) for x in Pv])
        nfe += len(Pfv)
        
        ## replacement ##
        mask = [f2 <= f1 for f1, f2 in zip(Pf, Pfv)]
        Px[mask] = Pv[mask]
        Pf[mask] = Pfv[mask]

        ## find gbest ##
        current_best = np.argmin(Pf)
        if gbest_f >= Pf[current_best]:
            gbest_x = Px[current_best].copy()
            gbest_f = Pf[current_best]
            
        ## history ##
        if file:
            str_gbestx = ";".join(map(str, gbest_x))
            file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
    
    result = {"x"  :gbest_x,
              "f"  :gbest_f,
              "nfe":nfe}
    
    return result