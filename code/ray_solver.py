import numpy as np
from scipy.integrate import solve_ivp

# Wormhole parameters

rho = 1
a = .5
W = .43
M = W / 1.42953

# Metric radial function

x = lambda l : 2*(np.abs(l) - a)/(np.pi*M)
r = lambda l : rho + np.heaviside(np.abs(l)/a -1, 1) * M * (x(l)*np.arctan(x(l)) - .5*np.log(1+x(l)**2))
dr_dl = lambda l : np.heaviside(np.abs(l)/a -1, 1) * 2/np.pi * np.sign(l) * np.arctan(x(l))

def get_ray_origin(l0, theta0, phi0, theta_cs, phi_cs):

    """

    Computes parting position for a ray received by a camera standing at the point (l0, theta0, phi0) at t = 0 that is looking at the point (theta_cs, phi_cs).

    """

    # Incoming light ray momenta

    p_l_0 = -1 * np.cos(phi_cs) * np.sin(theta_cs)
    p_theta_0 = r(l0) * np.cos(theta_cs)
    p_phi_0 = -1 * r(l0) * np.sin(theta0) * np.sin(phi_cs) * np.sin(theta_cs)

    # Conserved quantities

    b = p_phi_0
    B = np.sqrt(p_theta_0**2 + b**2 * np.sin(theta0)**-2)

    # Ray differential equations
    # coords = (l, theta, phi, p_l, p_theta)
    diff = lambda t, coords : (
        coords[3],
        coords[4] * r(coords[0])**-2,
        b * r(coords[0])**-2 * np.sin(coords[1])**-2,
        B**2 * r(coords[0])**-3 * dr_dl(coords[0]),
        b**2 * r(coords[0])**-2 * np.cos(coords[1]) * np.sin(coords[1])**-3
    )
        
    # Initial coordinates
    
    initial_coords = (l0, theta0, phi0, p_l_0, p_theta_0)

    # Runge-Kutta solving

    return solve_ivp(fun = diff, t_span = (0, -1e3), y0 = initial_coords, method = "RK45")
