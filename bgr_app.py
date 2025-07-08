import streamlit as st
import io
import os
import requests
from PIL import Image
from rembg import remove
import onnxruntime as ort
import tempfile
import zipfile
from urllib.parse import urlparse
import time

# Set page config
# Using an icon from a URL
st.set_page_config(
    page_title="Background Removal Tool",
    page_icon="https://i.ibb.co/m5DbdtZh/No-More-Backdrop.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-section {
        background-color: #e8f4f8;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1a5276;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []
if 'image_counter' not in st.session_state:
    st.session_state.image_counter = 1

def is_valid_url(url):
    """Check if the URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_image_from_url(url):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading image from URL: {str(e)}")
        return None

def remove_background(image_data, filename):
    """Remove background from image"""
    try:
        output_data = remove(image_data)
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}no_bg{st.session_state.image_counter}.png"
        st.session_state.image_counter += 1
        return output_data, output_filename
    except Exception as e:
        st.error(f"Error removing background: {str(e)}")
        return None, None

def process_single_image(image_data, filename):
    """Process a single image"""
    with st.spinner(f"Processing {filename}..."):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            original_img = Image.open(io.BytesIO(image_data))
            st.image(original_img, use_column_width=True)

        output_data, output_filename = remove_background(image_data, filename)

        if output_data:
            with col2:
                st.subheader("Background Removed")
                processed_img = Image.open(io.BytesIO(output_data))
                st.image(processed_img, use_column_width=True)

            st.download_button(
                label=f"Download {output_filename}",
                data=output_data,
                file_name=output_filename,
                mime="image/png",
                key=f"download_{st.session_state.image_counter}"
            )

            st.session_state.processed_images.append({
                'filename': output_filename,
                'data': output_data
            })

            st.success("Background removed successfully!")
        else:
            st.error("Failed to process the image.")

def create_zip_file():
    """Create a zip file with all processed images"""
    if not st.session_state.processed_images:
        return None

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for img_data in st.session_state.processed_images:
            zip_file.writestr(img_data['filename'], img_data['data'])

    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# Main app
def main():
    st.markdown('<h1 class="main-header">Background Removal Tool</h1>', unsafe_allow_html=True)

    st.sidebar.title("Instructions")
    st.sidebar.markdown("""
    ### How to use:
    1. Upload images using the uploader.
    2. Paste image URLs (one per line).
    3. Click process to remove backgrounds.
    4. Download individual or all images as ZIP.

    ### Supported formats:
    - PNG, JPG, JPEG, WebP, BMP
    - Output: PNG (preserves transparency)

    ### Features:
    - Multiple image processing
    - URL image processing
    - Batch download as ZIP
    - Real-time preview
    """)

    if st.sidebar.button("Clear All Processed Images"):
        st.session_state.processed_images = []
        st.session_state.image_counter = 1
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["Upload Images", "Add URLs", "Batch Download"])

    with tab1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("Upload Images")

        uploaded_files = st.file_uploader(
            "Choose images...",
            type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
            accept_multiple_files=True,
            help="Select one or more images to remove backgrounds"
        )

        if uploaded_files:
            st.write(f"{len(uploaded_files)} image(s) selected")

            if st.button("Process Uploaded Images", key="process_uploaded"):
                for uploaded_file in uploaded_files:
                    st.markdown(f"### Processing: {uploaded_file.name}")
                    image_data = uploaded_file.read()
                    process_single_image(image_data, uploaded_file.name)
                    st.divider()

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("Add Image URLs")

        urls_text = st.text_area(
            "Enter image URLs (one per line):",
            height=150,
            help="Paste image URLs, each on a new line"
        )

        if urls_text:
            urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
            if urls:
                st.write(f"{len(urls)} URL(s) found")

                valid_urls = []
                invalid_urls = []

                for url in urls:
                    if is_valid_url(url):
                        valid_urls.append(url)
                    else:
                        invalid_urls.append(url)

                if valid_urls:
                    st.success(f"{len(valid_urls)} valid URL(s)")
                if invalid_urls:
                    st.error(f"{len(invalid_urls)} invalid URL(s): {', '.join(invalid_urls)}")

                if valid_urls and st.button("Process URLs", key="process_urls"):
                    for i, url in enumerate(valid_urls):
                        st.markdown(f"### Processing URL {i+1}: {url}")
                        image_data = download_image_from_url(url)
                        if image_data:
                            filename = os.path.basename(urlparse(url).path)
                            if not filename or '.' not in filename:
                                filename = f"image_{i+1}.jpg"
                            process_single_image(image_data, filename)
                        else:
                            st.error(f"Failed to download image from: {url}")
                        st.divider()

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.subheader("Batch Download")

        if st.session_state.processed_images:
            st.write(f"{len(st.session_state.processed_images)} processed image(s) ready for download")

            cols = st.columns(3)
            for i, img_data in enumerate(st.session_state.processed_images):
                with cols[i % 3]:
                    st.write(f"{img_data['filename']}")
                    processed_img = Image.open(io.BytesIO(img_data['data']))
                    st.image(processed_img, use_column_width=True)

            zip_data = create_zip_file()
            if zip_data:
                st.download_button(
                    label="Download All as ZIP",
                    data=zip_data,
                    file_name=f"background_removed_images_{int(time.time())}.zip",
                    mime="application/zip",
                    key="download_zip"
                )
        else:
            st.info("No processed images yet. Process some images first!")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Background Removal Tool | Powered by rembg & Streamlit</p>
        <p>Upload images or paste URLs to remove backgrounds automatically</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
