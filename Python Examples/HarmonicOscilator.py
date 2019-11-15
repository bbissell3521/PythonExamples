from vpython import *
#GlowScript 2.9 VPython
ball = sphere(pos=vec(0,10,0), radius=.2, mass=0.5, vel=vec(0,0,0), color=color.green, opacity=0.7, make_trail=True)
center = sphere(radius=0.1)

dt = 0.001
t = 0
k = 20
timeofcrossing = 0
flag = True
p=3

def force(obj):
    obj.force = -k * (mag(obj.pos - center.pos)**p) * hat(obj.pos - center.pos)
    

plot = False #(2a)
if plot:
    gpos = gcurve(color=color.blue) # Creates a curve on the graph
    gpos.plot(t, ball.pos.y) # Adds a data point to the graph
    
    gvel = gcurve(color=color.green)
    gvel.plot(t, ball.vel.y)
    
    gacc = gcurve(color=color.red)

while True:
    rate(1/dt)
    t += dt
    # (1a) Update force
    force(ball)
    # (1b) Update velocity and position
    ball.acc = ball.force/ball.mass
    ball.vel = ball.vel + ball.acc * dt
    ball.pos = ball.pos + ball.vel * dt
    if plot:
        # (2b) Add a new data point to the graph
        gpos.plot(t,ball.pos.y)
        gvel.plot(t, ball.vel.y)
        gacc.plot(t, ball.acc.y)
    # (3) Check if crosses the origin going downwards.
    
    
    patstart = ball.pos.y
    if patstart <= 0:
        if flag == True:
            timei = -((ball.pos.y - 0)/ball.vel.y) + t
            print('timei =', timei)
            #print('time = ', t)
            if timeofcrossing != 0:
                period = timeofcrossing - t
                print('period = ', abs(period))
            timeofcrossing = t
            flag = False
    else if patstart >= 0:
        flag = True
        
   # if t >= 11:
    #  scene.pause('haha')
    # If so, print the time of crossing 
    # and the difference from the previous crossing time, if applicable.