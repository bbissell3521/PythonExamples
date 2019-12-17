from vpython import *
#GlowScript 2.9 VPython
scene.autoscale = False
scene.height = 512
scene.width = 800

throwTrue = False
end = False

restitution = 0.6


# ------------------------ Create Ball and Alley ------------------------
ball = sphere(
    pos = vec(0,0,0),
    posContact = vec(0,0,0),
    radius = 0.10795,
    mass = 6,
    vel = vec(0,0,0),
    velContact = vec(0,0,0),
    velInitial = 10,
    omega = vec(0,0,0),
    torque = vec(0,0,0),
    force = vec(0,0,0),
    angle = 0,
    color = vec(1,1,1),
    inertia = 0, 
    texture = "https://tr.rbxcdn.com/8ba6f75ad5678ba49a38f7b50109544f/420/420/Decal/Png"
    )
ball.inertia = (2 / 5) * ball.mass * (ball.radius ** 2)
ball.posContact = vec(0,-ball.radius,0)
ball.velContact = vec(0,0,0)

alley = box(
    pos = vec(0,-ball.radius - 0.25,-8),
    size = vec(1.05,0.5,21),
    color = vec(0.85,0.75,0.5),
    friction = 0.035,
    texture = textures.wood,
    shininess = 1.0
    )

back = box(
    pos = vec(0,1,alley.pos.z - (alley.size.z / 2) - 0.5),
    size = vec(alley.size.x + 1,4,1),
    color = vec(0.1,0.1,0.1),
    opacity = 0.8
    )

bumperL = box(
    pos = vec((-alley.size.x / 2) - 0.05,-0.2,alley.pos.z + 1),
    size = vec(0.1,0.6,alley.size.z - 2),
    color = vec(0.5,0.5,0.5)
    )

bumperR = box(
    pos = vec((alley.size.x / 2) + 0.05,-0.2,alley.pos.z + 1),
    size = vec(0.1,0.6,alley.size.z - 2),
    color = vec(0.5,0.5,0.5)
    )

startLine = box(
    pos = vec(0,-ball.radius,0),
    size = vec(alley.size.x,0.01,0.1),
    color = vec(0.2,0.8,0.9),
    opacity = 0.4,
    emissive = True
    )

lightHeight = 10
light1 = local_light(
    pos = vec(-16,lightHeight,-alley.size.z / 2 - 2),
    color = vec(0.8,0.7,0.5)
    )

light2 = local_light(
    pos = vec(16,lightHeight,-alley.size.z / 2 - 2),
    color = vec(0.8,0.7,0.5)
    )

# Create arrow that represents initial velocity
arrowVelocity = attach_arrow(ball, "vel", scale=0.1, shaftwidth=0.05,
                             color=color.green)


# ------------------------ Create Pins ------------------------
sizePin = vec(ball.radius * 2,0.12,0.12)
pinOffsetY = alley.pos.y + (alley.size.y / 2)
class Pin:
    def __init__(self,xPos,zPos):
        pins.append(cylinder(
            pos = vec(xPos,pinOffsetY,zPos),
            axis = vec(0,1,0),
            mass = 1.5,
            vel = vec(0,0,0),
            force = vec(0,0,0),
            omega = vec(0,0,0),
            size = sizePin,
            inertia = 0
        )
    )

pins = []

pin0 = Pin(0,-alley.size.z + 0.75)
pin1 = Pin(0.15,-alley.size.z + 0.5)
pin2 = Pin(-0.15,-alley.size.z + 0.5)
pin3 = Pin(0,-alley.size.z + 0.25)
pin4 = Pin(0.3,-alley.size.z + 0.25)
pin5 = Pin(-0.3,-alley.size.z + 0.25)
pin6 = Pin(0.15,-alley.size.z)
pin7 = Pin(-0.15,-alley.size.z)
pin8 = Pin(0.45,-alley.size.z)
pin9 = Pin(-0.45,-alley.size.z)

# Calculate moment of inertia of each pin
# Add starting position to a array for scoring
i = 0
pinPos = []
for pin in pins:
    pin.inertia = ((1 / 4) * pin.mass * ((pin.size.z / 2)**2)
                + (1 / 12) * pin.mass * (pin.size.y**2))
    pin.pos.z += 3.5
    global pinPos
    pinPos.append(pin.pos)
    i += 1


