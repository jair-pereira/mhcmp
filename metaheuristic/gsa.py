import numpy as np

def gsa(problem, maxnfe, n, g0, alpha, seed, file):
    myrng = np.random.RandomState(seed)

    ## initialization ##
    Px = np.array([myrng.uniform(problem.lower_bounds, problem.upper_bounds, problem.dimension) for _ in range(n)])

    ## other attributes ##
    Pv = np.zeros((n, problem.dimension)) # velocity
    Pmass  = np.zeros(n) # mass (Mi=Ma=Mp)
    Pmi    = np.zeros(n) # aux for mass
    Pforce = np.zeros((n, problem.dimension))
    Pacceleration = np.zeros(n) 

    ## evalute ##
    Pf = np.array([problem(x) for x in Px])
    nfe = len(Pf)

    ## find gbest and gworst ##
    current_best = np.argmin(Pf)
    gbest_x = Px[current_best].copy()
    gbest_f = Pf[current_best]
    gbest_fi = gbest_f #at iteration i
    
    current_worst = np.argmax(Pf)
    gworst_fi = Pf[current_worst]
    
    ## history ##
    str_gbestx = ";".join(map(str, gbest_x))
    file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
    
    max_iteration = np.ceil(maxnfe/n)
    kbest = list(map(int, np.linspace(n, 1, int(max_iteration))))
    
    iteration=0
    while nfe <= maxnfe:
        # compute g
        g = g0*np.e**(-alpha*iteration/max_iteration)
        
        # compute mass
        Pmi = (Pf-gworst_fi)/(np.finfo('float').eps+gbest_fi-gworst_fi)
        Pmass = Pmi/sum(Pmi)
        Pmass.resize(n,1)
        
        #choose k
        #K = np.arange(0, n)
        nk = int(np.ceil(n*np.e**(-alpha*iteration/max_iteration)))
        K = np.argpartition(Pf, -nk)[:nk]
        
        # compute force
        for i in range(n):
            Pforce[i] = 0
            for k in K:
                a = g*(Pmass[i] * Pmass[k])
                b = np.abs(Px[i]-Px[k]) + np.finfo('float').eps
                c = (Px[k]-Px[i])

                Pforce[i] += c*(a/b) * myrng.uniform(0,1,problem.dimension)
        
        # update acceleration, velocity, and position
        Pacceleration = Pforce/(Pmass+np.finfo('float').eps)
        Pv = [Pacceleration[i] + Pv[i]*myrng.uniform(0,1,problem.dimension) for i in range(n)]
        Px = np.array([np.clip(Px[i]+Pv[i], problem.lower_bounds, problem.upper_bounds) for i in range(n)])

        ## evaluate ##
        Pf = np.array([problem(x) for x in Px])
        nfe += len(Pf)
        
        ## update gbest and gworst ##
        current_best = np.argmin(Pf)
        if gbest_f >= Pf[current_best]:
            gbest_x = Px[current_best].copy()
            gbest_f = Pf[current_best]
        gbest_fi = Pf[current_best]
            
        current_worst = np.argmax(Pf)
        gworst_fi = Pf[current_worst]
        
        ## history ##
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
        
        iteration+=1
    
    result = {"x"  :gbest_x,
              "f"  :gbest_f,
              "nfe":nfe}
    
    return result