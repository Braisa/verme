import numpy as np
from PIL import Image
from scipy.interpolate import RegularGridInterpolator
from ray_solver import get_ray_origin
import pickle

# File parameters

save_name = "fig7b"
output_width = 200
output_height = 200

fidelity = .5

# Camera position

l_cam = 6.75
theta_cam = np.pi/2
phi_cam = 0

# Get pixel size and step

theta_step = np.pi / output_height
phi_step = 2*np.pi / output_width

N = int(fidelity * output_height)
M = int(fidelity * output_width)

# Get mapping to celestial spheres from camera sky

celestial_angles = np.zeros((N, M, 2))
celestial_signs = np.zeros((N,M))

for n in range(N):
    theta_cs = n * theta_step / fidelity
    for m in range(M):
        phi_cs = m * phi_step / fidelity
        
        print(n, m)

        sol = get_ray_origin(l_cam, theta_cam, phi_cam, theta_cs, phi_cs)
        l, theta, phi, _, _ = sol.y[:,-1]
        theta = np.abs(theta) % np.pi
        phi = np.abs(phi) % (2*np.pi)

        celestial_angles[n, m] = (theta, phi)
        celestial_signs[n, m] = np.sign(l)

# Interpolate for missing fidelity

celestial_map_theta = RegularGridInterpolator((np.arange(N), np.arange(M)), celestial_angles[:,:,0])
celestial_map_phi = RegularGridInterpolator((np.arange(N), np.arange(M)), celestial_angles[:,:,1])

celestial_map = (celestial_map_theta, celestial_map_phi, celestial_signs)

# Save map

with open(f"maps/map_{save_name}.pck", "wb") as file_handle:
    pickle.dump(celestial_map, file_handle)
