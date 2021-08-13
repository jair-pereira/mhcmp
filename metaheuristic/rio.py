import numpy as np
from scipy.spatial.distance import pdist, squareform

def calc_dist_matrix(Px, n, metric="euclidean"):
    # compute distance
    dist = pdist(Px, metric)
    
    # matrix form
    dist_matrix = squareform(dist)
    
    # compute median
    dist_median  = np.median(dist)

    return dist_median, dist_matrix

def get_neighborhood(i, dist_median, dist_matrix):
    # neighbors: distance < median
    mask_neighbors = (dist_matrix[i] < dist_median)
    
    # dont include itself as neighbor
    mask_neighbors[i] = False 
    
    return mask_neighbors

def rio(problem, maxnfe, n, t_hunger, a, c0, c1, seed, file):
    myrng = np.random.RandomState(seed)

    ## initialization ##
    Px = np.array([myrng.uniform(problem.lower_bounds, problem.upper_bounds, problem.dimension) for _ in range(n)])
    
    ## other attributes ##
    # velocity
    Pv = np.zeros((n, problem.dimension))
    # hunger
    Phunger = myrng.randint(0, t_hunger, n)

    ## evalute ##
    Pf = np.array([problem(x) for x in Px])
    nfe = len(Pf)

    ## find gbest ##
    current_best = np.argmin(Pf)
    gbest_x = Px[current_best].copy()
    gbest_f = Pf[current_best]

    ## find pbest ##
    Ppbest_x = np.array([x.copy() for x in Px])
    Ppbest_f = Pf[:]
    
    ## find lbest ##
    Plbest_x = np.array([x.copy() for x in Px])
    Plbest_f = Pf[:]
    
    ## history ##
    str_gbestx = ";".join(map(str, gbest_x))
    file.write(f"{nfe},{gbest_f},{str_gbestx}\n")

    while nfe <= maxnfe:
        # compute distances between c.solutions and the median
        dist_median, dist_matrix = calc_dist_matrix(Px, n)
        
        # for each c.solution
        for i in range(n):
            # get neighbors
            neighborhood = get_neighborhood(i, dist_median, dist_matrix)
        
            # chance of exchanging information with neighbors
            n_neighbors = sum(neighborhood)
            mask = (np.random.uniform(0, 1, n_neighbors) < a[min(n_neighbors-1, 2)])
            
            # exchange lbest info
            indices = np.arange(0, n)
            for neighbor in indices[neighborhood][mask]:
                if Pf[i] > Pf[neighbor]: #if i.fitness worse than neighbor, get neighbor.fitness
                    Plbest_f[i] = Pf[neighbor]
                    Plbest_x[i] = Px[neighbor]
                else: # give i.fitness to neighbor
                    Plbest_f[neighbor] = Pf[i]
                    Plbest_x[neighbor] = Px[i]
            
            # update position or re-initialize depending on hunger
            if Phunger[i] < t_hunger: #update
                r1 = myrng.random(problem.dimension)
                r2 = myrng.random(problem.dimension)
                #velocity update
                Pv[i] = c0*Pv[i] + c1*r1*(Ppbest_x[i] - Px[i]) + c1*r2*(Plbest_x[i] - Px[i])
                #position update
                Px[i] = np.clip(Px[i]+Pv[i], problem.lower_bounds, problem.upper_bounds)
                #hunger update
                Phunger[i]+=1                
            else: #re-initialize
                Px[i] = myrng.uniform(problem.lower_bounds, problem.upper_bounds, problem.dimension)
                Phunger[i]=0
                
            #evalute
            Pf[i] = problem(Px[i])
            nfe+=1 
            #update pbest
            if Ppbest_f[i] >= Pf[i]:
                Ppbest_x[i] = Px[i].copy()
                Ppbest_f[i] = Pf[i]
                
        ## find gbest ##
        current_best = np.argmin(Pf)
        if gbest_f >= Pf[current_best]:
            gbest_x = Px[current_best].copy()
            gbest_f = Pf[current_best]
            
        ## history ##
        str_gbestx = ";".join(map(str, gbest_x))
        file.write(f"{nfe},{gbest_f},{str_gbestx}\n")
    
    result = {"x"  :gbest_x,
              "f"  :gbest_f,
              "nfe":nfe}
    
    return result