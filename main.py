from flask import Flask, render_template, request
import numpy as np
from PIL import Image

app = Flask(__name__)


def extract_colour(colours, num, counts):
    colours_present = []
    for _ in range(num):
        try:
            dominant_color = colours[np.argmax(counts)]

            dcr = dominant_color[0]
            dcg = dominant_color[1]
            dcb = dominant_color[2]
            dc_tuple = (dcr, dcg, dcb)
            colours_present.append(dc_tuple)

            # Create a mask that filters out the color to remove
            mask = np.all(colours != dc_tuple, axis=1)
            colours = colours[mask]
        except IndexError:
            break

    return colours_present


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    uploaded_image = request.files['imageInput']
    if uploaded_image:
        img = Image.open(uploaded_image)
        img_array = np.array(img)

        h, w, _ = img_array.shape
        img_array_2d = img_array.reshape(h * w, -1)
        # Find the most frequent color
        unique_colors, counts = np.unique(img_array_2d, axis=0, return_counts=True)
        colours_present = extract_colour(unique_colors, 10, counts)

        return render_template('image.html', colours=colours_present)
    else:
        return render_template('index.html', no_image=True)


if __name__ == '__main__':
    app.run()
