from petsc4py import PETSc as petsc
import GPUArray

v = petsc.Vec()
v.create()
v.setSizes(4)
v.setType('cusp')
v.set(2.0)

print v.array
G = GPUArray.getGPUArray(v)
print G.get()
v.destroy()
