from random import uniform
from vpython import *

dt = 2e-5
G = 1
R = 1
ma = 71.44
mb = 11.01
mc = 0.00001
point = 'L4'

# funcs
def L1(ma, mb, r):
    rb = ma/(ma+mb)*r
    ra = mb/(ma+mb)*r
    def iter(ma, mb, x):
        return sqrt( ((mb/ma)*rb*r**2*(r+x)**2) / ((rb + x)*(r + x)**2-rb*r**2) )        
    
    x = 0.5
    while True:
        next_x = iter(ma, mb, x)
        if abs(next_x-x) < 1e-10 : return vector(next_x+r,0,0)
        x = next_x
 
def L2(ma, mb, r):
    rb = ma/(ma+mb)*r
    ra = mb/(ma+mb)*r
    def iter(ma, mb, x):
        return sqrt( ((mb/ma)*rb*r**2*(r-x)**2) / (rb*r**2-(rb - x)*(r - x)**2) )
    
    x = 0.5
    while True:
        next_x = iter(ma, mb, x)
        if abs(next_x-x) < 1e-10 : return vector(-next_x+r,0,0)
        x = next_x
        
def L3(ma, mb, r):
    rb = ma/(ma+mb)*r
    ra = mb/(ma+mb)*r
    def iter(ma, mb, x):
        return sqrt( ((ma/mb)*ra*r**2*(r+x)**2) / ((ra + x)*(r + x)**2-ra*r**2) )        
    x = 0.5
    while True:
        next_x = iter(ma, mb, x)
        if abs(next_x-x) < 1e-10 : return vector(-next_x,0,0)
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
        
def grvt(ma,pa,pb):
    if pa == pb : return 0
    return ma*G/mag2(pa-pb)*norm(pa-pb)

def gravity(a:sphere,b:sphere,c:sphere):
    return grvt(b.m,b.pos,a.pos) + grvt(c.m,c.pos,a.pos)

def init_omega(a,b,c):
    com = (a.m*a.pos+b.m*b.pos+c.m*c.pos)/(a.m+b.m+c.m)
    # calculation base on c
    acc:vector = gravity(c,a,b)
    r = c.pos-com
    v = vector(-acc.y,acc.x,0)*sqrt(mag(r))
    v = v/sqrt(mag(v))
    omega = cross(r,v)/mag2(r)
    return omega 

def rk4th(a, b, c, dt): #gravity is state variable
    #f is pos
    def gc(tag, ma,mb,mc,pa,pb,pc):
        match tag :
            case 'a':
                return grvt(mb,pb,pa) + grvt(mc,pc,pa)
            case 'b':
                return grvt(ma,pa,pb) + grvt(mc,pc,pb)
            case 'c':
                return grvt(mb,pb,pc) + grvt(ma,pa,pc)
    def step(tag,ma,mb,mc,pa,pb,pc,va,vb,vc,dt,k):
        return gc(tag,ma,mb,mc,pa+k*dt*va,pb+k*dt*vb,pc+k*dt*vc)
    
    v1 = {'a':a.v,'b':b.v,'c':c.v}
    a1= {}
    for tag in ['a','b','c']:
        a1[tag] = step(tag,a.m,b.m,c.m,a.pos,b.pos,c.pos,v1['a'],v1['b'],v1['c'],dt,0)

    a2, v2={}, {}
    for tag in ['a','b','c']:
        a2[tag] = step(tag,a.m,b.m,c.m,a.pos,b.pos,c.pos,v1['a'],v1['b'],v1['c'],dt,0.5)
        v2[tag] = v1[tag]+a2[tag]*0.5*dt        

    a3, v3={}, {}
    for tag in ['a','b','c']:
        a3[tag] = step(tag,a.m,b.m,c.m,a.pos,b.pos,c.pos,v2['a'],v2['b'],v2['c'],dt,0.5)
        v3[tag] = v1[tag]+a3[tag]*0.5*dt        

    a4, v4={}, {}
    for tag in ['a','b','c']:
        a4[tag] = step(tag,a.m,b.m,c.m,a.pos,b.pos,c.pos,v3['a'],v3['b'],v3['c'],dt,1)
        v4[tag] = v1[tag]+a4[tag]*dt    
        
    a.v += 1/6*(a1['a']+2*a2['a']+2*a3['a']+a4['a'])*dt
    b.v += 1/6*(a1['b']+2*a2['b']+2*a3['b']+a4['b'])*dt
    c.v += 1/6*(a1['c']+2*a2['c']+2*a3['c']+a4['c'])*dt
    a.pos += 1/6*(v1['a']+2*v2['a']+2*v3['a']+v4['a'])*dt
    b.pos += 1/6*(v1['b']+2*v2['b']+2*v3['b']+v4['b'])*dt
    c.pos += 1/6*(v1['c']+2*v2['c']+2*v3['c']+v4['c'])*dt
    return 

com = (ma*sa.pos+mb*sb.pos+mc*sc.pos)/(ma+mb+mc)
omega = init_omega(sa,sb,sc)
sa.v = cross(omega,sa.pos-com)
sb.v = cross(omega,sb.pos-com)
sc.v = cross(omega,sc.pos-com)
        
while True:
    rate(10000)
    rk4th(sa,sb,sc,dt)
        
        
# def rk4th(func, a, b, c, dt): #gravity is state variable
#     #f is pos
#     f1i = func(b.m,b.pos,i.pos)
#     f1j = func(i.m,i.pos,j.pos)
#     f2i = func(j.m,j.pos+0.5*dt*f1j,i.pos+0.5*dt*f1i)
#     f2j = func(i.m,i.pos+0.5*dt*f1i,j.pos+0.5*dt*f1j)
#     f3i = func(j.m,j.pos+0.5*dt*f2j,i.pos+0.5*dt*f2i)
#     f3j = func(i.m,i.pos+0.5*dt*f2i,j.pos+0.5*dt*f2j)
#     f4i = func(j.m,j.pos+dt*f3j,i.pos+dt*f3i)
#     f4j = func(i.m,i.pos+dt*f3i,j.pos+dt*f3j) 
#     a_i = 1/6*(f1i+2*f2i+2*f3i+f4i) # need dt times      
#     a_j = 1/6*(f1j+2*f2j+2*f3j+f4j)
#     return a_i, a_j
               