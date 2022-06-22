# Empirical Similarity Measure for Metaheuristics
This repository contains the code, data, and additional figures for the BIOMA 2022 submission.

In our paper, we propose a method to compare metaheuristics algorithms empirically based on their performance profile on many benchmark functions with multiple landscape characteristics.

The method has three steps:
1. generating algorithm instances through parameter tuning
2. performance profiling of all generated instances on benchmark problems with different landscape characteristics, and 
3. comparing the algorithm's instances using silhouette score and performance similarity.

## Additional figures
todo

## Running the experiment
### Docker
Scripts are in a Docker environment. To initialize the docker:
```
docker build -t mhcmp .
docker run -dt --cpus="X" --name mhcmp_c1 mhcmp
```
where X is the number of desired cpus

### Step 1: Algorithm instance generation (parameter tuning)
]To run step 1, initialize the docker, then 
```
docker exec -t -i mhcmp_c1 /bin/bash
nohup sh ./irace/exp.sh &
 ```

Then results of the parameter tuning will be in the folder "./irace/results".

### Step 2: Performance profiling all algorithms' instances
todo
### Step 3: Performance similarity
todo
