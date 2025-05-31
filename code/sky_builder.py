import numpy as np
from PIL import Image
from ray_solver import get_ray_origin

# File parameters

save_name = "fig7b2"
output_width = 100
output_height = 100

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

# Get pixel size and step

theta_step = np.pi / output_height
phi_step = 2*np.pi / output_width

# Get pixel in corresponding celestial sphere for each pixel in the camera sky

camera_sky_map = np.zeros((output_height, output_width, 3), dtype = np.uint8)

for n in range(output_height):
    theta_cs = n * theta_step
    for m in range(output_width):
        if True:
            phi_cs = m * phi_step
            
            print(n, m)

            sol = get_ray_origin(l_cam, theta_cam, phi_cam, theta_cs, phi_cs)
            l, theta, phi, _, _ = sol.y[:,-1]
            theta = np.abs(theta) % np.pi
            phi = np.abs(phi) % (2*np.pi)

            if l > 0:
                sphere_n = int(np.fix(upper_sphere_image.size[1] * theta/np.pi))
                sphere_m = int(np.fix(upper_sphere_image.size[0] * phi/2/np.pi))
                camera_sky_map[n, m] = upper_sphere_map[sphere_n, sphere_m]
            elif l < 0:
                sphere_n = int(np.fix(lower_sphere_image.size[1] * theta/np.pi))
                sphere_m = int(np.fix(lower_sphere_image.size[0] * phi/2/np.pi))
                camera_sky_map[n, m] = lower_sphere_map[sphere_n, sphere_m]
            
camera_sky_image = Image.fromarray(camera_sky_map)
camera_sky_image.save(f"results/{save_name}.jpg")
