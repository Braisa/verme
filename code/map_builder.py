import numpy as np
from PIL import Image
from scipy.interpolate import RegularGridInterpolator
from ray_solver import get_ray_origin
import pickle

# Map parameters

save_name = "trip_stills_8"
theta_samples = 150
phi_samples = 150

#theta_range = (np.pi/2-np.pi/20, np.pi/2+np.pi/20)
#phi_range = (np.pi-np.pi/20, np.pi+np.pi/20)

theta_range = (np.pi/2-np.pi/20, np.pi/2+np.pi/20)
phi_range = (np.pi-np.pi/20, np.pi+np.pi/20)

# Camera position

l_cam = -7
theta_cam = np.pi/2
phi_cam = 0

# Get angles

thetas = np.linspace(theta_range[0], theta_range[1], theta_samples)
phis = np.linspace(phi_range[0], phi_range[1], phi_samples)

# Get mapping to celestial spheres from camera sky

celestial_angles = np.zeros((theta_samples, phi_samples, 2))
celestial_signs = np.zeros((theta_samples, phi_samples))

for n, theta_cs in enumerate(thetas):
    for m, phi_cs in enumerate(phis):
        print(n, m, end = "\r")

        sol = get_ray_origin(l_cam, theta_cam, phi_cam, theta_cs, phi_cs)
        l, theta, phi, _, _ = sol.y[:,-1]

        # Account for frame change
        if l * l_cam < 0:
            phi = 2*np.pi - phi

        celestial_angles[n, m] = (theta, phi)
        celestial_signs[n, m] = np.sign(l)

# Interpolate for missing fidelity

celestial_map_theta = RegularGridInterpolator((thetas, phis), celestial_angles[:,:,0])
celestial_map_phi = RegularGridInterpolator((thetas, phis), celestial_angles[:,:,1])
celestial_map_sign = RegularGridInterpolator((thetas, phis), celestial_signs)

celestial_map = (celestial_map_theta, celestial_map_phi, celestial_map_sign)

# Save map

with open(f"maps/map_{save_name}.pck", "wb") as file_handle:
    pickle.dump(celestial_map, file_handle)
