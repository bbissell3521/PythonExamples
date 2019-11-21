from vpython import *
#GlowScript 2.9 VPython
balls  = []

restitution = 1
c = 0.01

dt = 0.01

X = 15  # 2*X is the box width
Y = 10  # 2*Y is the box height

create_box()

# Create random balls
create_balls(10)

# Or create balls manually
balls.append(sphere(pos=vec(5,1,0), vel=vec(-5,0,0), mass=1, radius=1))
balls.append(sphere(pos=vec(-5,0,0), vel=vec(5,0,0), mass=1, radius=1))


def collide_walls(s):
    if b.pos.x + b.radius >= X and b.vel.x > 0:
        b.vel.x = -b.vel.x * restitution
    else if b.pos.x - b.radius <= -X and b.vel.x < 0:
        b.vel.x = -b.vel.x * restitution
    else if b.pos.y + b.radius >= Y and b.vel.y > 0:
        b.vel.y = -b.vel.y * restitution
    else if b.pos.y - b.radius <= -Y and b.vel.y < 0:
        b.vel.y = -b.vel.y * restitution
    
 
 
def collide_spheres(a, b):
    n = hat(a.pos - b.pos)
    v = a.vel - b.vel
    vn = dot(v,n)
    
    J = (a.mass*b.mass) * (-(1 + restitution)*vn)/(a.mass + b.mass)
    dva = J * n / a.mass
    dvb = -J * n / b.mass
    
    d = sqrt((b.pos.x - a.pos.x)**2 + (b.pos.y - a.pos.y)**2)
    if(d < b.radius + a.radius and vn < 0):
        b.vel += dvb
        a.vel += dva
    
    
    
    pass
    

# Main Loop
t = 0
while True:
    rate(1/dt) # set frame rate
    # Move balls
    for b in balls:
        b.pos += b.vel*dt
        b.color = fire_color(.5 * b.mass * mag2(b.vel) * c)
        
    # Detect and resolve collisions with other balls
    for i in range(len(balls)): # range index i over all balls
        for j in range(i):      # range index j, so i,j reaches all combinations
            collide_spheres(balls[i], balls[j])
            
    # Detect and resolve collisions with the walls
    for b in balls:
        collide_walls(b)
    
    # Update time
    t += dt
    

def create_balls(n):
    for i in range(n):
        mass = rand(0.1, 3)
        radius = mass**(1/3)
        Xr = X - radius
        Yr = Y - radius
        max_speed = 15
        balls.append(sphere(pos=vec(rand(-Xr,Xr), rand(-Yr,Yr), 0),
                            vel=rand_disk(max_speed), 
                            mass=mass,
                            radius=radius,
                            color=vec(random(),random(), random()),
                            texture=None))

def rand(xmin, xmax):
    return xmin + (xmax - xmin)*random()
    
def rand_disk(radius):
    while True:
        x = rand(-X,X)
        y = rand(-Y,Y)
        if x*x + y*y <= 1:
            break
    return vec(x,y,0)*radius

def create_box():
    d = 0.1  # thickness of walls
    Xd = X+d
    Yd = Y+d
    
    box(pos=vec(-Xd,0,0), size=vec(2*d,2*Yd,6)) 
    box(pos=vec(Xd,0,0), size=vec(2*d,2*Yd,6)) 
    box(pos=vec(0,-Yd,0,0), size=vec(2*Xd,2*d,6)) 
    box(pos=vec(0,Yd,0,0), size=vec(2*Xd,2*d,6)) 

def fire_color(c):
    g = 0.2
    return vec(c, max(c-1,0), max(c-2,0))*(1-g) + g*vec(1,1,1)
