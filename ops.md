- pattern matching
 
"IN/OUT neighbors via"

signature: `nbs(x: Node, l: EdgeLabel, direction: "in" | "out"): Set[Node]`

Can be used as a building block.\
Let's say we want to know `parent(X, Chris) and sex(male, X)`,
we can build this using `nbs(Chris, parent, "in") ∩ nbs(male, sex, "out")`.

Caveat: some representations allow for fast in-neighbors while others allow only for fast out-neighbors.
Which buildings blocks are fast should be listed and optimized for, possibly by having multiple (partially redundant) representations.

- node classification

Given labels


- link prediction
- distance estimation


Classification
Query
Pattern matching
Link prediction
Clustering
Path analysis (shortest path)
Network analysis
Graph decoding
