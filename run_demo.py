from petsc4py import PETSc as petsc
import GPUArray

v = petsc.Vec()
v.create()
v.setSizes(4)
v.setType('cusp')
v.set(2.0)

print 'Original PETSc Vec:'
print v.array

G = GPUArray.getGPUArray(v)
print 'GPUArray constructed from PETSc Vec:'
print G

print 'Modified GPUArray:'
G.fill(4.0)
print G

print 'PETSc Vec changes too:'
print v.array

v.destroy()
