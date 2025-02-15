import os
import ctypes
from rembg import remove
from PIL import Image

# Function to change the wallpaper
def change_wallpaper(image_path):
    # Constants for setting the wallpaper
    SPI_SETDESKWALLPAPER = 20  # Action to change wallpaper
    SPIF_UPDATEINIFILE = 0x01  # Update user profile
    SPIF_SENDWININICHANGE = 0x02  # Notify change to system

    try:
        # Call Windows API to change wallpaper
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path,
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )
        return True
    except Exception as e:
        # Print error message if wallpaper change fails
        print(f"Error changing wallpaper: {e}")
        return False

# Main function
if __name__ == "__main__":
    # Get the current script directory
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Paths for input, output, and background images
    input_path = os.path.join(project_directory, 'car.jpg')  # Replace with your input image name
    output_path = os.path.join(project_directory, 'final_output.png')
    background_path = os.path.join(project_directory, 'backgrounds', 'road.jpg')

    try:
        # 1. Load and process the input image
        input_image = Image.open(input_path)
        processed_image = remove(input_image)

        # 2. Save the processed image temporarily
        processed_output_path = os.path.join(project_directory, 'gfgoutput.png')
        processed_image.save(processed_output_path)
        print(f"Background removed and saved to: {processed_output_path}")

        # 3. Load the background image
        background_image = Image.open(background_path)

        # 4. Resize the background to match the size of the processed image
        background_image = background_image.resize(processed_image.size)

        # 5. Create a new image to combine the background and the processed image
        final_image = Image.new("RGBA", background_image.size)
        final_image.paste(background_image, (0, 0))
        final_image.paste(processed_image, (0, 0), mask=processed_image)

        # 6. Save the final output image
        final_image.convert("RGB").save(output_path)
        print(f"Final image with new background saved to: {output_path}")

        # 7. Change the wallpaper to the output image
        if change_wallpaper(output_path):
            print("Wallpaper changed successfully!")
        else:
            print("Failed to change wallpaper.")
    except Exception as e:
        print(f"An error occurred: {e}")
