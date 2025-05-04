# Chilly's Monte Carlo Adventure 🐧🗺️

## About

This is a collection of algorithm to solve the 'Easter Puzzle 2025: Send the penguin Chilly on an egg hunt' in [c't 9/2025 page 150](https://www.heise.de/select/ct/2025/9/2507710375395222187). An implementation of the puzzle can be found [here](https://626d7a7179207166206f75646f717a657165.github.io/easter-chilly/) with the source code available [here](https://github.com/626d7a7179207166206f75646f717a657165/easter-chilly).  

The task of the puzzle is to find the **longest possible path** from the starting position to the exit under the additional condition to collect all eggs on the traversed route. Also, there is either one condition to fulfill to solve the puzzle: 1. Only visit any *edge* **ONCE** or 2. Only visit any *node* **ONCE**.  

As already noted in the article, the playfield can be considered as **directed cyclic graph** with *node* and *edges*. Additionally the playfield uses periodic boundary condition: if Chilly slides of the boundary it will be enter on the other side. Chilly's movement will only stop if it hits an obstacle (flower, tree, or rock), but not if an egg crosses its path (, which will be collected). At the end of the route Chilly needs to find the exit node, but it can also reach it without collecting all eggs. The start node isn't special at all... Also, there are lot of nodes that can actually never be reached as Chilly will not stop on them, but they are needed as the eggs are placed on them. In sum, Chilly's challenge is related to the [longest path problem in graph theory](https://en.wikipedia.org/wiki/Longest_path_problem). 

### Condition 1 - Only visit any EDGE once

- Rephrased: "Do NOT allow any multiple moves on edges, that have been already used."
- Strategy: keep track of all visited edges and strictly forbid to reuse them
- This can lead to very long paths

### Condition 2 - Only visit any NODE once

- Rephrased: "Do NOT allow any multiple stopping on a node, that have been already used."
- Important: the starting node does **not count** as visited in the beginning!
- Strategy: keep track of all visited nodes and strictly forbid to stop on them
- This can lead to long paths but presumably less than Condition 1

### Assumptions

- the nodes there the eggs are placed will not be considered explicitly as it will be assumed that the longest path on the graph will traverse these nodes
- the algorithm will immediately end if all eggs are collected and the exit has be hit 

## Brute Force Monte Carlo

- The [Swiss jackknife](https://en.wikipedia.org/wiki/Pocketknife#Multi-tool_knives) algorithm to find **one particular** (, but maybe not the best) solution
- The [Monte Carlo algorithm](https://en.wikipedia.org/wiki/Monte_Carlo_method) is purely based on randomness: there is a solution inherently by chance if any solution exist, but the convergence to the solution can be problematic
- The Monte Carlo algorithm basically performs random motion on the directed cyclic graph: it traverse by chance the edges (under condition 1 or 2), but needs to allow backtracking to avoid 'get stuck' on a path
- The backtracking is used as often as needed, also resulting on the start node again
- Brute Force Monte Carlo is maybe useful here, for small graphs and no inherent strong barriers (low number of accessible longest paths)

### Brute Force Monte Carlo - Condition 1: Every EDGE Once

- See the file 'Chilly_BruteForceMonteCarlo_Puzzle1.py'
- Example solutions: (on Puzzle1 seem 32 the maximum steps)
- Puzzle1: 32 steps: LULRDRLDRLRDUDLUDLURDULLRURDLRUL
- Puzzle1: 32 steps: LLRRDLURLDRLRDUDLUDULULRDURDLRUL
- Puzzle1: 32 steps: LLURUDLRRLDRLRDUDLDULULRDURDLRUL
- Puzzle1: 32 steps: LLURDLRUDDRLRDUDLDRRUDULULUDLRUL

### Brute Force Monte Carlo - Condition 2: Every Node Once

- For Puzzle1 there seems no solution, therefore have a look in 'Chilly_BruteForceMonteCarlo_Puzzle2_OnlyNodesOnce.py'
- Example solutions: (on Puzzle2 seems 40 the maximum steps)
- Puzzle2: 33 steps: DDULURLDULULRDULRULUDRDULRULRDLDL


## Monte Carlo Umbrella Sampling

- For huge graphs the convergence of Brute Force Monte Carlo can be limited as it needs to explore also very rare events, e.g. longest paths, which are very seldom or unique
- To guide the traversal to overcome the barrier or explore seldom regions, an additional potational is used to 'push' the walker in that region: known as [Umbrella Sampling](https://en.wikipedia.org/wiki/Umbrella_sampling)
- Puzzle2 is solved that way in file 'Chilly_UmbrellaSampling_Puzzle2_OnlyNodesOnce.py'
- Puzzle2: 33 steps: DDULDRLDRULRURLDLRDURULRDURUDLRDL
- Puzzle2: 37 steps: UDDULDURLDULDULRDULRULDLRDULRULRDLDRL
- Puzzle2: 40 steps: UDUDLDURLDULDULRDULRURLUDLRDULRULRDRLDRL

## Monte Carlo Iterative Boltzmann Inversion

- To overcome even more high barriers on an unknown landscape, a [flat histogram method](https://en.wikipedia.org/wiki/Multicanonical_ensemble) known as 'Iterative Boltzmann Inversion' is used
- It samples the 'energy landscape' by random walk and reproduces the inverse 'potential of mean force' balancing the penalty of movements in high energy regions with rare events.
- Puzzle3 is solved that way in file 'Chilly_IBI_Puzzle3_OnlyEgdesOnce.py'
- Puzzle3: 73 steps: LRDDUUDURLDLUDURDULULDURUDLULDURDULRULRLDLRURLDRDRLULRURLRDURLDRURDRDUDRL
- Puzzle3: 75 steps: LDRURDRDURUDURLDLURDLDULUDULDULDURDLURURLRURLDRLRURLDRUDRLULRULRDURLDRDDURU
- Puzzle3: 77 steps: UDUDDUDULURLRDLDULUDULULDURDLDURUDURLRURLDUDRLRDRLULDRURLRURLRDURLDRLDRURDRDL 
- Puzzle3: 77 steps: LDRDDULDURDLULRLUDULDURLDURUDURLRULDUDRLRULDRUDRLURLRULRDURLDLRURDRLULDURLDRU 

## Can we do better?

- Yes, all implementation are not optimized regarding memory efficiency and runtime.
- Yes, the convergence of the Umbrella and Iterative Boltzmann algorithm can be tuned by adjusting the parameters.
- Yes, all algorithm consider a random walk on the graph without explicitly finding the end node. A lot of time, the longest path will not even reach the exit. Therefore, the Monte Carlo move should be adjusted in the way, that the already explored path should be combined with the shortest path of the current position to the exit node. This guarantees only paths from the start to end node in contrast to the proposed calculations.
- Yes, the mandatory win condition to collect all eggs is only implicitly fulfilled and not considered straight away in the Monte Carlo move. 

## References, License, Credit, Acknowledgment

* It's just for fun and educational purpose. Feel free to modify, improve, and use it :)
* The codes are released under [The Unlicense](https://unlicense.org/) into public domain for free usage.


