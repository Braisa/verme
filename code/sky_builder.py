import numpy as np
from PIL import Image
import pickle
from ray_solver import get_ray_origin

# Map parameters

map_name = "fig7b"

# File parameters

save_name = "wow"
output_width = 300
output_height = 300

# Camera position

l_cam = 6.75
theta_cam = np.pi/2
phi_cam = 0

# Open celestial spheres' images

upper_sphere_path = "assets/InterstellarWormhole_Fig6b-1750x875.jpg"
lower_sphere_path = "assets/InterstellarWormhole_Fig6a-1750x875.jpg"

upper_sphere_image = Image.open(upper_sphere_path)
lower_sphere_image = Image.open(lower_sphere_path)

upper_sphere_map = np.asarray(upper_sphere_image)
lower_sphere_map = np.asarray(lower_sphere_image)

# Get angles

thetas = np.linspace(0, np.pi, output_height)
phis = np.linspace(0, 2*np.pi, output_width)

# Open map

with open(f"maps/map_{map_name}.pck", "rb") as file_handle:
    celestial_map_theta, celestial_map_phi, celestial_signs = pickle.load(file_handle)

# Get pixel in corresponding celestial sphere for each pixel in the camera sky

camera_sky_map = np.zeros((output_height, output_width, 3), dtype = np.uint8)

for n, theta_cs in enumerate(thetas):
    for m, phi_cs in enumerate(phis):
        
        theta = celestial_map_theta((theta_cs, phi_cs))
        phi = celestial_map_phi((theta_cs, phi_cs))

        if celestial_signs((theta_cs, phi_cs)) > 0:
            sphere_n = int(np.fix(upper_sphere_image.size[1] * theta/np.pi))
            sphere_m = int(np.fix(upper_sphere_image.size[0] * phi/2/np.pi))
            camera_sky_map[n, m] = upper_sphere_map[sphere_n, sphere_m]
        elif celestial_signs((theta_cs, phi_cs)) < 0:
            sphere_n = int(np.fix(lower_sphere_image.size[1] * theta/np.pi))
            sphere_m = int(np.fix(lower_sphere_image.size[0] * phi/2/np.pi))
            camera_sky_map[n, m] = lower_sphere_map[sphere_n, sphere_m]
            
camera_sky_image = Image.fromarray(camera_sky_map)
camera_sky_image.save(f"results/{save_name}.jpg")
