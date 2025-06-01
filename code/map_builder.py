import numpy as np
from PIL import Image
from scipy.interpolate import RegularGridInterpolator
from ray_solver import get_ray_origin
import pickle

# Map parameters

save_name = "fig7b"
theta_samples = 100
phi_samples = 100

theta_range = (0, np.pi)
phi_range = (0, 2*np.pi)

# Camera position

l_cam = 6.75 * 50
theta_cam = np.pi/2
phi_cam = 0

# Get meshgrid

thetas = np.linspace(theta_range[0], theta_range[1], theta_samples)
phis = np.linspace(phi_range[0], phi_range[1], phi_samples)

# Get mapping to celestial spheres from camera sky

celestial_angles = np.zeros((theta_samples, phi_samples, 2))
celestial_signs = np.zeros((theta_samples,phi_samples))

for n, theta_cs in enumerate(thetas):
    for m, phi_cs in enumerate(phis):
        print(n, m, end = "\r")

        l, theta, phi, _, _ = get_ray_origin(l_cam, theta_cam, phi_cam, theta_cs, phi_cs)

        celestial_angles[n, m] = (theta, phi)
        celestial_signs[n, m] = np.sign(l)

# Interpolate for missing fidelity

celestial_map_theta = RegularGridInterpolator((thetas, phis), celestial_angles[:,:,0])
celestial_map_phi = RegularGridInterpolator((thetas, phis), celestial_angles[:,:,1])
celestial_map_sign = RegularGridInterpolator((thetas, phis), celestial_signs)

celestial_map = (celestial_map_theta, celestial_map_phi, celestial_map_sign, theta_range, phi_range)

# Save map

with open(f"maps/map_{save_name}.pck", "wb") as file_handle:
    pickle.dump(celestial_map, file_handle)
