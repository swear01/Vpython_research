from random import uniform
from vpython import *



dt = 1e-5
G = 1
N = 3

# funcs
def grvt(ma,pa,pb):
    return ma*G/mag2(pa-pb)*norm(pa-pb)

ms = [uniform(0.3,1) for _ in range(N)]
vs = [vector(uniform(-0.2,0.2),uniform(-0.2,0.2),uniform(-0.2,0.2)) for _ in range(N-1)]
pos = [vector(uniform(-0.4,0.4),uniform(-0.4,0.4),uniform(-0.4,0.4)) for _ in range(N)]

momentum = vec(0,0,0)
for vsi, msi in zip(vs, ms):
    momentum += vsi*msi

vs.append(-momentum/ms[N-1]) #make total momentum = 3

scene = canvas(width = 800, height = 800)
blits = [sphere(radius=0.05, make_trail=True, color=vector(random(),random(),random())) for _ in range(N)]
blits[0].color = vector(1,0,0)
blits[1].color = vector(0,1,0)
blits[2].color = vector(0,0,1)

while True:
    rate(1000000)
    for i in range(N):
        for j in range(i):
            if mag(pos[i]-pos[j]) < 0.1:
                #formula https://en.wikipedia.org/wiki/Elastic_collision
                v1 = vs[i] - (2*ms[j])/(ms[i]+ms[j])*(pos[i]-pos[j])*dot(vs[i]-vs[j],pos[i]-pos[j])/mag2(pos[i]-pos[j])
                v2 = vs[j] - (2*ms[i])/(ms[i]+ms[j])*(pos[j]-pos[i])*dot(vs[i]-vs[j],pos[i]-pos[j])/mag2(pos[i]-pos[j])
                vs[i], vs[j] = v1, v2
    
    for i in range(N):
        for j in range(i):
            vs[i] += grvt(ms[j],pos[j],pos[i])*dt
            vs[j] += grvt(ms[i],pos[i],pos[j])*dt
                        
    for i in range(N):
        pos[i] += vs[i]*dt
        blits[i].pos = pos[i]         
    