from vpython import *
#GlowScript 2.9 VPython
scene.width = 1250
scene.height = 550

# System objects
earth = sphere(radius=6371000, color = vec(0,5,0) , mass = 5.9742e24)
moon = sphere(radius = 1736000, color = vec(1,0,0), mass = 0.07346e24)
ship = sphere(radius = 1e6, color = vec(5,5,0), make_trail = True, interval = 10, mass = 15000)
G = 6.67e-11

# Initial positions
earth.pos = vec(-192500000,0,0)
moon.pos = vec(192500000,0,0)
ship.pos = vec(-10*earth.radius+earth.pos.x,0,0)
# Initial velocity of the ship
ship.vel = vec(0,3257.92,0)

# Gravitational force function
def force(ship, other):
    global crashed # access the crashed variable outside this function
    r = ship.pos - other.pos
    if r.mag < other.radius:
        crashed = True
    return (-6.67e-11*((ship.mass * other.mass)/mag(r)**2)*hat(r))

# Simulation loop goes here
crashed = False
t = 0
dt = 60

while not crashed:
    rate(10000)
    t += dt
    f = force(ship, earth) + force(ship, moon)
    ship.vel += f/ship.mass * dt
    ship.pos += ship.vel * dt