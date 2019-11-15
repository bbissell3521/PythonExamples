from vpython import *
#GlowScript 2.9 VPython
s1 = sphere()
s2 = sphere(pos=vec(6,0,0), radius=3, color=vec(0,0,1), opacity = 0.3)
s3 = sphere(pos=vec(-6,0,0), size=vec(3,1,3), axis=vec(1,1,0), opacity = 0.3)
flag = bool(False)
flag2 = bool(False)
flag3 = bool(False)

objects = [s1, s2]


b1 = box(pos=vec(0,-3,0), size=vec(12,0.5,4), color=vec(1,0.5,0.25))

#helix(pos = vec(3,5,0), size = vec(2,4,10))

#this will change the color when you click on the picture
scene.pause()
s1.color = vec(0.5,0.5,1)

#this will move it up 1 on click 
#scene.pause()
#s1.pos = s1.pos + vec(0,1,0)

#moves this up 1 more click
#scene.pause()
#s1.pos += vec(0,1,0)

s1.vel = vec(5,2,0)
s2.vel = vec(-3,0,0)
s3.vel = vec(1,1,0)
b1.vel = vec(0,2,0)

t = 0
dt = 1/60

while True:
    rate(1/dt)
    t += dt
    for obj in objects:
        obj.pos += obj.vel*dt
        if obj.pos.x > 6 or obj.pos.x < -6 or obj.pos.y > 6 or obj.pos.y < -6:
            if flag3 == bool(False):
                obj.vel *= -1
                obj.vel *= .125
                flag3 = bool(True)
            else if flag3 = bool(True):
                obj.vel *= .125
                flag3 = bool(False)
            
            
            
    if t > 1 and flag == bool(False):
        objects.append(s3)
        flag = bool(True)
    
    if t > 5 and flag2 == bool(False):
        objects.append(b1)
        flag2 = bool(True)
        b1.color = vec(0.75,0.25,0)



