import os
from rembg import remove
from PIL import Image

# Get the current script directory
project_directory = os.path.dirname(os.path.abspath(__file__))

# Store path of the image in the variable input_path
input_path = os.path.join(project_directory, 'car.jpg')

# Store path of the output image in the variable output_path
output_path = os.path.join(project_directory, 'gfgoutput.png')

# Processing the image
input_image = Image.open(input_path)

# Removing the background from the given Image
output_image = remove(input_image)

# Saving the image in the given path
output_image.save(output_path)
