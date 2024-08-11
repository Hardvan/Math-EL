import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import os

# Parameters for the snake's motion in a pipeline
n_frames = 100
snake_length = 10
pipeline_radius = 5
pipeline_length = 50


def create_snake_frame(t):
    # Create a new frame with a snake's position in the pipeline
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, pipeline_length, 100)
    Z, THETA = np.meshgrid(z, theta)
    X = pipeline_radius * np.sin(THETA)
    Y = pipeline_radius * np.cos(THETA)

    # Define the snake's position
    snake_z = (t * pipeline_length / n_frames) % pipeline_length
    X_snake = X + 0.5 * pipeline_radius * \
        np.sin(2 * np.pi * (Z - snake_z) / snake_length)
    Y_snake = Y + 0.5 * pipeline_radius * \
        np.sin(2 * np.pi * (Z - snake_z) / snake_length)
    Z_snake = Z

    return X_snake, Y_snake, Z_snake


def save_frame_as_image(frame_num, X, Y, Z, filename):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(f"Frame {frame_num}")
    plt.savefig(filename)
    plt.close()


def create_video():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 files
    out = cv2.VideoWriter('snake_pipeline.mp4', fourcc, 10.0, (640, 480))

    for i in range(n_frames):
        X, Y, Z = create_snake_frame(i)
        img_filename = f"frame_{i:03d}.png"
        save_frame_as_image(i, X, Y, Z, img_filename)
        img = cv2.imread(img_filename)
        resized_img = cv2.resize(img, (640, 480))
        out.write(resized_img)
        # Remove the image file after adding it to the video
        os.remove(img_filename)

    out.release()
    print("MP4 video created successfully.")


create_video()