# ------------------------ Collisions ------------------------
def collisionWalls():
    global end
    global t
    global tEnd
    # Collision with back wall
    if (ball.pos.z - ball.radius <= back.pos.z + (back.size.z / 2)):
        ball.vel = vec(0,0,0)
        ball.angle = 0
        ball.force = vec(0,0,0)
        ball.omega = vec(0,0,0)
        ball.torque = vec(0,0,0)
        throwTrue = False
        tEnd = t
        ball.pos.z = back.pos.z + (back.size.z / 2) + 0.01 + ball.radius

    # Collision with bumpers
    if (ball.pos.x - ball.radius <= bumperL.pos.x + (bumperL.size.x / 2)
        and ball.vel.x < 0
        or ball.pos.x + ball.radius >= bumperR.pos.x - (bumperR.size.x / 2)
        and ball.vel.x > 0):
            ball.vel.x *= restitution
            ball.vel.x = -ball.vel.x
        
def collisionBallToPin():
    for pin in pins:
        n = hat(ball.pos - pin.pos)
        n.y = 0
        pinContact = ball.pos - n * ball.radius
        s = pinContact - pin.pos
        v = ball.vel - (pin.vel + cross(pin.omega, s))
        vn = dot(v, n)
        
        # snsn is used if calculating rotation for pins as well
        # sn = cross(s,n)
        # sns = cross(sn,s)
        # snsn = dot(sns,n)
        J = ((-(1 + restitution) * vn)
            / ((1 / ball.mass)+ (1 / pin.mass))) #+ (snsn / pin.inertia)))
        
        dvball = J * n / ball.mass
        dvpin = (-J * n / pin.mass) * 3
        
        cRad = (pin.size.z / 2) + ball.radius
        d = sqrt((ball.pos.x - pin.pos.x)**2 + (ball.pos.z - pin.pos.z)**2)
        if(d < cRad and vn < 0):
            ball.vel += dvball
            pin.vel += dvpin
            
def collisionPinToPin(a, b):
    v = a.vel - b.vel
    n = hat(a.pos - b.pos)
    vn = dot(v,n)
    
    J = ((a.mass * b.mass) * (-(1 + restitution) * vn)) / (a.mass + b.mass)
    dva = J * n / a.mass
    dvb = -J * n / b.mass
    
    d = sqrt((b.pos.x - a.pos.x)**2 + (b.pos.z - a.pos.z)**2)
    if (d < ((a.size.z / 2) + (b.size.z / 2)) or mag(v) < 0):
        a.vel += dva
        b.vel += dvb


# ------------------------ Calculations ------------------------
def calcInitialVel():
    ball.vel = vec(
        ball.velInitial * sin(ball.angle),
        0,
        -ball.velInitial * cos(ball.angle)
        )
    
def calcForceBall():
    ball.force = alley.friction * ball.mass * -9.8 * ball.velContact
    
def calcForcePin():
    pin.force = alley.friction * pin.mass * -9.8 * pin.vel
    
def calcTorque():
    ball.torque = cross(ball.posContact, ball.force)
    
def calcOmega(): 
    if(ball.torque.x != 0):
        ball.omega.x += ball.torque.x / ball.inertia * dt
    if(ball.torque.y != 0):
        ball.omega.y += ball.torque.y / ball.inertia * dt
    if(ball.torque.z != 0):
        ball.omega.z += ball.torque.z / ball.inertia * dt

# Rotate the ball according to omega
def rotateBall():
    global dt
    global ball
    ball.rotate(angle = ball.omega.mag * dt, axis = ball.omega.hat)
    
# Calculate score based on pin movement 
def calcScore():
    global pinPos
    score = 0
    i = 0
    for pin in pins:
        if(pinPos[i] != pin.pos):
            score += 1
        i += 1
    print('Your Score is:', score)


# ------------------------ Camera ------------------------
scene.camera.follow(ball)
scene.camera.pos = ball.pos + vec(0,0.5,0)
scene.camera.axis = vec(0,-1.15,-2.2)


