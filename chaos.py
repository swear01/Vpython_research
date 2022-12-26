from random import uniform
from vpython import *



dt = 1e-4
G = 1
N = 10

# funcs
def grvt(ma,pa,pb):
    return ma*G/mag2(pa-pb)*norm(pa-pb)

ms = [uniform(0.1,1) for _ in range(N)]
vs = [vector(random(),random(),random()) for _ in range(N)]
pos = [vector(random(),random(),random()) for _ in range(N)]

scene = canvas(width = 600, height = 400)
blits = [sphere(radius=0.05, make_trail=True, color=vector(random(),random(),random())) for _ in range(N)]
blits[0].color = vector(1,0,0)
blits[1].color = vector(0,1,0)
blits[2].color = vector(0,0,1)

while True:
    rate(1000)
    for i in range(N):
        for j in range(i):
            vs[i] += grvt(ms[j],pos[j],pos[i])*dt
            vs[j] += grvt(ms[i],pos[i],pos[j])*dt
                        
    for i in range(N):
        pos[i] += vs[i]*dt
        blits[i].pos = pos[i]         
    