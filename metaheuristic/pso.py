import numpy as np

def pso(problem, maxnfe, n, w, c1, c2, seed, file=None):
    myrng = np.random.default_rng(seed)

    ## initialization ##
    Px = np.array([myrng.uniform(problem.lower_bounds, problem.upper_bounds, problem.dimension) for _ in range(n)])

    ## velocity ##
    Pv = np.zeros((n, problem.dimension))

    ## evalute ##
    Pf = np.array([problem(x) for x in Px])
    nfe = len(Pf)

    ## find gbest ##
    current_best = np.argmin(Pf)
    gbest_x = Px[current_best].copy()
    gbest_f = Pf[current_best]

    ## find pbest ##
    Pbest_x = np.array([x.copy() for x in Px])
    Pbest_f = Pf[:]
    
    ## history ##
    if file:
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")

    while nfe <= maxnfe:
        ## compute new velocity ##
        R1 = myrng.random((n, problem.dimension))
        R2 = myrng.random((n, problem.dimension))
        Pv = np.array([w*Pv[i] + c1*R1[i]*(Pbest_x[i] - Px[i]) + c2*R2[i]*(gbest_x - Px[i]) for i in range(n)])

        ## compute new position ##
        Px = np.array([np.clip(Px[i]+Pv[i], problem.lower_bounds, problem.upper_bounds) for i in range(n)])

        ## evaluate ##
        Pf = np.array([problem(x) for x in Px])
        nfe += len(Pf)

        ## find gbest ##
        current_best = np.argmin(Pf)
        if gbest_f >= Pf[current_best]:
            gbest_x = Px[current_best].copy()
            gbest_f = Pf[current_best]

        ## find pbest ##
        for i in range(n):
            if Pbest_f[i] >= Pf[i]:
                Pbest_x[i] = Px[i].copy()
                Pbest_f[i] = Pf[i]
                
        ## history ##
        if file:
            str_gbestx = ";".join(map(str, gbest_x))
            file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
    
    result = {"x"  :gbest_x,
              "f"  :gbest_f,
              "nfe":nfe}
    
    return result