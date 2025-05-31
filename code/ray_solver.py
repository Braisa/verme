import numpy as np
from scipy.integrate import solve_ivp
from numba import jit

# Wormhole parameters

rho = 1
a = .5
W = .05
M = W / 1.42953

# Heaviside function

@jit
def heaviside(l):
    if l < 0.0:
        return 0.0
    else:
        return 1.0

# Metric radial function
@jit
def x(l):
    X = 2*(np.abs(l) - a)/(np.pi*M)
    return X
@jit
def r(l):
    R = rho + heaviside(np.abs(l) - a) * M * (x(l)*np.arctan(x(l)) - .5*np.log(1+x(l)**2))
    return R
@jit
def dr_dl(l):
    DR_DL = heaviside(np.abs(l) - a) * 2/np.pi * np.sign(l) * np.arctan(x(l))
    return DR_DL

def get_ray_origin(l0, theta0, phi0, theta_cs, phi_cs):

    """

    Computes parting position for a ray received by a camera standing at the point (l0, theta0, phi0) at t = 0 that is looking at the point (theta_cs, phi_cs).

    """

    # Incoming light ray momenta

    p_l = lambda l, theta : -1 * np.cos(phi_cs) * np.sin(theta_cs)
    p_theta = lambda l, theta : r(l) * np.cos(theta_cs)
    p_phi = lambda l, theta : r(l) * np.sin(theta) * (-1 * np.sin(phi_cs) * np.sin(theta_cs))

    # Conserved quantities

    b = p_phi(l0, theta0)
    B = p_theta(l0, theta0)**2 + b**2 * np.sin(theta0)**-2

    # Ray differential equations
    @jit
    def diff(t, coords):
        l, theta, phi, p_l, p_theta = coords
        dl = p_l
        dtheta = p_theta * r(l)**-2
        dphi = b * r(l)**-2 * np.sin(theta)**-2
        dp_l = B**2 * r(l)**-3 * dr_dl(l)
        dp_theta = B**2 * r(l)**-2 * np.cos(theta) * np.sin(theta)**-3
        return (dl, dtheta, dphi, dp_l, dp_theta)
        
    # Initial coordinates
    
    initial_coords = (l0, theta0, phi0, p_l(l0, theta0), p_theta(l0, theta0))

    # Runge-Kutta solving

    return solve_ivp(fun = diff, t_span = (0, -1e5), y0 = initial_coords, method = "RK45")
