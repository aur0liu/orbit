#where the physics actually happens

import math as maths

from renderer import *


# --------------------- CONSTANTS ---------------------

#gravitational constant
#G = (6.674 * 10**-11) * ((6 * 10**24)/(10**27)) #units m3 kg-1 s-2
    #real value         #scale factor
#G = (6.674 * 10**-11) #real value
G = 1 #arbitrary units

#worldspace to screenspace multiplier
WORLD_TO_SCREEN = 1/175

#timestep
dt = 1/10



class Body:
    def __init__(self, name, mass, x, y, vx, vy, radius, num_sides, colour):
        self.name = name
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.radius = radius
        self.num_sides = num_sides
        self.colour = colour

        self.verts_raw = body_verts(self.radius, self.num_sides, 1)
        self.verts_scaled = body_verts(self.radius, self.num_sides, WORLD_TO_SCREEN)



def initial_velocity(bodies, G):
    #determine initial velocity for stable orbit
    for body in bodies: #for each body calculate its initial velocity
        velocity = 0
        total_vx = 0
        total_vy = 0
        for other in bodies: #calculate force on body from every other body
            if other != body: #and (body.mass/other.mass) < 0.01: #only calculate this if mass of body is much smaller than other body
                if not (body.x == other.x and body.y == other.y):
                    dx = other.x - body.x
                    dy = other.y - body.y
                    r = maths.sqrt(dx**2 + dy**2)
                else:
                    dx = 0
                    dy = 0
                    r = 0.01
                
                velocity += maths.sqrt((G*other.mass)/r) #find velocity by equating gravitational force with required centripetal force
                total_vx += velocity * (-dy/r) 
                total_vy += velocity * (dx/r)
        body.vx = total_vx 
        body.vy = total_vy 
        print(f'initial vx is {body.vx}, initial vy is {body.vy}')

    return bodies


def euler_gravitation(body, bodies, G, dt):
    acc_x = 0
    acc_y = 0

    for other in bodies:
        if other != body: #and (body.mass/other.mass) < 0.01:
            #calculate distance between bodies
            dx = other.x - body.x
            dy = other.y - body.y
            #print(f'dx: {dx}, dy: {dy}')
            r = maths.sqrt(dx**2 + dy**2)
            #print(f'r:{r}')

            #acceleration
            acc = G * (other.mass)/(r**2)
            #print(f'acc:{acc}')

            acc_x += acc * (dx/r) #using trig ratios rather than trig functions to calculate acc
            acc_y += acc * (dy/r)
            #print(f'acc_x: {acc_x}, acc_y: {acc_y}')
            
    #velocity
    body.vx += acc_x * dt #euler integration further pure yayyy
    body.vy += acc_y * dt
    #print(f'vx:{body.vx}, vy:{body.vy}')
    
    #position
    body.x += body.vx * dt
    body.y += body.vy * dt  
    #print(f'x:{body.x}, y:{body.y}') 

    return body
