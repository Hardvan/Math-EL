import numpy as np
from scipy.integrate import solve_ivp
from dynamic_model import dynamic_model

# ============================= Parameters ===============================
param = {
    'N': 14,  # Number of snake robot links
    'm': 0.406,  # Weight of snake robot link
    'l': 0.0525,  # Radius of snake robot link
    'g': 9.81,  # Gravitational acceleration
    'diameter': 0.30,  # Diameter of a pipeline
    'diameterInfluence': 0.10,  # Auxiliary constant
    'd': 0.30 - 2*0.0525,  # Theoretical diameter for snake robot links
    'dt': 0.01,  # Time increment [s]
    'ct': 0.015,  # Viscous friction coefficient of ground in tangential direction
    'cn': 0.03,  # Viscous friction coefficient of ground in normal direction
    'ut': 0.15,  # Coulomb friction coefficient of ground in tangential direction
    'un': 0.3,  # Coulomb friction coefficient of ground in normal direction
    'ctPipe': 0.08,  # Viscous friction coefficient of pipeline in tangential direction
    'utPipe': 0.2,  # Coulomb friction coefficient of pipeline in tangential direction
    'umax': 3,  # Maximum snake robot link torque
    'qmax': 400*0.01,  # Contact parameter
    'Erub': 400000,  # Contact parameter
    'vrub': 0.49,  # Contact parameter
    'friction': 1,  # Choice of friction: 0 - Coulomb, 1 - viscous
    'contact': 1,  # Choice of side walls contact: 0 - without contact, 1 - with contact
    'minLinkVel': 0.001,  # Auxiliary variable of snake robot link angular velocity
    'dimensionPlot3D': 0,  # Choice of a graph: 0 - 2D, 1 - 3D
    'resultsShow': 0,  # Choice of animation: 0 - show simulation, 1 - show graphs
    'kp': 25,  # Gain for position controller
    'kd': 10,  # Gain for velocity controller
    'alphaA': 0.3981,
    'omega': 0.6936,
    'delta': 0.4914,
    'offset': 0
}

t = np.arange(0, 20, param['dt'])

# Initial values for trajectory
phi_required = {}
phi_reference = np.zeros(param['N']-1)
for i in range(param['N']-1):
    phi = param['alphaA'] * np.sin(param['omega'] * t + i * param['delta'])
    phi_required[i] = phi
    phi_reference[i] = phi[0]

# Initial values
theta = np.zeros(param['N'])
thetaDot = np.zeros(param['N'])
phi = np.zeros(param['N']-1)
phiDot = np.zeros(param['N']-1)
p = np.zeros(2)
pDot = np.zeros(2)
qa = phi
qu = np.array([theta[-1], p[0], p[1]])
qaDot = phiDot
quDot = np.array([thetaDot[-1], pDot[0], pDot[1]])
x0 = np.concatenate([qa, qu, qaDot, quDot])

# Solution
solution = solve_ivp(lambda t, y: dynamic_model(
    t, y, param), [t[0], t[-1]], x0, t_eval=t)

# The results of snake robot motion are in solution.y
X = solution.y  # The matrix X contains the results
