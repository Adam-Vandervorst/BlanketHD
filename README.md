| implementation                         | directed | self loops | edge labels | node labels |
|----------------------------------------|----------|------------|-------------|-------------|
| edge-bind graph-bundle                 | x        | x          | x           | v           |
| edge-bind blanket-bundle               | x        | x          | x           | v           |
| directed-edge-bind graph-bundle        | v        | v          | x           | x           |
| self mixed outgoing-majority           | v        | x          | x           | v           |
| setd(root, m-clique, m)                | x        | x          | x           | x           |
| iterative distance refinement          | x        | x          | x           | x           |
| iterative directed distance refinement | v        | x          | x           | x           |
| setdrel(src, tgt, C)                   | v        | x          | x           | x           |
| NTE                                    | v        | ?          | v           | v           |
| hyperedge multibind bundle             | v        | ?          | x           | v           |
| hyperedge bundle bundle                | v        | ?          | x           | v           |
| hyperedge permute bind                 | v        | ?          | x           | v           |

## Implementations

### edge-bind graph-bundle

[file](edgebind_graphbundle.py)

handle: `bind(src, tgt) bundle`

### edge-bind blanket-bundle

[file](benchmarks/edgebind_blanketbundle.py)

handle: `bind(src in blanket, tgt in blanket) bundle`

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

[file](bias_ps_nte.py)

handle: `setdrel(src, tgt, maj(ls))`

[file](self_mixed_propertybundle.py)

handle: `randsel(s, bundle(bind(p, o)))`

[file](triplebind_propertybundle.py)

handle: `p, bundle(bind(Ps, Qo))`

### Directed Hypergraphs

[file](hyperedge_multibind_bundle.py)

handle: `bind(multibind(srcs), bundle(dsts))`

[file](hyperedge_bundle_bundle.py)

handle: `bind(bundle(srcs), bundle(dsts))`


### Ordered Hypergraphs

[file](hyperedge_permute_bind.py)

handle: `bind(src_i.permute(i))`
