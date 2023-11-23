- pattern matching
 
"IN/OUT neighbors via"

signature: `nbs(x: Node, l: EdgeLabel, direction: "in" | "out"): Set[Node]`

Can be used as a building block.\
Let's say we want to know `parent(X, Chris) and sex(male, X)`,
we can build this using `nbs(Chris, parent, "in") ∩ nbs(male, sex, "out")`.

Caveat: some representations allow for fast in-neighbors while others allow only for fast out-neighbors.
Which buildings blocks are fast should be listed and optimized for, possibly by having multiple (partially redundant) representations.

- graph completion

(resting box)
(resting vase)
(adjacent box vase)

introduce surface-1290
(on box surface-1290)
(on vase surface-1290)

- node classification

Given labels on part of the nodes, classify the rest based on their connections.

- link prediction

Given a part of the edges, predict which edges would be likely to be part of the full graph.

- distance estimation

Given two nodes, estimate the length of the shortest path between them.


---
Original tasks:
Classification
Query
Pattern matching
Link prediction
Clustering
Path analysis (shortest path)
Network analysis
Graph decoding
