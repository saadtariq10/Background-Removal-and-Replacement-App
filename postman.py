import os
from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

# Directory to store background images
BACKGROUND_FOLDER = "backgrounds"

@app.route('/')
def index():
    return "Welcome to the Flask API! Use /upload or /backgrounds."

@app.route('/upload', methods=['POST'])
def upload_and_process():
    try:
        # Check if the input image is present in the request
        if 'input_image' not in request.files:
            return jsonify({"error": "No input image provided"}), 400

        # Load the input image
        input_image_file = request.files['input_image']
        input_image = Image.open(input_image_file)

        # Process the image to remove the background
        output_image = remove(input_image)

        # Check if a background image is provided
        if 'background_image' not in request.files:
            return jsonify({"error": "No background image provided"}), 400

        # Load the background image
        background_image_file = request.files['background_image']
        background_image = Image.open(background_image_file)

        # Resize background to match the processed image size
        background_image = background_image.resize(output_image.size)

        # Combine the processed image and the background
        final_image = Image.new("RGBA", background_image.size)
        final_image.paste(background_image, (0, 0))
        final_image.paste(output_image, (0, 0), mask=output_image)
        final_image_rgb = final_image.convert("RGB")

        # Save the final image to a byte stream
        img_byte_arr = io.BytesIO()
        final_image_rgb.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Send the final image as a downloadable file
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='final_image.png'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# List available backgrounds in the folder
@app.route('/backgrounds', methods=['GET'])
def list_backgrounds():
    try:
        background_files = [
            f for f in os.listdir(BACKGROUND_FOLDER) if f.endswith(('jpg', 'jpeg', 'png'))
        ]
        return jsonify({"backgrounds": background_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Ensure background folder exists
    os.makedirs(BACKGROUND_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
