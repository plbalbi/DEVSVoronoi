import numpy as np
import matplotlib.animation as animation

from matplotlib import pyplot as plt

def get_simulated_voronoi_animation(drawlog_np_generated_filename, intial_values, figsize=(15,10)):
    loadedMatrix = np.load(drawlog_np_generated_filename)

    composedMatrix = np.zeros([intial_values.values.shape[0], intial_values.values.shape[1], len(loadedMatrix.files)],
                              dtype=np.double)

    for index, npFileName in enumerate(loadedMatrix.files):
        composedMatrix[..., index] = loadedMatrix[npFileName].reshape(intial_values.values.shape)

    initial_values = composedMatrix[..., 0]
    cells_cmap = plt.cm.Pastel1

    # Set nan's to be displayed as red dots
    cells_cmap.set_bad((1, 0, 0, 1))

    def do_compose_image(images, index):
        composed_image = images[..., index]
        composed_image[initial_values != 0] = np.nan
        return composed_image

    index = 0
    fig, ax = plt.subplots(figsize=figsize)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plottedImage = ax.imshow(composedMatrix[..., index], cmap=cells_cmap);
    stepsCount = composedMatrix.shape[2]

    def updateImage(frame_number, *fargs):
        # reuse index 0 to be shown inside drawn animation
        plottedImage.set_array(do_compose_image(composedMatrix, frame_number))
        return plottedImage,

    simulationAnimation = animation.FuncAnimation(fig, updateImage, interval=100, frames=stepsCount, repeat=False)
    return simulationAnimation.to_html5_video()