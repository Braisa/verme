import numpy as np
from PIL import Image
from scipy.interpolate import RegularGridInterpolator
from ray_solver import get_ray_origin
import pickle

# Map parameters

theta_range = (np.pi/2-np.pi/15, np.pi/2+np.pi/15)
phi_range = (np.pi-np.pi/15, np.pi+np.pi/15)

def create_map(save_name, samples, a, W, l_cam, theta_cam, phi_cam):

    # Get angles

    thetas = np.linspace(theta_range[0], theta_range[1], samples)
    phis = np.linspace(phi_range[0], phi_range[1], samples)

    # Get mapping to celestial spheres from camera sky

    celestial_angles = np.zeros((samples, samples, 2))
    celestial_signs = np.zeros((samples, samples))

    for n, theta_cs in enumerate(thetas):
        for m, phi_cs in enumerate(phis):
            
            print("                                  ", end = "\r")
            print(f"Map progress: {100*(n*samples + m+1)/samples**2:.1f}%", end = "\r")

            sol = get_ray_origin(a, W, l_cam, theta_cam, phi_cam, theta_cs, phi_cs)
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

    print()

if __name__ == "__main__":

    save_name = input("Input a name for the save file: ")
    sample_amount = int(input("Input the amount of samples for the map building: "))

    a = float(input("Input the length (a) of the wormhole, in terms of its radius: "))
    W = float(input("Input the lensing width (W) of the wormhole, in terms of its radius: "))

    l_cam = float(input("Input the position (l) of the camera, in terms of the wormhole's radius: "))
    theta_cam = float(input("Input the theta position of the camera, in degrees: ")) * np.pi/180
    phi_cam = float(input("Input the phi position of the camera, in degrees: ")) * np.pi/180

    create_map(save_name = save_name, samples = sample_amount, a = a, W = W, l_cam = l_cam, theta_cam = theta_cam, phi_cam = phi_cam)

    print("Map saved!")
