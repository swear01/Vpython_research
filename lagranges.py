from random import uniform
from vpython import *

dt = 1e-5
G = 1
R = 1
ma = 10
mb = 0.99
mc = 0.0001
point = 'L2'

# funcs
def init_omega(ma, mb, mc, pa, pb, pc):
    com = (ma*pa+mb*pb+mc*pc)/(ma+mb+mc)
    # calculation base on c
    a:vector = grvt(ma,pa,pc)+grvt(mb,pb,pc)
    r = pc-com
    v = vector(-a.y,a.x,0)*sqrt(mag(r))
    v = v/sqrt(mag(v))
    omega = cross(r,v)/mag2(r)
    return omega 

def grvt(ma,pa,pb):
    return ma*G/mag2(pa-pb)*norm(pa-pb)

def L1(ma, mb, r):
    rb = ma/(ma+mb)*r
    ra = mb/(ma+mb)*r
    def iter(ma, mb, x):
        return sqrt( ((mb/ma)*rb*r**2*(r+x)**2) / ((rb + x)*(r + x)**2-rb*r**2) )        
    
    x = 0.1
    while True:
        next_x = iter(ma, mb, x)
        if abs(next_x-x) < 1e-45 : return vector(next_x+r,0,0)
        x = next_x

        
def L2(ma, mb, r):
    rb = ma/(ma+mb)*r
    ra = mb/(ma+mb)*r
    def iter(ma, mb, x):
        return sqrt( ((mb/ma)*rb*r**2*(r-x)**2) / (rb*r**2-(rb - x)*(r - x)**2) )
    
    x = 0.1
    while True:
        next_x = iter(ma, mb, x)
        if abs(next_x-x) < 1e-45 : return vector(-next_x+r,0,0)
        x = next_x
        
def L3(ma, mb, r):
    rb = ma/(ma+mb)*r
    ra = mb/(ma+mb)*r
    def iter(ma, mb, x):
        return sqrt( ((ma/mb)*ra*r**2*(r+x)**2) / ((ra + x)*(r + x)**2-ra*r**2) )        
    x = 0.1
    while True:
        next_x = iter(ma, mb, x)
        if abs(next_x-x) < 1e-45 : return vector(-next_x,0,0)
        x = next_x
        
def L4(ma,mb,r):
    return vector(0.5*r,sqrt(3)/2*r,0)

def L5(ma,mb,r):
    return vector(0.5*r,-sqrt(3)/2*r,0)

scene = canvas(width = 800, height = 800)
sa = sphere(radius=0.1*R, make_trail=True, color=color.yellow, m=ma)
sb = sphere(radius=0.04*R, make_trail=True, color=color.blue, m=mb)
sc = sphere(radius=0.04*R, make_trail=True, color=color.white, m=mc)

sa.pos = vector(0,0,0)
sb.pos = vector(R,0,0)
match point:
    case 'L1':
        sc.pos = L1(ma,mb,R)
    case 'L2':
        sc.pos = L2(ma,mb,R)
    case 'L3':
        sc.pos = L3(ma,mb,R)
    case 'L4':
        sc.pos = L4(ma,mb,R)
    case 'L5':
        sc.pos = L5(ma,mb,R)
        
com = (ma*sa.pos+mb*sb.pos+mc*sc.pos)/(ma+mb+mc)
omega = init_omega(ma,mb,mc,sa.pos,sb.pos,sc.pos)
sa.v = cross(omega,sa.pos-com)
sb.v = cross(omega,sb.pos-com)
sc.v = cross(omega,sc.pos-com)


while True:
    rate(100000)
    for i in [sa,sb,sc]:
        for j in [sa,sb,sc]:
            if i == j : continue
            j.v += grvt(i.m,i.pos,j.pos)*dt
                        
    for i in [sa,sb,sc]:
        i.pos += i.v*dt