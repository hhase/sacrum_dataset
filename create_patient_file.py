import os
import numpy as np
import matplotlib.pyplot as plt

def load_data(path):
    frame_coords = np.genfromtxt(path, dtype=float, delimiter=',', names=True)
    header = frame_coords.dtype.names
    data = frame_coords.view((float, len(frame_coords.dtype.names)))
    if "tilting" in path:
        data = data[:, :7]
    else:
        data = data[:, :3]
    return header, data

def plot_sweep(data):
    plt.scatter(data[:, 1], data[:, 2])
    plt.show()

def force_into_grid(data, cols=11, col_range=200):
    data = data[:col_range*cols, :]
    data_y_shift = np.nanmin(data[:, 2])
    col_dist = np.abs(np.nanmean(data[:col_range, 2]) - np.nanmean(data[(cols-1)*col_range:cols*col_range, 2]) / cols)
    print(col_dist)
    for i in range(cols):
        data[i*col_range:(i+1) * col_range, 1] = i*col_dist
        data[i*col_range:(i+1)*col_range, 2] -= np.nanmin(data[i*col_range:(i+1)*col_range, 2])
    data[:, 2] += data_y_shift
    plot_sweep(data)
    return data

def def_step_size(steps_x, steps_y, margins, data):
    mins = np.nanmin(data[:,1:3], axis=0)
    maxs = np.nanmax(data[:,1:3], axis=0)
    return (maxs - mins - 2 * margins)/[steps_x-1, steps_y-1]

def find_closest_frame(coords, data):  # Look into KDTrees!
    distance = (data[:, 1] - coords[0]) ** 2 + (data[:, 2] - coords[1]) ** 2
    frame_idxs = np.argsort(distance)
    frame_idx = data[frame_idxs[:5], 0]
    return frame_idx.astype(int)


name = "SubjectXX"
DATASET_PATH = "" # write here absolute path to the dataset folder

patient_path = DATASET_PATH + "/sacrum_dataset/Sacrum_{}/".format(name)
frame_path = patient_path + "sacrum_sweep_frames/"

file_path = DATASET_PATH + "/sacrum_dataset/Patient_files/{}.txt".format(name)

patient_file = open(file_path, "w")

patient_file.write(name + "\n")
patient_file.write(frame_path)

steps_x = 11
steps_y = 15
margins = np.array([0,0])

header, data = load_data(patient_path + "sacrum_sweep_data.csv")
# Sample frequency can differ due to different acquisition configurations
if data.shape[0] > 3000:
    col_size = 350
else:
    col_size = 200

data = force_into_grid(data, cols=11, col_range=col_size)

step_size = def_step_size(steps_x, steps_y, margins, data)

# When creating a new patient file, go through the frames assigned to each bin and manually enter the coordinates on the file with the x-y coordinates
patient_file.write("goal_bins:goal_bin_x,goal_bin_y\n")

grid = np.zeros((steps_x, steps_y)).astype(int)
data_y_shift = np.nanmin(data[:, 2])
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        x_location = i * step_size[0] + margins[0]
        y_location = j * step_size[1] + margins[1]
        location = np.array([x_location, y_location + data_y_shift])
        print(location)
        coords = np.array([i, j])
        frame_idxs = find_closest_frame(location, data)
        grid[i,j] = frame_idxs[0]
        # Write frames to file in the format: x_coord,y_coord:frame_idxs
        patient_file.write("{},{}:{}\n".format(i, j, ",".join(map(str, frame_idxs))))

patient_file.write("\n\n******************************************\n\n")

# Grid visualization - has no impact in the loading the environments, but helps for visualization

row = ""
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        frame = grid[i, j]
        row += "{:4d} ".format(frame)
    patient_file.write(row + "\n")
    print(row)
    row = ""

patient_file.close()
