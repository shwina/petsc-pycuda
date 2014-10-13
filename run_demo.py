from petsc4py import PETSc as petsc
import GPUArray

v = petsc.Vec()
v.create()
v.setSizes(4)
v.setType('cusp')


