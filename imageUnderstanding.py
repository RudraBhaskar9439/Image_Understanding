import os
from pathlib import Path
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import streamlit as st

# Constants
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("Please set GOOGLE_API_KEY in .env file")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32
}

# Helper functions
def get_image_path(image_name: str) -> Path:
    path = IMAGE_DIR / image_name
    if path.exists() and path.suffix.lower() in SUPPORTED_FORMATS:
        return path
    if '.' not in image_name:
        for ext in SUPPORTED_FORMATS:
            path = IMAGE_DIR / f"{image_name}{ext}"
            if path.exists():
                return path
    raise ValueError(f"Image '{image_name}' not found in {IMAGE_DIR} or format not supported.")

def analyze_image(image_name: str, prompt: str = "Describe this image in detail.") -> str:
    try:
        image_path = get_image_path(image_name)
        model = genai.GenerativeModel('gemini-2.0-flash')
        image = Image.open(image_path)
        response = model.generate_content([
            prompt,
            image
        ], generation_config=generation_config)
        return response.text or "No analysis generated."
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def compare_images(image1_name: str, image2_name: str) -> str:
    try:
        image1_path = get_image_path(image1_name)
        image2_path = get_image_path(image2_name)
        model = genai.GenerativeModel('gemini-2.0-flash')
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        response = model.generate_content([
            "Compare these two images and describe their differences.",
            image1,
            image2
        ], generation_config=generation_config)
        return response.text
    except Exception as e:
        return f"Error comparing images: {str(e)}"

def list_available_images() -> List[str]:
    return [f.name for f in IMAGE_DIR.iterdir() if f.suffix.lower() in SUPPORTED_FORMATS]

# Streamlit UI
st.set_page_config(page_title="🖼️ Gemini Vision AI", layout="wide")
st.sidebar.title("🧠 Gemini Vision")
mode = st.sidebar.radio("Choose Mode", ["Analyze Image", "Compare Images", "View Gallery"])

st.title("🖼️ Gemini Vision Assistant")
st.markdown("""
Upload or choose images to get detailed AI-generated descriptions or comparisons using Gemini Pro Vision.
""")

IMAGE_DIR.mkdir(exist_ok=True)
images = list_available_images()

if mode == "Analyze Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "webp"])
    if uploaded:
        img_path = IMAGE_DIR / uploaded.name
        with open(img_path, 'wb') as f:
            f.write(uploaded.read())
        images.append(uploaded.name)

    selected_img = st.selectbox("Choose an image to analyze", images)
    prompt = st.text_input("Prompt", value="Describe this image in detail.")

    if st.button("🔍 Analyze Image"):
        with st.spinner("Analyzing image..."):
            result = analyze_image(selected_img, prompt)
        st.image(get_image_path(selected_img), caption=selected_img, width=300)
        st.markdown("---")
        st.markdown("### 📝 Result:")
        st.write(result)

elif mode == "Compare Images":
    col1, col2 = st.columns(2)
    with col1:
        image1 = st.selectbox("Select first image", images, key="img1")
    with col2:
        image2 = st.selectbox("Select second image", images, key="img2")

    if st.button("🆚 Compare Images"):
        with st.spinner("Comparing images..."):
            result = compare_images(image1, image2)
        col1, col2 = st.columns(2)
        col1.image(get_image_path(image1), caption=image1, width=300)
        col2.image(get_image_path(image2), caption=image2, width=300)
        st.markdown("---")
        st.markdown("### 🔎 Comparison Result:")
        st.write(result)

elif mode == "View Gallery":
    st.markdown("### 📷 Available Images")
    if images:
        cols = st.columns(4)
        for i, img in enumerate(images):
            cols[i % 4].image(get_image_path(img), caption=img, width=150)
    else:
        st.info("No images found in the 'images' directory.")
