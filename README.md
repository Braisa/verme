# verme

Interstellar wormhole visualization tool implemented in Python. Based on a paper by Oliver James *et al.* available at https://arxiv.org/abs/1502.03809.

## Demo usage

To create a simple image without diving into the code, you can use the `simple_camera.py` file in the *code* folder. Upon execution, it will ask you to input the multiple parameters required for the image creation process. The resulting image will be stored in the *results* folder under the save name provided, in `.jpg` format.

If you want to change the sky images on the upper and lower celestial spheres, put the new images in the *assets* folder under the names `upper_sphere` and `lower_sphere`, both in `.jpg` format.

For a faster computing time, you can lower image size and map sampling, at the cost of image quality and fidelity, respectively.

As an example, the following image was produced using the parameters

- Image size: 500
- Sample amount: 200
- Wormhole length (a): 0.005
- Wormhole lensing width (W): 0.05
- Wormhole theta position: 72 degrees
- Wormhole phi position: 271.5 degrees
- Camera position (l): 6.255
- Camera theta position: 90 degrees
- Camera phi position: 0 degrees

And by putting the images `InterstellarWormhole-Fig6a-1750x875.jpg` onto the lower celestial sphere and `InterstellarWormhole-Fig6b-1750x875.jpg` onto the upper celestial sphere. Both are available in the *assets* folder and have been taken from https://www.dneg.com/news/visualizing-interstellars-wormhole.

![Sample wormhole image](/results/demo.jpg)
