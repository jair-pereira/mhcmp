import numpy as np

def ffa(problem, maxnfe, n, alpha, gamma, seed, file=None):
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
    
    ## history ##
    if file:
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
    
    while nfe <= maxnfe:# and not problem.final_target_hit:
        i_sorted = np.argsort(-Pf) #best at the end
        for k, i in enumerate(i_sorted):
            for j in i_sorted[k+1:]:
                rnd = myrng.uniform(-0.5, +0.5, problem.dimension)
                if Pf[i] > Pf[j]:
                    dist = np.sqrt((Px[j]-Px[i])**2)
                    beta = 0.2 + (1-0.2)*np.exp(-gamma*dist*dist)
                    # attraction + random walk
                    Px[i] = Px[i] + beta*(Px[j]-Px[i]) + (alpha/100)*rnd
                else:
                    # random walk
                    Px[i] = Px[i] + alpha*rnd
        
        ## best particle random walk ##
        Px[current_best] += (alpha/1000)*myrng.uniform(-0.01, +0.01, problem.dimension)
        
        ## repair ##
        Px = [np.clip(x, problem.lower_bounds, problem.upper_bounds) for x in Px]
        
        ## evalute ##
        Pf = np.array([problem(x) for x in Px])
        nfe += len(Pf)

        ## update gbest ##
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