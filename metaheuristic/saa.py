import numpy as np

def saa(problem, maxnfe, n, alpha, seed, file=None):
    myrng = np.random.default_rng(seed)

    ## initialization ##
    Px = np.array([myrng.uniform(problem.lower_bounds, problem.upper_bounds, problem.dimension) for _ in range(n)])
    
    ## evalute ##
    Pf = np.array([problem(x) for x in Px])
    nfe = len(Pf)
    
    ## find gbest ##
    current_best = np.argmin(Pf)
    gbest_x = Px[current_best].copy()
    gbest_f = Pf[current_best]
    
    ## temperature step ##
    k  = int(maxnfe/n)
    ki = 1
    
    ## neighborhood step size
    steps = np.linspace(1, 1e-9, num=int(maxnfe/n))
    
    ## history ##
    if file:
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")

    while nfe+n <= maxnfe and not problem.final_target_hit:
       ## temperature ##
        temperature = 1- ki/k
        ki+=1
        
        ## neighbor ##
        Pmut = alpha*np.array([myrng.uniform(steps[ki-2], steps[ki-2], problem.dimension) for _ in range(n)])
        Pu = Px + Pmut
        
        ## evaluate Pu ##
        Pfu = np.array([problem(u) for u in Pu])
        nfe += len(Pfu)
        
        ## replacement ##
        mask = [True if Pf[i]>=Pfu[i] or temperature>=myrng.uniform() else False for i in range(n)]
        Px[mask] = Pu[mask]
        Pf[mask] = Pfu[mask]

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