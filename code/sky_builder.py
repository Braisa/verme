import numpy as np
from PIL import Image, ImageChops, ImageOps
import pickle
from ray_solver import get_ray_origin

theta_range = (np.pi/2-np.pi/15, np.pi/2+np.pi/15)
phi_range = (np.pi-np.pi/15, np.pi+np.pi/15)

def create_image(save_name, map_name, size, center_theta, center_phi):

    # Open celestial spheres' images

    upper_sphere_path = "assets/upper_sphere.jpg"
    lower_sphere_path = "assets/lower_sphere.jpg"

    upper_sphere_image = Image.open(upper_sphere_path)
    lower_sphere_image = Image.open(lower_sphere_path)

    # Center sky

    center_x = upper_sphere_image.size[0] * (1/2 - center_theta/np.pi)
    center_y = upper_sphere_image.size[1] * (1/2 - center_phi/2/np.pi)
    upper_sphere_image = ImageChops.offset(upper_sphere_image, xoffset = int(center_x), yoffset = int(center_y))

    upper_sphere_map = np.asarray(upper_sphere_image)
    lower_sphere_map = np.asarray(lower_sphere_image)

    # Open map

    with open(f"maps/map_{map_name}.pck", "rb") as file_handle:
        celestial_map_theta, celestial_map_phi, celestial_signs = pickle.load(file_handle)

    # Get angles

    thetas = np.linspace(theta_range[0], theta_range[1], size)
    phis = np.linspace(phi_range[0], phi_range[1], size)

    # Get pixel in corresponding celestial sphere for each pixel in the camera sky

    camera_sky_map = np.zeros((size, size, 3), dtype = np.uint8)

    for n, theta_cs in enumerate(thetas):
        for m, phi_cs in enumerate(phis):
            
            print("                                  ", end = "\r")
            print(f"Image progress: {100*(n*size + m+1)/size**2:.1f}%", end = "\r")
            
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
                
    camera_sky_image = Image.fromarray(camera_sky_map)
    camera_sky_image.save(f"results/{save_name}.jpg")

    print()

if __name__ == "__main__":

    save_name = input("Input a name for the save file: ")
    map_name = input("Input the name of the map file that will be used: ")
    image_size = int(input("Input the size of the final image, in pixels: "))

    center_theta = float(input("Input the theta position of the wormhole in the sky, in degrees: "))
    center_phi = float(input("Input the phi position of the wormhole in the sky, in degrees: "))

    create_image(save_name = save_name, map_name = map_name, size = image_size, center_theta = center_theta, center_phi = center_phi)

    print("Image saved!")
