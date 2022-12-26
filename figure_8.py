from random import uniform
from vpython import *

dt = 1e-5
G = 1

#vx, vy = 0.3471128135672417, 0.532726851767674 #stable solution
vx, vy = 0.4, 0.5

# funcs
def grvt(ma,pa,pb):
    return ma*G/mag2(pa-pb)*norm(pa-pb)

sa = sphere(radius=0.05, make_trail=True, color=color.yellow,pos=vec(-1,0,0),v=vec(vx,vy,0))
sb = sphere(radius=0.05, make_trail=True, color=color.blue,pos=vec(0,0,0),v=vec(-2*vx,-2*vy,0))
sc = sphere(radius=0.05, make_trail=True, color=color.red,pos=vec(1,0,0),v=vec(vx,vy,0))

while True:
    rate(100000)
    for i in [sa,sb,sc]:
        for j in [sa,sb,sc]:
            if i == j : continue
            j.v += grvt(1,i.pos,j.pos)*dt
                        
    for i in [sa,sb,sc]:
        i.pos += i.v*dt