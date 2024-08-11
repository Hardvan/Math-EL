from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from snake import create_video_request_handler

app = Flask(__name__)
UPLOAD_FOLDER = 'static/videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n_frames = int(request.form['n_frames'])
        snake_length = float(request.form['snake_length'])
        pipeline_radius = float(request.form['pipeline_radius'])
        pipeline_length = float(request.form['pipeline_length'])
        snake_radius = float(request.form['snake_radius'])

        # Generate videos
        video_paths = create_video_request_handler(
            n_frames, snake_length, pipeline_radius, pipeline_length, snake_radius, UPLOAD_FOLDER
        )

        # Prepare video file paths for rendering
        videos = {motion: url_for('static', filename=os.path.basename(
            path)) for motion, path in video_paths.items()}

        return render_template('videos.html', videos=videos)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
