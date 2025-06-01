import numpy as np
from PIL import Image
import pickle
from ray_solver import get_ray_origin

# Map parameters

map_name = "fig7b"

# File parameters

debug = True

save_name = "fig7b"
output_width = 300
output_height = 300

# Open celestial spheres' images

upper_sphere_path = "assets/Gargantua.jpg"
lower_sphere_path = "assets/Saturn.jpg"

upper_sphere_image = Image.open(upper_sphere_path)
lower_sphere_image = Image.open(lower_sphere_path)

upper_sphere_map = np.asarray(upper_sphere_image)
lower_sphere_map = np.asarray(lower_sphere_image)

# Open map

with open(f"maps/map_{map_name}.pck", "rb") as file_handle:
    celestial_map_theta, celestial_map_phi, celestial_signs, theta_range, phi_range = pickle.load(file_handle)

# Get angles

thetas = np.linspace(theta_range[0], theta_range[1], output_height)
phis = np.linspace(phi_range[0], phi_range[1], output_width)

# Get pixel in corresponding celestial sphere for each pixel in the camera sky

camera_sky_map = np.zeros((output_height, output_width, 3), dtype = np.uint8)
if debug:
    debug_map = np.zeros((output_height, output_width, 3), dtype = np.uint8)
    upper_debug_map, lower_debug_map = upper_sphere_map.copy(), lower_sphere_map.copy()


for n, theta_cs in enumerate(thetas):
    for m, phi_cs in enumerate(phis):
        
        print(n, m, end = "\r")
        
        theta = celestial_map_theta((theta_cs, phi_cs))
        phi = celestial_map_phi((theta_cs, phi_cs))
        sign = celestial_signs((theta_cs, phi_cs))

        if sign > 0:
            sphere_n = int(np.fix(upper_sphere_image.size[1] * theta/np.pi)) % upper_sphere_image.size[1]
            sphere_m = int(np.fix(upper_sphere_image.size[0] * phi/2/np.pi)) % upper_sphere_image.size[0]
            camera_sky_map[n, m] = upper_sphere_map[sphere_n, sphere_m]
            if debug:
                c1, c2 = sphere_n/upper_sphere_image.size[1], sphere_m/upper_sphere_image.size[0]
                upper_debug_map[sphere_n, sphere_m] = [255 * c1, 0, 255 * c2]
                debug_map[n, m] = [255 * c1, 0, 255 * c2]
        elif sign < 0:
            sphere_n = int(np.fix(lower_sphere_image.size[1] * theta/np.pi)) % lower_sphere_image.size[1]
            sphere_m = int(np.fix(lower_sphere_image.size[0] * phi/2/np.pi)) % lower_sphere_image.size[0]
            camera_sky_map[n, m] = lower_sphere_map[sphere_n, sphere_m]
            if debug:
                c1, c2 = sphere_n/lower_sphere_image.size[1], sphere_m/lower_sphere_image.size[0]
                lower_debug_map[sphere_n, sphere_m] = [255 * c1, 255 * c2, 0]
                debug_map[n, m] = [255 * c1, 255 * c2, 0]

Image.fromarray(camera_sky_map).save(f"results/{save_name}.jpg")

if debug:
    Image.fromarray(debug_map).save(f"results/debug_{save_name}.jpg")
    Image.fromarray(upper_debug_map).save(f"results/debug_upper_{save_name}.jpg")
    Image.fromarray(lower_debug_map).save(f"results/debug_lower_{save_name}.jpg")
