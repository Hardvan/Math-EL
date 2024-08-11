import numpy as np


def dynamic_model(t, x, param):
    # ==============================================================================================================
    # Basic parameters
    # ==============================================================================================================
    ut = param['ut']
    un = param['un']
    ct = param['ct']
    cn = param['cn']
    N = param['N']
    kp = param['kp']
    kd = param['kd']
    l = param['l']
    diameter = param['diameter']
    diameterI = param['diameterInfluence']
    m = param['m']
    g = param['g']
    offset = param['offset']
    alphaA = param['alphaA']
    omega = param['omega']
    delta = param['delta']
    viscous = param['friction']
    contact = param['contact']
    utPipe = param['utPipe']
    ctPipe = param['ctPipe']
    Erub = param['Erub']
    vrub = param['vrub']
    umax = param['umax']
    qmax = param['qmax']
    minLinkVel = param['minLinkVel']
    d = diameter - 2*l
    I = (m*(2*l)**2)/3

    # ==============================================================================================================
    # Auxiliary matrices
    # ==============================================================================================================
    A = np.eye(N-1, N, k=0) + np.eye(N-1, N, k=1)
    D = np.eye(N-1, N, k=0) - np.eye(N-1, N, k=1)
    Va = A.T @ np.linalg.inv(D @ D.T) @ A
    Ka = A.T @ np.linalg.inv(D @ D.T) @ D

    J = np.eye(N, N+1, k=0) - np.eye(N, N+1, k=1)
    K = np.eye(N, N+1)

    J2 = np.eye(N, N-1, k=0) + np.eye(N, N-1, k=1)
    Jf = np.eye(N, N-1, k=0) - np.eye(N, N-1, k=1)

    HH = np.triu(np.ones((N, N)))
    J3 = -J2
    J1 = -Jf
    NN = J @ np.linalg.pinv(K)
    T = np.abs(NN)

    e = np.ones(N+1)
    e[-1] = 0
    k = np.ones(N)
    j = np.zeros(N)
    j[-1] = -1

    # ==============================================================================================================
    # Kinematic model
    # ==============================================================================================================
    phi = x[:N]
    p = x[N:N+2]
    phiDot = x[N+2:2*N+2]
    pDot = x[2*N+2:2*N+4]

    theta = HH @ phi
    thetaDot = HH @ phiDot

    s_vect = np.sin(theta)
    c_vect = np.cos(theta)
    sgn = np.sign(theta)
    dThetaqSqared = thetaDot**2

    Cm = np.diag(np.cos(theta))
    Sm = np.diag(np.sin(theta))

    A = J @ J.T
    B = (1/N) * j[:, np.newaxis]
    C = (1/N) * j[np.newaxis, :]
    D = (1/N)

    DD = np.linalg.inv(D - C @ np.linalg.inv(A) @ B)
    AA = np.linalg.inv(A) + np.linalg.inv(A) @ B @ DD @ C @ np.linalg.inv(A)
    BB = -np.linalg.inv(A) @ B @ DD
    CC = -DD @ C @ np.linalg.inv(A)

    Hinv = np.vstack(
        [J.T, (1/N)*e]).T @ np.vstack([np.hstack([AA, BB]), np.hstack([CC, DD])])

    X = Hinv @ np.hstack([2*l*c_vect, p[0] - (l/N)*k @ c_vect])
    Y = Hinv @ np.hstack([2*l*s_vect, p[1] - (l/N)*k @ s_vect])

    dX = (-J.T @ AA @ 2*l*Sm @ thetaDot - (1/N)*e @ CC @ 2*l*Sm @ thetaDot +
          J.T @ BB @ pDot[0] + J.T @ BB @ (l/N) * k @ Sm @ thetaDot +
          (1/N)*e @ DD @ pDot[0] + (1/N)*e @ DD @ (l/N) * k @ Sm @ thetaDot)

    dY = (J.T @ AA @ 2*l*Cm @ thetaDot + (1/N)*e @ CC @ 2*l*Cm @ thetaDot +
          J.T @ BB @ pDot[1] - J.T @ BB @ (l/N) * k @ Cm @ thetaDot +
          (1/N)*e @ DD @ pDot[1] - (1/N)*e @ DD @ (l/N) * k @ Cm @ thetaDot)

    Xc = K @ X + l*c_vect
    Yc = K @ Y + l*s_vect

    dXc = K @ dX - l*Sm @ thetaDot
    dYc = K @ dY + l*Cm @ thetaDot

    # ==============================================================================================================
    # Dynamics model
    # ==============================================================================================================
    M = np.diag([m for _ in range(N)])
    C = np.zeros((N, N))
    G = np.zeros(N)
    f = np.zeros(N)
    for i in range(N):
        G[i] = -m * g * l * np.sin(theta[i])
        for j in range(N):
            C[i, j] = I if i == j else 0

    tau = np.zeros(N)
    for i in range(N-1):
        tau[i] = kp * (param['alphaA'] * np.sin(param['omega']
                       * t + i * param['delta']) - phi[i]) - kd * phiDot[i]

    d2theta = np.linalg.inv(M) @ (tau - C @ thetaDot - G - f)

    # Update the state derivatives
    phi_ddot = d2theta[:-1]
    theta_ddot = np.hstack([d2theta[-1], phi_ddot])
    xDot = np.hstack([phiDot, pDot, theta_ddot, dXc, dYc])

    return xDot
