| implementation                            | directed | self loops | edge labels | node labels |
|-------------------------------------------|----------|------------|-------------|-------------|
| edge-bind graph-bundle                    | x        | x          | x           | v           |
| directed-edge-bind graph-bundle           | v        | v          | x           | x           |
| self mixed outgoing-majority              | v        | x          | x           | v           |
| setd(root, m-clique, m)                   | x        | x          | x           | x           |
| iterative distance refinement             | x        | x          | x           | x           |
| iterative directed distance refinement    | v        | x          | x           | x           |
| setdrel(src, tgt, adj(src, tgt), C)       | v        | x          | x           | x           |
| setdrel(src, tgt, adj(src, tgt), maj(ls)) | v        | x          | v           | x           |

## Implementations

### edge-bind graph-bundle

[file](edgebind_graphbundle.py)

handle: `bind(src, tgt) bundle`

### directed-edge-bind graph-bundle

[file](directededgebind_graphbundle.py)

handle: `bind(src, l, perm(tgt)) bundle`

### self mixed outgoing-majority

[file](self_mixed_outgoingmajority.py)

handle: `randsel(src, majority(tgts))`

### iterative distance refinement

[file](distance.py)

handle: `setd(src, tgt, adj(src, tgt))`

### iterative directed distance refinement

[file](directed_distance.py)

handle: `setdd(src, tgt, adj(src, tgt), D)`
