from vpython import *
#GlowScript 2.9 VPython
#scene.range 


s = sphere(make_trail=True, mass=1)
#attach_arrow(s, "vel", color = color.green, shaftwidth = 0.3)
#attach_arrow(s, "force", color = color.yellow, shaftwidth = 0.3)

scene.camera.follow(s)
#initial Conditions
s.pos = vec(0,0,0)
s.vel = vec(0,5,0)

def force(obj):
    obj.force = -mag2(obj.vel)*hat(obj.vel)

scene.pause()

dt = 0.0001
t = 0

while True:
    rate(1/dt)
    t += dt
    force(s)                            #update force
    s.vel = s.vel + (s.force/s.mass)*dt #update velocity
    s.pos += s.vel*dt                   #update position

    
    
    