from vpython import *

K, G = 1e6, 10
dt = 1e-4

class Nunchakus:
    def __init__(self, r, a1, a2):
        self.r = r
        x1, y1 = r*cos(a1), r*sin(a1)
        x2, y2 = x1+r*cos(a2), y1+r*sin(a2)
        self.node1 = sphere(radius=0.1*r, color=color.blue, pos=vec(x1,y1,0), v=vec(0,0,0), make_trail=True, retain=10)
        self.node2 = sphere(radius=0.1*r, color=color.red, pos=vec(x2,y2,0), v=vec(0,0,0), make_trail=True, retain=10)
        self.spring1 = cylinder(radius=0.01*r, color=color.white, pos=vec(0,0,0), axis=self.node1.pos)
        self.spring2 = cylinder(radius=0.01*r, color=color.white, pos=self.node1.pos, axis=self.node2.pos-self.node1.pos)
        
                
    def tick(self):
        self.spring1.axis = self.node1.pos
        self.spring2.pos = self.node1.pos
        self.spring2.axis = self.node2.pos-self.node1.pos
        
        self.node1.v += -K*(mag(self.spring1.axis)-self.r)*norm(self.spring1.axis)*dt
        self.node1.v += K*(mag(self.spring2.axis)-self.r)*norm(self.spring2.axis)*dt
        self.node1.v += vec(0,-G,0)*dt
        
        self.node2.v += -K*(mag(self.spring2.axis)-self.r)*norm(self.spring2.axis)*dt
        self.node2.v += vec(0,-G,0)*dt
        
        self.node1.pos += self.node1.v*dt
        self.node2.pos += self.node2.v*dt

    def set_color(self, color):
        self.node1.color = color 
        self.node1.trail_color = color       
        self.node2.color = color       
        self.node2.trail_color = color   
        self.spring1.color = color        
        self.spring2.color = color        


        
ns = [Nunchakus(1,-(0.2+i*0.001)*pi, 0.8*pi) for i in range(7)]
ns[0].set_color(color.red)
ns[1].set_color(color.orange)
ns[2].set_color(color.yellow)
ns[3].set_color(color.green)
ns[4].set_color(color.cyan)
ns[5].set_color(color.blue)
ns[6].set_color(color.purple)

while True:
    rate(100000)
    for n in ns:
        n.tick()