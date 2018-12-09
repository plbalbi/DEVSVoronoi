import os, re
import numpy as np
import matplotlib.animation as animation

from matplotlib import pyplot as plt


def get_simulated_voronoi_animation(drawlog_np_generated_filename, intial_values, figsize=(15, 10)):

    drawlog_prefix = drawlog_np_generated_filename.split("/")[-1]
    drawlog_files_basepath = "/".join(drawlog_np_generated_filename.split("/")[:-1]) + "/"

    extract_time_regex = re.compile("%s_state_([0-9]+)" % drawlog_prefix)

    found_files = {}

    for file in os.listdir(drawlog_files_basepath):
        if file.find(drawlog_prefix) != -1:
            current_file_name = drawlog_files_basepath + file
            current_file_time = int(extract_time_regex.findall(file)[0])
            converted_file = np.genfromtxt(current_file_name, delimiter=",", filling_values=[np.nan])

            found_files[current_file_time] = converted_file

    composed_matrix = np.zeros([intial_values.values.shape[0], intial_values.values.shape[1], len(found_files)], dtype=np.double)

    fileCount = 0
    for index in sorted(found_files.keys()):
        composed_matrix[..., fileCount] = found_files[index]
        fileCount += 1

    initial_values = composed_matrix[..., 0]
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
    plottedImage = ax.imshow(composed_matrix[..., index], cmap=cells_cmap);
    stepsCount = composed_matrix.shape[2]

    def updateImage(frame_number, *fargs):
        # reuse index 0 to be shown inside drawn animation
        plottedImage.set_array(do_compose_image(composed_matrix, frame_number))
        return plottedImage,

    simulationAnimation = animation.FuncAnimation(fig, updateImage, interval=100, frames=stepsCount, repeat=False)
    return simulationAnimation.to_html5_video()
