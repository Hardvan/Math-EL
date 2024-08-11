import numpy as np
from scipy.integrate import solve_ivp

# ============================= Parameters ===============================
# Snake robot parameters
param = {
    "N": 14,                                      # Number of snake robot links
    "m": 0.406,                                   # Weight of snake robot link
    "l": 0.0525,                                  # Radius of snake robot link
    "g": 9.81,                                    # Gravitational acceleration
    "diameter": 0.30,                             # Diameter of a pipeline
    "diameterInfluence": 0.10,                    # Auxiliary constant
    # Theoretical diameter for snake robot links
    "d": 0.30 - 2 * 0.0525,
    "dt": 0.01,                                   # Time increment [s]
    # Viscous friction coefficient of the ground in the tangential direction
    "ct": 0.015,
    # Viscous friction coefficient of the ground in the normal direction
    "cn": 0.03,
    # Coulomb friction coefficient of the ground in the tangential direction
    "ut": 0.15,
    # Coulomb friction coefficient of the ground in the normal direction
    "un": 0.3,
    # Viscous friction coefficient of a pipeline in the tangential direction
    "ctPipe": 0.08,
    # Coulomb friction coefficient of a pipeline in the tangential direction
    "utPipe": 0.2,
    "umax": 3,                                    # Maximum snake robot link torque
    "qmax": 400 * 0.01,                           # Contact parameter
    "Erub": 400000,                               # Contact parameter
    "vrub": 0.49,                                 # Contact parameter
    # Choice of friction:   0 - Coulomb, 1 - viscous
    "friction": 1,
    # Choice of side walls contact: 0 - without contact, 1 - with contact
    "contact": 1,
    # Auxiliary variable of snake robot link angular velocity
    "minLinkVel": 0.001,
    # Choice of a graph:    0 - 2D, 1 - 3D
    "dimensionPlot3D": 0,
    # Choice of animation:  0 - show simulation, 1 - show graphs
    "resultsShow": 0,
    "kp": 25,                                     # Gain for position controller
    "kd": 10,                                     # Gain for velocity controller
    "alphaA": 0.3981,
    "omega": 0.6936,
    "delta": 0.4914,
    "offset": 0
}

# Simulation time
t = np.arange(0, 20 + param["dt"], param["dt"])

# Initial values for trajectory
phi_reference = []
for i in range(param["N"] - 1):
    phi = param["alphaA"] * np.sin((param["omega"] * t + i * param["delta"]))
    phi_reference.append(phi)

# Initial values
theta = np.zeros(param["N"])
thetaDot = np.zeros(param["N"])
phi = np.zeros(param["N"] - 1)
phiDot = np.zeros(param["N"] - 1)
p = np.zeros(2)
pDot = np.zeros(2)
qa = phi.copy()
qu = np.array([theta[-1], p[0], p[1]])
qaDot = phiDot.copy()
quDot = np.array([thetaDot[-1], pDot[0], pDot[1]])
x0 = np.concatenate((qa, qu, qaDot, quDot))


# Solution
def dynamic_model(t, x, param):
    # Include the dynamic model calculations here
    # Return the derivatives xDot as a 1D numpy array
    pass


sol = solve_ivp(dynamic_model, [t[0], t[-1]], x0, t_eval=t, args=(param,))

# The results of snake robot motion are in the matrix X
X = sol.y.T
