| implementation                         | directed | self loops | edge labels | node labels |
|----------------------------------------|----------|------------|-------------|-------------|
| edge-bind graph-bundle                 | x        | x          | x           | v           |
| directed-edge-bind graph-bundle        | v        | v          | x           | x           |
| self mixed outgoing-majority           | v        | x          | x           | v           |
| setd(root, m-clique, m)                | x        | x          | x           | x           |
| iterative distance refinement          | x        | x          | x           | x           |
| iterative directed distance refinement | v        | x          | x           | x           |
| setdrel(src, tgt, C)                   | v        | x          | x           | x           |
| NTE                                    | v        | ?          | v           | v           |

## Implementations

### edge-bind graph-bundle

[file](edgebind_graphbundle.py)

handle: `bind(src, tgt) bundle`

### directed-edge-bind graph-bundle

[file](directededgebind_graphbundle.py)

handle: `bind(src, l, perm(tgt)) bundle`

### self mixed outgoing-bundle

[file](self_mixed_outgoingbundle.py)

handle: `randsel(src, bundle(tgts))`

### iterative distance refinement

[file](distance.py)

handle: `setd(src, tgt, adj(src, tgt))`

### iterative directed distance refinement

[file](directed_distance.py)

handle: `setdd(src, tgt, adj(src, tgt), D)`

### NTE

[file](nte.py)

handle: `setdrel(src, tgt, maj(ls))`
