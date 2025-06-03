import numpy as np
from map_builder import create_map
from sky_builder import create_image

save_name = input("Input a name for the save file: ")
image_size = int(input("Input the size of the final image, in pixels: "))
sample_amount = int(input("Input the amount of samples for the map building: "))

a = float(input("Input the length (a) of the wormhole, in terms of its radius: "))
W = float(input("Input the lensing width (W) of the wormhole, in terms of its radius: "))

center_theta = float(input("Input the theta position of the wormhole in the sky, in degrees: "))
center_phi = float(input("Input the phi position of the wormhole in the sky, in degrees: "))

l_cam = float(input("Input the position (l) of the camera, in terms of the wormhole's radius: "))
theta_cam = float(input("Input the theta position of the camera, in degrees: ")) * np.pi/180
phi_cam = float(input("Input the phi position of the camera, in degrees: ")) * np.pi/180

create_map(save_name = save_name, samples = sample_amount, a = a, W= W, l_cam = l_cam, theta_cam = theta_cam, phi_cam = phi_cam)

create_image(save_name = save_name, map_name = save_name, size = image_size, center_theta = center_theta, center_phi = center_phi)

print("Image saved!")
