| implementation                            | directed | self loops | edge labels | node labels |
|-------------------------------------------|----------|------------|-------------|-------------|
| edge-bind graph-bundle                    | x        | x          | x           | v           |
| bind(src, l, perm(tgt)) bundle            | v        | v          | v           | v           |
| setd(root, m-clique, m)                   | x        | x          | x           | x           |
| iterative distance refinement             | x        | x          | x           | x           |
| setdrel(src, tgt, adj(src, tgt), C)       | v        | x          | x           | x           |
| setdrel(src, tgt, adj(src, tgt), maj(ls)) | v        | x          | v           | x           |

## Implementations

### edge-bind graph-bundle

[file](edgebind_graphbundle.py)

handle: `bind(src, tgt) bundle`

### iterative distance refinement

[file](distance.py)

handle: `setd(src, tgt, adj(src, tgt))`
