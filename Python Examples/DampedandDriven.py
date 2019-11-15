from vpython import *
#GlowScript 2.9 VPython
ball = sphere(pos=vec(0,2,0), radius=.2, mass=0.5, vel=vec(0,0,0), color=color.green, opacity=0.7, make_trail=True)
center = sphere(radius=0.1)

attach_arrow(ball, "spring_force", color=color.orange, scale=0.1, shaftwidth=0.1)
attach_arrow(ball, "damping_force", color=color.red, scale=0.1, shaftwidth=0.1)
attach_arrow(ball, "driving_force", color=color.purple, scale=0.1, shaftwidth=0.1)


dt = 0.001
t = 0
k = 20
timeofcrossing = 0
flag = True
p=1

#Energies
potential = 0
moving = 0
total = 0

#Driving Force Constants
D = 20
W = 12
unit= vec(0,1,0)

#Damping Force Constrants
b = 1

def drivingforce(obj):
    obj.force = dampingforce(obj) + unit * D * sin(W*t)
    
def dampingforce(obj):
    obj.force = -k * (mag(obj.pos - center.pos)**p) * hat(obj.pos - center.pos) + (-b * obj.vel)
    
def force(obj):
    force = -k * (mag(obj.pos - center.pos)**p) * hat(obj.pos - center.pos) 
    return force
    
def U_func():
    potential = 1/2 * k * ball.pos.y ** 2
    return potential
    
def K_func():
    moving = 1/2 * ball.mass * mag(ball.vel)**2
    return moving
    
def Total_func():
    total = moving + potential
    return total

plot = True #(2a)
if plot:
    gpotential = gcurve(color=color.orange)
    gpotential.plot(t, potential)

    gmoving = gcurve(color = color.green)
    gmoving.plot(t, moving)
    
    gtotal = gcurve(color = color.purple)
    gtotal.plot(t, total)
    
    gpos = gcurve(color=color.blue) # Creates a curve on the graph
    gpos.plot(t, ball.pos.y)
    
    print("Legend:")
    print("U = orange")
    print("K = green")
    print("E = purple")
    print("pos = blue")

while True:
    rate(1/dt)
    t += dt
    
    ball.damping_force = -b*ball.vel
    ball.driving_force = unit * D * sin(W*t)
    
    # (1b) Update velocity and position
    ball.force = force(ball) + ball.damping_force + ball.driving_force
    # (1b) Update velocity and position
    ball.acc = ball.force/ball.mass
    ball.vel = ball.vel + ball.acc * dt
    ball.pos = ball.pos + ball.vel * dt
    potential = 1/2 * k * ball.pos.y ** 2
    moving = 1/2 * ball.mass * mag(ball.vel)**2
    total = moving + potential
    if plot:
        # (2b) Add a new data point to the graph
       # gpotential.plot(t,potential)
        #gmoving.plot(t, moving)
        #gtotal.plot(t, total)
        gpos.plot(t, ball.pos.y)
    # (3) Check if crosses the origin going downwards.
    
    
    patstart = ball.pos.y
    if patstart <= 0:
        if flag == True:
            timei = -((ball.pos.y - 0)/ball.vel.y) + t
            #print('timei =', timei)
            #print('time = ', t)
            if timeofcrossing != 0:
                period = timeofcrossing - t
                #print('period = ', abs(period))
            timeofcrossing = t
            flag = False
    else if patstart >= 0:
        flag = True
        
    #if t >= 2:
     #scene.pause('haha')
    # If so, print the time of crossing 
    # and the difference from the previous crossing time, if applicable.