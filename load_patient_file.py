import numpy as np
from PIL import Image


num_states = 165
num_cols = 15
num_rows = 11
frames_per_state = 5
resize_x = 272
resize_y = 258


def load_frame(frame_path, idx):
    frame = Image.open(frame_path + "sacrum_translation{:04d}.png".format(idx))
    frame = np.array(frame)
    return frame


def process_frame(frame):
    frame = resize(frame, (resize_x, resize_y))
    frame = (frame - np.min(frame)) / np.ptp(frame)
    return frame


def load_patient(file_path, patient_name):
    with open(file_path + 'Patient_files/{}'.format(patient_name)) as file:
       name = file.readline().strip()

       _ = file.readline()
       frame_path = file_path + "Sacrum_{}/sacrum_sweep_frames/".format(name)
       goal_coords = file.readline().strip().replace(";", ":").split(":")[1:]

       goals = []
       for i in range(len(goal_coords)):
           row, col = map(int, goal_coords[i].split(","))
           goals.append(row * num_cols + col)

        frame_array = np.zeros((num_states, frames_per_state, resize_x, resize_y))
        for _ in range(num_states):
            coords, frames = file.readline().strip().split(":")
            row, col = map(int, coords.split(","))
            frames = list(map(int, frames.split(",")))
            for i in range(self.frames_per_state):
                frame = load_frame(frame_path, frames[i])
                frame = process_frame(frame)
                frame_array[row * num_cols + col, i, :, :] = frame
    
    return goals, frame_array


name = "SubjectXX"

DATASET_PATH = "" 	# define absolute path to dataset

goals, frame_array = load_patient(DATASET_PATH, name)