# ------------------------ UI Elements ------------------------
def sVelocity(s):
    global throwTrue
    ball.velInitial = s.value

def sPos(s):
    global throwTrue
    if (throwTrue == False):
        ball.pos.x = s.value

def sAngle(s):
    global throwTrue
    if (throwTrue == False):
        ball.angle = s.value

def sOmega(s):
    global throwTrue
    if (throwTrue == False):
        ball.omega.z = -s.value

def sMass(s):
    global throwTrue
    if (throwTrue == False):
        ball.mass = s.value

def sAlley(s):
    global alley
    global bumperL
    global bumperR
    global back
    if (throwTrue == False):
        alley.size.z = -s.value
        alley.pos.z = alley.size.z / 2.625
        back.pos.z = (alley.size.z * 0.9047) - 0.5
        bumperL.size.z = alley.size.z * 0.90476
        bumperL.pos.z = alley.pos.z + 1
        bumperR.size.z = alley.size.z  * 0.90476
        bumperR.pos.z = alley.pos.z + 1
        i = 0
        for pin in pins:
            if i == 0:
                pins[i].pos.z = alley.size.z * 0.85 + 0.75
            if (i > 0) and (i < 3):
                pins[i].pos.z = alley.size.z * 0.85 + 0.5
            if (i >= 3) and (i < 7):
                pins[i].pos.z = alley.size.z * 0.85 + 0.25            
            if (i >= 7) and (i < 10):
                pins[i].pos.z = alley.size.z * 0.85
            i += 1
            
def bThrow(b):
    global throwTrue
    throwTrue = True
    
def bPause(b):
    global throwTrue
    throwTrue = False
    print('Paused. Press Throw to Resume')

scene.append_to_caption('\n\n')
wtext(text='Velocity: ')
slider(
    bind = sVelocity,
    min = 4,
    max = 16,
    value = 10
    )
scene.append_to_caption('\n\n')

wtext(text='Position: ')
slider(
    bind = sPos,
    min = -0.4,
    max = 0.4,
    value = 0
    )
scene.append_to_caption('\n\n')

wtext(text='Mass:      ')
slider(
    bind = sMass,
    min = 1,
    max = 12,
    value = 6
    )
scene.append_to_caption('\n\n')

wtext(text='Angle:    ')
slider(
    bind = sAngle,
    min = -radians(12),
    max = radians(12),
    value = 0
    )
scene.append_to_caption('\n\n')

wtext(text='Spin:      ')
slider(
    bind = sOmega,
    min = -200,
    max = 200,
    value = 0
    )
scene.append_to_caption('\n\n')

wtext(text='Alley Length: ')
slider(
    bind = sAlley,
    min = 4,
    max = 40,
    value = 21
    )
scene.append_to_caption('\n\n')

button(
    bind=bThrow,
    text="Throw"
    )
        
button(
    bind=bPause,
    text="Pause"
    )


# ------------------------ Simulation Loop ------------------------
dt = 0.01
t = 0
tEnd = 100
doOnce=True

while True:
    rate(1 / dt)
    # Calculate Initial Velocity once, display arrowVelocity before throwing
    if(doOnce):
        calcInitialVel()
        arrowVelocity.start()
        
    # Update ball and pins after ball is thrown
    if (throwTrue):
        # Disable calcInitialVel and arrowVelocity
        doOnce=False
        arrowVelocity.stop()

        ball.velContact = ball.vel + cross(ball.omega, ball.posContact)
        calcForceBall()
        calcTorque()
        calcOmega()
        ball.vel += ball.force / ball.mass * dt
        ball.pos += ball.vel * dt
        rotateBall()
        
        for pin in pins:
            pin.vel += pin.force / pin.mass * dt
            pin.pos += pin.vel * dt
        calcForcePin()
        
        collisionWalls()
        collisionBallToPin()
        for i in range(len(pins)): # range index i over all pins
            for j in range(i):      # range index j, so i,j for all combinations
                collisionPinToPin(pins[i], pins[j])
    

    # When the ball hits back wall, calculate score and exit loop
    if(t > tEnd + 0.5):
        calcScore()
        break
    t += dt
