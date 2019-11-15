from vpython import *
#GlowScript 2.8 VPython
# Parameters
xi = 0   # initial position 
vi = 4     # initial velocity
t_end = 20  # length of simulation
m = 1       # mass
dt = 0.001   # timestep

# Potential energy function
def U_func(x):
    '''Change the potential energy function here, as directed'''
    U = cos(x**2)**3 *x
    return U
    
def K_func():
    K = 1/2 * m * v**2
    return K
    
def Total_func():
    T = K + U
    return T
  
# Warning if Glowscript version 2.9 is used
if str(type(U_func)) != "<class 'builtin_function_or_method'>":
    print("Incompatible version!") 
    print("Please change the top line of the code to:")
    print("Glowscript 2.8 Python")
    return

# Force function (numerical derivative)  
def F_func(U, x):
    dx = 0.0001
    return -( U(x+dx) - U(x-dx) ) / (2*dx)

# Plot curve of U(x)
Ucurve = gcurve(color=vec(1,0.5,0))
xmin = -1.5
xmax = 1.5
x1 = xmin
dx = 0.01
while x1 < xmax+dx:
    Ucurve.plot(x1, U_func(x1))
    x1 = x1 + dx

# Initialize curves to plot K, U, and E=K+U as the particle moves
Kplot = gcurve(color=color.green, dot=True)
Uplot = gcurve(color=vec(1,0.5,0), dot=True)
Eplot = gcurve(color=color.blue, dot=True)

print("Legend:")
print("U = orange")
print("K = green")
print("E = blue")

# Set position, velocity, and time  to initial conditions 
x = xi
v = vi
t = 0

# Simulation loop
while t <= t_end:
    rate(2/dt) # Show the simulation at a moderate speed (2x real time)
    # Plot current potential energy
    U = U_func(x) # current potential energy
    Uplot.plot(x, U)
    '''(2a) Plot current kinetic energy'''
    K = K_func()
    Kplot.plot(x, K)
    '''(2b) Plot current total energy'''
    T = Total_func()
    Eplot.plot(x, T)
    # Update motion to new timestep
    F = F_func(U_func, x) # current force on particle
    v += F/m * dt
    x += v * dt
    t += dt