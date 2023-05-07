

| implementation                            | #hypervectors | directed | self loops | edge labels | node labels |
|-------------------------------------------|---------------|----------|------------|-------------|-------------|
| bind(src, tgt) bundle                     | 1             | x        | x          | x           | v           |
| bind(src, l, perm(tgt)) bundle            | 1             | v        | v          | v           | v           |
| setd(root, m-clique, m)                   | N             | x        | x          | x           | x           |
| setd(src, tgt, adj(src, tgt))             | N             | x        | x          | x           | x           |
| setdrel(src, tgt, adj(src, tgt), C)       | N             | v        | x          | x           | x           |
| setdrel(src, tgt, adj(src, tgt), maj(ls)) | N             | v        | x          | v           | x           |
 