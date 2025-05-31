import numpy as np
from PIL import Image
from ray_solver import get_ray_origin

# Result name

save_name = "test"

# Camera position

l_cam = 0
theta_cam = np.pi/2
phi_cam = 0

# Open celestial spheres' images

upper_sphere_path = "assets/orange_sphere.png"
lower_sphere_path = "assets/blue_sphere.png"

upper_sphere_image = Image.open(upper_sphere_path)
lower_sphere_image = Image.open(lower_sphere_path)

upper_sphere_map = upper_sphere_image.load()
lower_sphere_map = lower_sphere_image.load()

# Get pixel size and step

pixels_high, pixels_wide = upper_sphere_image.size

theta_step = np.pi / pixels_high
phi_step = 2*np.pi / pixels_wide

# Get pixel in corresponding celestial sphere for each pixel in the camera sky

camera_sky = Image.new(mode = "RGB", size = (pixels_high, pixels_wide))
camera_sky_map = camera_sky.load()

for n in range(pixels_high):
    theta_cs = n * theta_step
    for m in range(pixels_wide):
        phi_cs = m * phi_step
        
        sol = get_ray_origin(l_cam, theta_cam, phi_cam, theta_cs, phi_cs)
        l, theta, phi, _, _ = sol.y[:,-1]
        sphere_n = np.round(theta/theta_step)
        sphere_m = np.round(phi/phi_step)

        if l > 0:
            camera_sky_map[n, m] = upper_sphere_map[sphere_n, sphere_m]
        elif l < 0:
            camera_sky_map[n, m] = lower_sphere_map[sphere_n, sphere_m]

camera_sky.save(f"results/{save_name}.png")
