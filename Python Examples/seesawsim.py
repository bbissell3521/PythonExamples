from vpython import *
#GlowScript 2.9 VPython

''' Glowscript documentation:
    https://www.glowscript.org/docs/GlowScriptDocs/index.html '''

# beam of seesaw
beam = box(size=vec(1, 0.03, 0.005), color=vec(1,0.75,0.5), mass=0.200, omega=0)
''' Compute the moment of inertia of the beam pivoted about the center of mass.  '''
I = 1/12*(beam.mass*((beam.size.x**2)+(beam.size.y**2)))

# pivot point and axle
pivot = vec(-0.058,0.015,0)
length = 0.1
axle = cylinder(pos=pivot-vec(0,0,length/2), axis=vec(0,0,length), radius=0.005, color=vec(1,0,0))
''' Apply the parallel axis theorem to modify the moment of inertia to be about this pivot point. '''
Ip = I + beam.mass*(mag(beam.pos - pivot) ** 2)
print('Ip', Ip)

# weights
density = 3000
weight1 = sphere(pos=vec(0.3, 0, 0), radius=0.02)
weight2 = sphere(pos=vec(-0.3, 0, 0), radius=0.025)
''' Assign a mass to each weight based on volume and density. '''
weight1.mass = (4 * pi)*(weight1.radius**3/3) * density
weight2.mass = (4 * pi) * (weight2.radius**3/3) * density
print('Mass 1', weight1.mass)
print('Mass 2', weight2.mass)
''' The weights will be rigidly bonded to the beam, we we can treat 
    the beam plus weights as one rigid object with one moment of inertia.
    Compute the additional moment of inertia from each weight. ''' 
Iw1 = (2/5) * weight1.mass * weight1.radius**2
Iw2 = (2/5) * weight1.mass * weight1.radius**2
''' The total moment of inertia of the system should be stored in one variable. '''
Itot = Ip + Iw1 + Iw2
print('Itot =', Itot)
t = 0
dt = 0.01
gravity = vec(0, -9.8, 0)

angle_graph = gcurve(color=color.red)

while True:
    # Limits frame rate.
    rate(1/dt)
    
    ''' Plot the angle as a function of time, using beam.axis.  (Look it up.) '''
    angle_graph.plot(t,degrees(atan(beam.axis.y/beam.axis.x)))
    ''' Set torque to zero. '''
    beam.torque = vec(0,0,0)
    ''' Add the torque from gravity acting on the beam and on the weights. '''
    beam.torque += cross(beam.pos - pivot, beam.mass * gravity)
    beam.torque += cross(weight1.pos - pivot, weight1.mass * gravity)
    beam.torque += cross(weight2.pos - pivot, weight2.mass * gravity)
    #print('beam torque', beam.torque)
    ''' Update omega (angular velocity) '''
    beam.omega += beam.torque.z/Itot*dt
    #print('beam.omega', beam.omega)
    # This adds viscous friction to the axle so the motion settles to equilibrium.  
    beam.omega *= 1 - 0.02
    
    ''' Use the rotate function to rotate each object around the z axis 
        by the proper amount about the pivot point. (Look it up.) '''
    beam.rotate(angle = beam.omega * dt, origin = pivot, axis = vec(0,0,1))
    weight1.rotate(angle = beam.omega * dt, origin = pivot, axis = vec(0,0,1))
    weight2.rotate(angle = beam.omega * dt, origin = pivot, axis = vec(0,0,1))
    # Updates time.
    t += dt
    