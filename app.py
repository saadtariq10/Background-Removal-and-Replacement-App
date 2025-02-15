import streamlit as st
from rembg import remove
from PIL import Image
import io

def main():
    st.title("Background Remover App")
    st.write("Upload an image, and this app will remove its background!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the original image
        image = Image.open(uploaded_file)
        st.subheader("Original Image:")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Removing background..."):
            uploaded_bytes = uploaded_file.read()  # Read the raw bytes from the uploaded file
            result = remove(uploaded_bytes, force_return_bytes=True)  # Ensure raw byte output
            bg_removed_image = Image.open(io.BytesIO(result))


        # Display the output image
        st.subheader("Image without Background:")
        st.image(bg_removed_image, caption="Background Removed", use_column_width=True)

        # Download the image
        buf = io.BytesIO()
        bg_removed_image.save(buf, format="PNG")
        buf.seek(0)

        st.download_button(
            label="Download Image Without Background",
            data=buf,
            file_name="bg_removed.png",
            mime="image/png",
        )

if __name__ == "__main__":
    main()
