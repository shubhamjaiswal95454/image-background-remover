import streamlit as st
from PIL import Image
from rembg import remove
import io

st.title("AI-Powered Background Remover")

st.markdown("""
Upload an image (JPG/PNG), and instantly remove the background in high quality.
""")

@st.cache_data(show_spinner=True)
def remove_bg(input_image_bytes):
    # Use rembg to remove background from bytes and return PIL Image
    output = remove(input_image_bytes)
    return Image.open(io.BytesIO(output))

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")
    st.subheader("Original Image")
    st.image(image, use_container_width=True)
    
    with st.spinner("Removing background..."):
        result_img = remove_bg(input_bytes)
    
    st.subheader("Image with Background Removed")
    st.image(result_img, use_container_width=True)
    
    buf = io.BytesIO()
    # Save with high quality alpha (PNG)
    result_img.save(buf, format="PNG")
    st.download_button(
        label="Download Image (PNG)",
        data=buf.getvalue(),
        file_name="image_no_bg.png",
        mime="image/png"
    )
