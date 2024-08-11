import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import os


class SnakePipelineSimulator:
    def __init__(self, n_frames=50, snake_length=10, pipeline_radius=5, pipeline_length=50, snake_radius=1.5):
        self.n_frames = n_frames
        self.snake_length = snake_length
        self.pipeline_radius = pipeline_radius
        self.pipeline_length = pipeline_length
        self.snake_radius = snake_radius

    def create_cylindrical_wall(self):
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.linspace(0, self.pipeline_length, 100)
        THETA, Z = np.meshgrid(theta, z)
        X = self.pipeline_radius * np.cos(THETA)
        Y = self.pipeline_radius * np.sin(THETA)
        return X, Y, Z

    def lateral_undulation(self, t):
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.linspace(0, self.pipeline_length, 100)
        Z, THETA = np.meshgrid(z, theta)
        X = self.snake_radius * np.sin(THETA)
        Y = self.snake_radius * np.cos(THETA)

        snake_z = (t * self.pipeline_length /
                   self.n_frames) % self.pipeline_length
        X_snake = X + 0.5 * self.pipeline_radius * \
            np.sin(2 * np.pi * (Z - snake_z) / self.snake_length)
        Y_snake = Y + 0.5 * self.pipeline_radius * \
            np.sin(2 * np.pi * (Z - snake_z) / self.snake_length)
        Z_snake = Z

        return X_snake, Y_snake, Z_snake

    def concertina(self, t):
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.linspace(0, self.pipeline_length, 100)
        Z, THETA = np.meshgrid(z, theta)
        X = self.snake_radius * np.sin(THETA)
        Y = self.snake_radius * np.cos(THETA)

        snake_z = (t * self.pipeline_length /
                   self.n_frames) % self.pipeline_length
        amplitude = 2.0
        frequency = 2 * np.pi / self.snake_length
        X_snake = X + amplitude * np.sin(frequency * (Z - snake_z))
        Y_snake = Y
        Z_snake = Z

        return X_snake, Y_snake, Z_snake

    def rectilinear(self, t):
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.linspace(0, self.pipeline_length, 100)
        Z, THETA = np.meshgrid(z, theta)
        X = self.snake_radius * np.sin(THETA)
        Y = self.snake_radius * np.cos(THETA)

        snake_z = (t * self.pipeline_length /
                   self.n_frames) % self.pipeline_length
        amplitude = 2.0  # Amplitude of the compression/expansion
        frequency = 2 * np.pi / self.snake_length

        # Sinusoidal modulation for alternating compression and expansion
        Z_snake = Z + amplitude * np.sin(frequency * (Z - snake_z))

        return X, Y, Z_snake

    def sidewinding(self, t):
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.linspace(0, self.pipeline_length, 100)
        Z, THETA = np.meshgrid(z, theta)
        X = self.snake_radius * np.sin(THETA)
        Y = self.snake_radius * np.cos(THETA)

        snake_z = (t * self.pipeline_length /
                   self.n_frames) % self.pipeline_length
        amplitude = 1.5
        frequency = 2 * np.pi / self.snake_length
        X_snake = X + amplitude * np.sin(frequency * (Z - snake_z))
        Y_snake = Y + amplitude * np.cos(frequency * (Z - snake_z))
        Z_snake = Z

        return X_snake, Y_snake, Z_snake

    def save_frame_as_image(self, frame_num, X_cyl, Y_cyl, Z_cyl, X_snake, Y_snake, Z_snake, filename):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(X_cyl, Y_cyl, Z_cyl, color='lightgrey', alpha=0.5)
        ax.plot_surface(X_snake, Y_snake, Z_snake, cmap='viridis')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title(f"Frame {frame_num}")
        plt.savefig(filename)
        plt.close()

    def create_video(self, motion_type, file_path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = f'{file_path}/{motion_type}.mp4'
        out = cv2.VideoWriter(output_path, fourcc, 10.0, (640, 480))

        print(f"🎥  Creating video for {motion_type}...")
        for i in range(self.n_frames):
            X_cyl, Y_cyl, Z_cyl = self.create_cylindrical_wall()
            if motion_type == 'lateral_undulation':
                X_snake, Y_snake, Z_snake = self.lateral_undulation(i)
            elif motion_type == 'concertina':
                X_snake, Y_snake, Z_snake = self.concertina(i)
            elif motion_type == 'rectilinear':
                X_snake, Y_snake, Z_snake = self.rectilinear(i)
            elif motion_type == 'sidewinding':
                X_snake, Y_snake, Z_snake = self.sidewinding(i)
            else:
                raise ValueError("❌  Invalid motion type")

            img_filename = f"frame_{motion_type}_{i:03d}.png"
            self.save_frame_as_image(
                i, X_cyl, Y_cyl, Z_cyl, X_snake, Y_snake, Z_snake, img_filename)

            img = cv2.imread(img_filename)
            resized_img = cv2.resize(img, (640, 480))
            out.write(resized_img)

            os.remove(img_filename)

            print(f"🖼️  Frame {i + 1} of {motion_type} done...", end='\r')

        out.release()
        print(f"✅  MP4 video for {motion_type} created successfully.")
        return output_path


def create_video_request_handler(n_frames, snake_length, pipeline_radius, pipeline_length, snake_radius, file_path):
    simulator = SnakePipelineSimulator(
        n_frames, snake_length, pipeline_radius, pipeline_length, snake_radius)
    motion_types = ['lateral_undulation',
                    'concertina', 'rectilinear', 'sidewinding']

    output_paths = {}
    for motion_type in motion_types:
        output_path = simulator.create_video(motion_type, file_path)
        output_paths[motion_type] = output_path

    return output_paths


# Example usage:
if __name__ == '__main__':
    output_paths = create_video_request_handler(50, 10, 5, 50, 1.5, '.')
    print(output_paths)
