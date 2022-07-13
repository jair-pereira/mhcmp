import numpy as np

def ata(problem, maxnfe, n, tolerance, w0, w, seed, file=None):
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

    ## find pbest ##
    Pbest_x = np.array([x.copy() for x in Px])
    Pbest_f = Pf[:]
    
    ## history ##
    if file:
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")

    gbest_f_prev = gbest_f_cur = gbest_f
    while nfe <= maxnfe:
        if gbest_f_prev-gbest_f_cur < tolerance: #migration
            for i in range(n):
                r1 = myrng.uniform(0, 1, problem.dimension)
                r2 = myrng.uniform(0, 1, problem.dimension)
                Px[i] = Px[i] + w0*r1*(Pbest_x[i]-Px[i]) + w*r2*(gbest_x-Px[i])
        else: #propagation
            for i in range(n):
                r1 = myrng.uniform(0, 1, problem.dimension)
                Px[i] = r1*Px[i] + (1-r1)*Px[myrng.integers(0, n)]
        
        ## evaluate ##
        Pf = np.array([problem(x) for x in Px])
        nfe += len(Pf)

        ## find gbest ##
        current_best = np.argmin(Pf)
        if gbest_f >= Pf[current_best]:
            gbest_x = Px[current_best].copy()
            gbest_f = Pf[current_best]
        gbest_f_prev = gbest_f_cur
        gbest_f_cur  = gbest_f

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