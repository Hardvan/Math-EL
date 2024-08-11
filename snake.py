import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import os

# Parameters for the snake's motion in a pipeline
n_frames = 50
snake_length = 10
pipeline_radius = 5
pipeline_length = 50
snake_radius = 1.5  # Smaller radius for the snake


def create_cylindrical_wall():
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, pipeline_length, 100)
    THETA, Z = np.meshgrid(theta, z)
    X = pipeline_radius * np.cos(THETA)
    Y = pipeline_radius * np.sin(THETA)
    return X, Y, Z


def lateral_undulation(t):
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, pipeline_length, 100)
    Z, THETA = np.meshgrid(z, theta)
    X = snake_radius * np.sin(THETA)
    Y = snake_radius * np.cos(THETA)

    snake_z = (t * pipeline_length / n_frames) % pipeline_length
    X_snake = X + 0.5 * pipeline_radius * \
        np.sin(2 * np.pi * (Z - snake_z) / snake_length)
    Y_snake = Y + 0.5 * pipeline_radius * \
        np.sin(2 * np.pi * (Z - snake_z) / snake_length)
    Z_snake = Z

    return X_snake, Y_snake, Z_snake


def concertina(t):
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, pipeline_length, 100)
    Z, THETA = np.meshgrid(z, theta)
    X = snake_radius * np.sin(THETA)
    Y = snake_radius * np.cos(THETA)

    # Concertina motion
    snake_z = (t * pipeline_length / n_frames) % pipeline_length
    amplitude = 2.0
    frequency = 2 * np.pi / snake_length
    X_snake = X + amplitude * np.sin(frequency * (Z - snake_z))
    Y_snake = Y
    Z_snake = Z

    return X_snake, Y_snake, Z_snake


def rectilinear(t):
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, pipeline_length, 100)
    Z, THETA = np.meshgrid(z, theta)
    X = snake_radius * np.sin(THETA)
    Y = snake_radius * np.cos(THETA)

    # Rectilinear motion
    snake_z = (t * pipeline_length / n_frames) % pipeline_length
    X_snake = X
    Y_snake = Y
    Z_snake = Z + snake_z

    return X_snake, Y_snake, Z_snake


def sidewinding(t):
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(0, pipeline_length, 100)
    Z, THETA = np.meshgrid(z, theta)
    X = snake_radius * np.sin(THETA)
    Y = snake_radius * np.cos(THETA)

    # Sidewinding motion
    snake_z = (t * pipeline_length / n_frames) % pipeline_length
    amplitude = 1.5
    frequency = 2 * np.pi / snake_length
    X_snake = X + amplitude * np.sin(frequency * (Z - snake_z))
    Y_snake = Y + amplitude * np.cos(frequency * (Z - snake_z))
    Z_snake = Z

    return X_snake, Y_snake, Z_snake


def save_frame_as_image(frame_num, X_cyl, Y_cyl, Z_cyl, X_snake, Y_snake, Z_snake, filename):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the cylindrical wall
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, color='lightgrey', alpha=0.5)

    # Plot the snake
    ax.plot_surface(X_snake, Y_snake, Z_snake, cmap='viridis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(f"Frame {frame_num}")
    plt.savefig(filename)
    plt.close()


def create_video(motion_type):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 files
    out = cv2.VideoWriter(f'snake_{motion_type}.mp4', fourcc, 10.0, (640, 480))

    print(f"🎥  Creating video for {motion_type}...")
    for i in range(n_frames):
        X_cyl, Y_cyl, Z_cyl = create_cylindrical_wall()
        if motion_type == 'lateral_undulation':
            X_snake, Y_snake, Z_snake = lateral_undulation(i)
        elif motion_type == 'concertina':
            X_snake, Y_snake, Z_snake = concertina(i)
        elif motion_type == 'rectilinear':
            X_snake, Y_snake, Z_snake = rectilinear(i)
        elif motion_type == 'sidewinding':
            X_snake, Y_snake, Z_snake = sidewinding(i)
        else:
            raise ValueError("❌  Invalid motion type")

        img_filename = f"frame_{motion_type}_{i:03d}.png"
        save_frame_as_image(i, X_cyl, Y_cyl, Z_cyl, X_snake,
                            Y_snake, Z_snake, img_filename)

        img = cv2.imread(img_filename)
        resized_img = cv2.resize(img, (640, 480))
        out.write(resized_img)

        # Remove the image file after adding it to the video
        os.remove(img_filename)

        # Print progress message with carriage return
        print(f"🖼️  Frame {i + 1} of {motion_type} done...", end='\r')

    out.release()
    print(f"✅  MP4 video for {motion_type} created successfully.")


# Create videos for different types of motion
create_video('lateral_undulation')
create_video('concertina')
create_video('rectilinear')
create_video('sidewinding')
