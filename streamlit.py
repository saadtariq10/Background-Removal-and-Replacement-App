import os
import streamlit as st
from rembg import remove
from PIL import Image
import io

# Function to change wallpaper
def change_wallpaper(image_path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(
            20, 0, image_path, 0x01 | 0x02  # SPI_SETDESKWALLPAPER
        )
        return True
    except Exception as e:
        print(f"Error changing wallpaper: {e}")
        return False

# Main Streamlit app
def main():
    st.title("Background Removal and Replacement")

    # Allow user to upload an image
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the uploaded image
        input_image = Image.open(uploaded_file)

        # Show the uploaded image to the user
        st.image(input_image, caption="Uploaded Image", use_column_width=True)

        # Remove the background using rembg
        st.write("Removing background...")
        output_image = remove(input_image)
        st.image(output_image, caption="Processed Image (No Background)", use_column_width=True)

        # List all background images in the 'backgrounds' folder
        background_folder = "backgrounds"
        background_files = [f for f in os.listdir(background_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

        # Check if any background images are available
        if not background_files:
            st.write("No background images available in the folder.")
        else:
            st.write("Available Backgrounds:")
            preview_images = []  # To store the resulting images for download

            # For each background image, combine with the processed image
            for background_file in background_files:
                background_path = os.path.join(background_folder, background_file)
                background_image = Image.open(background_path)

                # Resize background to match processed image size
                background_image = background_image.resize(output_image.size)

                # Create a new image with background and overlay the processed image
                final_image = Image.new("RGBA", background_image.size)
                final_image.paste(background_image, (0, 0))
                final_image.paste(output_image, (0, 0), mask=output_image)

                # Convert to RGB and save the final image for downloading
                final_image_rgb = final_image.convert("RGB")
                img_byte_arr = io.BytesIO()
                final_image_rgb.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)

                # Show the final image preview
                st.image(final_image_rgb, caption=f"Background: {background_file}", use_column_width=True)

                # Provide download button
                preview_images.append((background_file, img_byte_arr))

            # Provide a download button for each final image
            for background_file, img_byte_arr in preview_images:
                st.download_button(
                    label=f"Download Image with {background_file}",
                    data=img_byte_arr,
                    file_name=f"final_with_{background_file}",
                    mime="image/png"
                )

# Run the app
if __name__ == "__main__":
    main()
