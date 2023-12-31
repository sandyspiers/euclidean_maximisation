# The Euclidean Max-Sum Cutting Plane Algorithm (EMSCA)

Here, we provide a brief summary of 4 exact algorithms implemented in `EmsModel`.
For detail descriptions and proof of convergence, see [1].

## 1. Repeated Outer-Approximation (`repoa`)

 1. Begin with the tangent plane of the a maximum cardinality solution.
 2. Use Theorem 1.b from [1] to assure each tangent plane generated by the **optimal solution** of the outer approximation subproblem always creates a valid cut.
 3. Repeat until `LB=UB`

## 2. Forced Cardinality (`fcard`)

1. Begin with the tangent plane of the a maximum cardinality solution.
2. Fix cardinality to max, and solve subproblem using branch and cut.
3. Calculate upper bound of future iterations.
4. Decrease cardinality by 1, but preserve all tangent planes.
5. Repeat until `LB=UB`.

## 3. Glover Linearisation (`glover`)

Uses a Glover linearisation of the objective function, and solve using `CPLEX`.

## 4. Quadratic CPLEX (`quad`)

Uses a the quadratic mixed-integer solver available within `CPLEX`.

## LP-tangents

LP-tangents can be used to speed up cut generation.
This is done using 3 options:

 1. `True` : Add LP-tangents at the start of every iteration.
 2. `rootonly` : Add LP-tangents only at the first iteration
 3. `False` : Never add LP-tangents.

## References

[1] Hoa T. Bui, Sandy Spiers, Ryan Loxton, *Cutting Plane Algorithms on Euclidean Distance Maximisation are Exact*, Manuscript under review.
