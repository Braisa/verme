import numpy as np
from PIL import Image, ImageChops, ImageOps
import pickle
from ray_solver import get_ray_origin

# Map parameters

map_name = "fig7c"

# File parameters

debug = False

save_name = map_name
output_width = 1000
output_height = 1000

theta_range = (np.pi/2-np.pi/20, np.pi/2+np.pi/20)
phi_range = (np.pi-np.pi/20, np.pi+np.pi/20)
#phi_range = (0, np.pi/20)

# Open celestial spheres' images

upper_sphere_path = "assets/InterstellarWormhole_Fig6b-1750x875.jpg"
lower_sphere_path = "assets/InterstellarWormhole_Fig6a-1750x875.jpg"

upper_sphere_image = Image.open(upper_sphere_path)
lower_sphere_image = Image.open(lower_sphere_path)

upper_sphere_image = ImageChops.offset(upper_sphere_image, xoffset = int((1750/2)-1320), yoffset = int((875/2)-350))

upper_sphere_map = np.asarray(upper_sphere_image)
lower_sphere_map = np.asarray(lower_sphere_image)

# Open map

with open(f"maps/map_{map_name}.pck", "rb") as file_handle:
    celestial_map_theta, celestial_map_phi, celestial_signs = pickle.load(file_handle)

# Get angles

thetas = np.linspace(theta_range[0], theta_range[1], output_height)
phis = np.linspace(phi_range[0], phi_range[1], output_width)

# Get pixel in corresponding celestial sphere for each pixel in the camera sky

camera_sky_map = np.zeros((output_height, output_width, 3), dtype = np.uint8)
if debug:
    debug_map = np.zeros((output_height, output_width), dtype = np.uint8)


for n, theta_cs in enumerate(thetas):
    for m, phi_cs in enumerate(phis):

        print(n, m, end = "\r")
        
        theta = celestial_map_theta((theta_cs, phi_cs)) % np.pi
        phi = celestial_map_phi((theta_cs, phi_cs)) % (2*np.pi)

        if celestial_signs((theta_cs, phi_cs)) > 0:
            sphere_n = int(np.fix(upper_sphere_image.size[1] * theta/np.pi)) % upper_sphere_image.size[1]
            sphere_m = int(np.fix(upper_sphere_image.size[0] * phi/2/np.pi)) % upper_sphere_image.size[0]
            camera_sky_map[n, m] = upper_sphere_map[sphere_n, sphere_m]
        elif celestial_signs((theta_cs, phi_cs)) < 0:
            sphere_n = int(np.fix(lower_sphere_image.size[1] * theta/np.pi)) % lower_sphere_image.size[1]
            sphere_m = int(np.fix(lower_sphere_image.size[0] * phi/2/np.pi)) % lower_sphere_image.size[0]
            camera_sky_map[n, m] = lower_sphere_map[sphere_n, sphere_m]
        
        if debug:
            debug_map[n, m] = celestial_signs((theta_cs, phi_cs))
            
camera_sky_image = Image.fromarray(camera_sky_map)
camera_sky_image.save(f"results/{save_name}.jpg")

if debug:
    debug_image = Image.fromarray(debug_map)
    debug_image.save(f"results/debug_{save_name}.jpg")
